#!/bin/sh
# Deletes files in docs/drafts/ not modified for more than 14 days. Called by githooks/post-checkout.
# Age is counted from the last modification, so a rewritten draft starts over.

cd "$(git rev-parse --show-toplevel)" || exit 0

[ -d docs/drafts ] || exit 0
find docs/drafts -mindepth 1 -type f ! -path docs/drafts/.gitkeep -mtime +14 -delete
# Deleting files updates the directory's mtime, so directories are removed when empty, not by age
find docs/drafts -mindepth 1 -type d -empty -delete
