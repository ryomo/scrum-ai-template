#!/usr/bin/env python3
"""Reads the backlog in GitHub Projects.

Non-obvious points:
  - `gh project item-list` and `gh issue list` hold different data. The former has Sprints and
    Story Points but no parent/child relations; the latter is the opposite. One ProjectV2 GraphQL
    query is faster than calling both and joining them, and misses nothing, so all lists use it.
  - Of the Sprint (Iteration) field, `configuration.iterations` are the current and future Sprints
    and `completedIterations` are past ones.
  - Story Points are set on parent issues only, so totals add up parents only.
    Children are listed under their parent but not counted.
  - Besides issues, a Project holds draft issues (no number, shown as `#-`) and PRs filed
    without an issue (marked `[PR]`).
  - Projects cannot exclude weekends, so a Sprint's period includes them.
    The remaining days are counted as weekdays, including today, so they are not mistaken for working days.
  - `show` does not use `gh issue view --comments`: when stdout is not a terminal it prints only the
    comments, without the body, so an agent calling it could not read the body. It builds the output from JSON.
"""

import argparse
import datetime
import json
import pathlib
import subprocess
import sys

CONFIG_PATH = pathlib.Path(__file__).with_name("config.json")

QUERY = """
query($owner:String!, $number:Int!, $cursor:String) {
  owner: %s(login:$owner) {
    projectV2(number:$number) {
      title url readme
      field(name:"Sprint") {
        ... on ProjectV2IterationField {
          configuration {
            iterations { title startDate duration }
            completedIterations { title startDate duration }
          }
        }
      }
      items(first:100, after:$cursor) {
        pageInfo { hasNextPage endCursor }
        nodes {
          fieldValues(first:20) {
            nodes {
              ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2FieldCommon { name } } }
              ... on ProjectV2ItemFieldNumberValue { number field { ... on ProjectV2FieldCommon { name } } }
              ... on ProjectV2ItemFieldIterationValue { title field { ... on ProjectV2FieldCommon { name } } }
            }
          }
          content {
            __typename
            ... on DraftIssue { title }
            ... on Issue {
              number title state
              parent { number }
              subIssuesSummary { total completed }
            }
            ... on PullRequest { number title state }
          }
        }
      }
    }
  }
}
"""

STATUS_LABEL = {"Todo": "Todo", "In Progress": "WIP", "Done": "Done"}


def load_config() -> dict:
    """Reads the owner, Project number, and repository written by scripts/setup.sh."""
    try:
        config = json.loads(CONFIG_PATH.read_text())
    except FileNotFoundError:
        sys.exit(f"{CONFIG_PATH} not found. Run scripts/setup.sh first")
    if config.get("ownerType") not in ("user", "organization"):
        sys.exit(f'ownerType in {CONFIG_PATH} must be "user" or "organization"')
    return config


def gh(*args: str) -> str:
    try:
        r = subprocess.run(["gh", *args], capture_output=True, text=True, check=True)
    except FileNotFoundError:
        sys.exit("gh command not found")
    except subprocess.CalledProcessError as e:
        # A missing project scope ends up here. Ask a human to run: gh auth refresh -s project
        sys.exit(f"gh failed:\n{e.stderr.strip()}")
    return r.stdout


def fetch(config: dict) -> tuple[dict, list[dict]]:
    """Fetches the Project's metadata and all of its items."""
    query = QUERY % config["ownerType"]
    project, items, cursor = None, [], None
    while True:
        args = [
            "api",
            "graphql",
            "-F",
            f"owner={config['owner']}",
            "-F",
            f"number={config['project']}",
            "-f",
            f"query={query}",
        ]
        if cursor:
            args += ["-F", f"cursor={cursor}"]
        project = json.loads(gh(*args))["data"]["owner"]["projectV2"]
        items += [parse_item(n) for n in project["items"]["nodes"]]
        page = project["items"]["pageInfo"]
        if not page["hasNextPage"]:
            return project, items
        cursor = page["endCursor"]


def parse_item(node: dict) -> dict:
    content = node["content"] or {}
    fields = {}
    for v in node["fieldValues"]["nodes"]:
        name = (v.get("field") or {}).get("name")
        if name:
            fields[name] = v.get("name") or v.get("title") or v.get("number")
    return {
        "num": content.get("number"),
        "title": content.get("title", "(no title)"),
        "draft": content.get("__typename") == "DraftIssue",
        "pr": content.get("__typename") == "PullRequest",
        "parent": (content.get("parent") or {}).get("number"),
        "sub": content.get("subIssuesSummary") or {"total": 0, "completed": 0},
        "status": fields.get("Status", "-"),
        "sprint": fields.get("Sprint"),
        "point": fields.get("Story Point"),
    }


def _point(value: float | None) -> str:
    """Formats Story Points for display. "-" if not estimated."""
    if value is None:
        return "-"
    return (str(int(value)) if float(value).is_integer() else str(value)) + "pt"


