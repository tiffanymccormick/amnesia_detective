#!/usr/bin/env bash
set -euo pipefail
IMG="${1:-}"
if [[ -z "$IMG" || ! -f "$IMG" ]]; then
  echo "Usage: $0 /path/to/wallpaper.png" >&2
  exit 1
fi

PROP="/backdrop/screen0/monitor0/workspace0/last-image"
xfconf-query -c xfce4-desktop -p "$PROP" -s "$IMG" || {
  if command -v feh >/dev/null 2>&1; then feh --bg-scale "$IMG"; else
    echo "Warning: failed to set wallpaper (xfconf + feh missing)."
  fi
}