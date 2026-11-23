#!/usr/bin/env bash
set -euo pipefail

repo="StefanB-Qadna/catch-up"
ref="${CATCH_UP_REF:-main}"
dest="${CLAUDE_CONFIG_DIR:-$HOME/.claude}/skills/catch-up"

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

curl -fsSL "https://codeload.github.com/$repo/tar.gz/$ref" | tar -xz -C "$tmp"
src="$(find "$tmp" -mindepth 3 -maxdepth 3 -type d -path '*/skills/catch-up')"
[ -n "$src" ] || { echo "install: skills/catch-up not found in $repo@$ref" >&2; exit 1; }

mkdir -p "$(dirname "$dest")"
rm -rf "$dest"
cp -R "$src" "$dest"
echo "Installed /catch-up to $dest. Restart Claude Code to load it."