def _line(item: dict, child: bool = False, orphan: bool = False) -> None:
    """Prints one item as one line of a list."""
    num = f"#{item['num']}" if item["num"] else "#-"
    marks = ""
    if item["sub"]["total"]:
        marks += f"  [sub {item['sub']['completed']}/{item['sub']['total']}]"
    # A child whose parent is not in the list gets the parent's number,
    # so its missing points are not mistaken for a missing estimate
    if orphan:
        marks += f"  [parent #{item['parent']}]"
    if item["draft"]:
        marks += "  [draft]"
    # Issues and PRs share one number sequence, so PRs need a mark to tell them apart
    if item["pr"]:
        marks += "  [PR]"
    indent = "  └ " if child else ""
    print(
        f"{STATUS_LABEL.get(item['status'], item['status']):<5}{_point(item['point']):>4}  "
        f"{num:<6}{indent}{item['title']}{marks}"
    )


def _children(parent: dict, items: list[dict]) -> None:
    """Prints the children of `parent` under it."""
    # Drafts have no number; matching on it would pick up every item without a parent as a child
    if not parent["num"]:
        return
    for child in items:
        if child["parent"] == parent["num"]:
            _line(child, child=True)


def show(header: str, items: list[dict], chosen: list[dict]) -> None:
    """Prints children under their parent, even children that are not in `chosen`."""
    print(header, end="\n\n")
    if not chosen:
        print("(none)")
        return
    ids = {i["num"] for i in chosen if i["num"]}
    order = {"In Progress": 0, "Todo": 1}
    total = done = 0
    for item in sorted(chosen, key=lambda i: order.get(i["status"], 2)):
        if item["parent"] and item["parent"] in ids:
            continue  # printed under its parent
        _line(item, orphan=bool(item["parent"]))
        if item["point"] is not None:
            total += item["point"]
            done += item["point"] if item["status"] == "Done" else 0
        _children(item, items)
    print(
        f"\n{len(chosen)} items / {_point(done)} done of {_point(total)}"
        " (points are on parent issues only)"
    )


def cmd_show(config: dict, number: str) -> None:
    issue = json.loads(
        gh(
            "issue",
            "view",
            number,
            "--repo",
            config["repo"],
            "--json",
            "title,state,labels,body,comments",
        )
    )
    labels = ", ".join(label["name"] for label in issue["labels"])
    print(f"#{number} {issue['title']}  [{issue['state']}]  {labels}", end="\n\n")
    print(issue["body"].rstrip())
    for c in issue["comments"]:
        print(f"\n---- comment: {c['author']['login']} {c['createdAt'][:10]} ----\n")
        print(c["body"].rstrip())


def cmd_sprint(project: dict, items: list[dict], _args) -> None:
    iterations = project["field"]["configuration"]["iterations"]
    if not iterations:
        sys.exit("No Sprint in progress. Add an Iteration in the Project settings")
    # `iterations` also holds future ones, and its first entry is the next Sprint when there is a gap between Sprints
    current = iterations[0]
    start = datetime.date.fromisoformat(current["startDate"])
    end = start + datetime.timedelta(days=current["duration"] - 1)
    today = datetime.date.today()
    if today < start:
        sys.exit(f"No Sprint in progress. Next: {current['title']} starts on {start}")
    left = sum(
        1
        for d in range((end - today).days + 1)
        if (today + datetime.timedelta(days=d)).weekday() < 5
    )
    show(
        f"{current['title']}\n{start} - {end} ({left} weekdays left, including today)",
        items,
        [i for i in items if i["sprint"] == current["title"]],
    )


def cmd_backlog(_project: dict, items: list[dict], _args) -> None:
    show(
        "Backlog (no Sprint, not Done)",
        items,
        [i for i in items if not i["sprint"] and i["status"] != "Done"],
    )


def cmd_list(_project: dict, items: list[dict], args) -> None:
    if args.all:
        show("All items", items, items)
    else:
        show(
            "All items except Done (use list --all to include them)",
            items,
            [i for i in items if i["status"] != "Done"],
        )


def cmd_overview(project: dict, _items: list[dict], _args) -> None:
    """The Project's README and its Sprints."""
    print(project["title"], project["url"], end="\n\n")
    print((project["readme"] or "(no README)").strip(), end="\n\n")
    config = project["field"]["configuration"]
    for label, key in (("current", "iterations"), ("done   ", "completedIterations")):
        for it in config[key]:
            print(f"{label}  {it['startDate']} ({it['duration']} days)  {it['title']}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="cmd")
    sub.add_parser("sprint", help="items in the current Sprint (default)")
    sub.add_parser("backlog", help="items not assigned to a Sprint")
    p_list = sub.add_parser("list", help="all items")
    p_list.add_argument("--all", action="store_true", help="include Done")
    sub.add_parser("overview", help="Project README and Sprints")
    p_show = sub.add_parser("show", help="issue body and comments")
    p_show.add_argument("number")
    args = parser.parse_args()

    config = load_config()
    if args.cmd == "show":
        cmd_show(config, args.number)
        return

    project, items = fetch(config)
    {
        "backlog": cmd_backlog,
        "list": cmd_list,
        "overview": cmd_overview,
        None: cmd_sprint,
        "sprint": cmd_sprint,
    }[args.cmd](project, items, args)


if __name__ == "__main__":
    main()
