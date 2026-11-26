#!/bin/sh
# Sets up a repository created from this template:
#   - creates the labels in .github/labels.json
#   - copies the template GitHub Project (views and fields cannot be created through the API) and links it to the repository
#   - writes the Project's README from .github/project-readme.md
#   - writes .agents/skills/backlog/config.json
#   - enables githooks/
#
# Usage: scripts/setup.sh [--project N] [--prune-labels]
#   --project N     use an existing Project N instead of copying the template
#   --prune-labels  delete labels not in .github/labels.json (e.g. GitHub's defaults such as "question")
#
# Requires gh with the project scope (gh auth refresh -s project) and python3.

set -eu

TEMPLATE_OWNER=ryomo
TEMPLATE_PROJECT=8

project=""
prune=false
while [ $# -gt 0 ]; do
  case "$1" in
    --project) project="$2"; shift 2 ;;
    --prune-labels) prune=true; shift ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

cd "$(git rev-parse --show-toplevel)"

repo=$(gh repo view --json nameWithOwner --jq .nameWithOwner)
owner=${repo%%/*}
# The GraphQL query in backlog.py differs between user and organization owners
case "$(gh api "users/$owner" --jq .type)" in
  Organization) owner_type=organization ;;
  *) owner_type=user ;;
esac

echo "== Labels"
python3 -c '
import json, sys
for label in json.load(open(".github/labels.json")):
    print("\t".join((label["name"], label["color"], label["description"])))
' | while IFS="$(printf '\t')" read -r name color description; do
  gh label create "$name" --repo "$repo" --color "$color" --description "$description" --force
  # Print the result here because gh prints nothing when stdout is not a terminal
  echo "Created or updated: $name"
done
if $prune; then
  keep=$(python3 -c 'import json; print("\n".join(l["name"] for l in json.load(open(".github/labels.json"))))')
  gh label list --repo "$repo" --limit 200 --json name --jq '.[].name' | while read -r name; do
    if ! printf '%s\n' "$keep" | grep -qxF "$name"; then
      gh label delete "$name" --repo "$repo" --yes
      echo "Deleted: $name"
    fi
  done
fi

echo "== Project"
if [ -z "$project" ]; then
  project=$(gh project copy "$TEMPLATE_PROJECT" \
    --source-owner "$TEMPLATE_OWNER" \
    --target-owner "$owner" \
    --title "${repo#*/}" \
    --format json --jq .number)
  echo "Copied the template to Project $project"
fi
gh project link "$project" --owner "$owner" --repo "$repo"
gh project edit "$project" --owner "$owner" \
  --readme "$(sed "s|{{REPO}}|$repo|g" .github/project-readme.md)"

cat > .agents/skills/backlog/config.json <<EOF
{
  "owner": "$owner",
  "ownerType": "$owner_type",
  "project": $project,
  "repo": "$repo"
}
EOF

git config core.hooksPath githooks

url=$(gh project view "$project" --owner "$owner" --format json --jq .url)
cat <<EOF

Done. Finish these in the browser ($url):
  1. Workflows > Default workflows > "Auto-add to project" > Edit > Filters:
     select $repo, set the filter to is:issue,pr, and click "Save and turn on workflow".
     Copying a Project does not copy this workflow. It is not "Item added to project",
     nor the "Default repository" in the Project settings
  2. Settings > Sprint: add the first Iteration titled "Sprint 1", with the length you want.
     Its start date is settled while preparing for Sprint Planning (below),
     and its Sprint Goal at Sprint Planning
  3. Edit the Sprint section of the Project README if you changed the length or start day

Then, in this session, prepare for the first Sprint Planning:
  1. Decide the first Sprint's start date: today with the full length,
     or the regular start day even if shorter. Adjust the Iteration to match
  2. Decide the Product Goal and file it as a product-goal issue
  3. File the first PBIs and order them
  4. Fill in AGENTS.md (product, stack, commands, who merges PRs and how)
     and docs/DEFINITION_OF_DONE.md.
     Sprint Planning needs them to forecast and plan the work.
     Also decide whether agents keep posting How comments on PBIs
     without waiting for instructions (the default in AGENTS.md)
  5. Commit .agents/skills/backlog/config.json and these files, and merge them into main
Then start a new session and hold Sprint Planning as docs/SCRUM.md describes
(e.g. "Hold Sprint Planning for Sprint 1").
EOF
