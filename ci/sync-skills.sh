#!/usr/bin/env bash
# Sync Farm-Grind/claude-skills → /mnt/skills/user/
# Run at session start. Requires PAT via GITHUB_PAT env var or first argument.
# Usage: bash sync-skills.sh <PAT>
#        GITHUB_PAT=<PAT> bash sync-skills.sh

set -e

PAT="${1:-$GITHUB_PAT}"
if [ -z "$PAT" ]; then
  echo "ERROR: PAT required. Pass as argument or set GITHUB_PAT env var." >&2
  exit 1
fi

REPO="https://${PAT}@github.com/Farm-Grind/claude-skills.git"
CLONE_DIR="/tmp/claude-skills-sync-$$"
TARGET="/mnt/skills/user"

echo "Cloning Farm-Grind/claude-skills..."
git clone --depth=1 --quiet "$REPO" "$CLONE_DIR"

echo "Syncing skills/ → $TARGET ..."
cp -a "$CLONE_DIR/skills/." "$TARGET/"

echo "Cleaning up..."
rm -rf "$CLONE_DIR"

echo "Done. Skills deployed:"
ls "$TARGET"
