#!/usr/bin/env bash
set -euo pipefail
SCENE="${1:-intro}"
SCENE_FILE="/opt/amnesia/cutscenes/${SCENE}.txt"
[[ -f "$SCENE_FILE" ]] || { echo "Scene not found: $SCENE_FILE" >&2; exit 1; }

x-terminal-emulator -T "Memory Log" -e bash -lc '
  tput setaf 2; echo "[Memory recovered...]"; tput sgr0;
  while IFS= read -r line; do
    printf "%s\n" "$line"
    sleep 1
  done < "'"$SCENE_FILE"'"
  echo
  read -p "[Press Enter to continue] " _
'