#!/usr/bin/env bash
# Sync Farm-Grind/claude-skills → /mnt/skills/user/
# No credentials required — repo is public.
# Usage: bash sync-skills.sh
#
# Guarantees:
#   - Atomic: stages to temp dir before touching live target
#   - Delete: skills removed from repo are removed from /mnt/skills/user/
#   - Idempotent: safe to run multiple times per session

set -euo pipefail

REPO="https://github.com/Farm-Grind/claude-skills.git"
STAGE_DIR="/tmp/claude-skills-stage-$$"
TARGET="/mnt/skills/user"

cleanup() {
  rm -rf "$STAGE_DIR"
}
trap cleanup EXIT

echo "[sync] Cloning Farm-Grind/claude-skills (public, no auth)..."
git clone --depth=1 --quiet "$REPO" "$STAGE_DIR"

echo "[sync] Syncing skills/ → $TARGET ..."

python3 - "$STAGE_DIR/skills" "$TARGET" <<'PYEOF'
import sys, os, shutil

src = sys.argv[1]
dst = sys.argv[2]

repo_skills = set(os.listdir(src))
live_skills  = set(os.listdir(dst)) if os.path.isdir(dst) else set()

# Remove skills no longer in repo
for name in live_skills - repo_skills:
    path = os.path.join(dst, name)
    if os.path.isdir(path):
        shutil.rmtree(path)
        print(f"  [delete] {name}")
    elif os.path.isfile(path):
        os.remove(path)
        print(f"  [delete] {name}")

# Copy/overwrite skills from repo
os.makedirs(dst, exist_ok=True)
for name in repo_skills:
    src_path = os.path.join(src, name)
    dst_path = os.path.join(dst, name)
    if os.path.isdir(src_path):
        if os.path.exists(dst_path):
            shutil.rmtree(dst_path)
        shutil.copytree(src_path, dst_path)
    else:
        shutil.copy2(src_path, dst_path)
    print(f"  [sync]   {name}")

print(f"\n[sync] Done. {len(repo_skills)} skills deployed, {len(live_skills - repo_skills)} removed.")
PYEOF
