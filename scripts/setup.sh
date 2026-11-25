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
     Start it on the day of the first Sprint Planning; a past date shortens the first Sprint.
     Its Sprint Goal is added at Sprint Planning
  3. Edit the Sprint section of the Project README if you changed the length or start day
Then commit .agents/skills/backlog/config.json.

Next, hold the first Sprint Planning: see "The first Sprint Planning" in docs/SCRUM.md.
EOF
