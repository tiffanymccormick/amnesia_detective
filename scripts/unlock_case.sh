#!/usr/bin/env bash
set -euo pipefail

CODE="${1:-}"
if [[ -z "$CODE" ]]; then
  echo "Usage: $0 UNLOCK_CODE"; exit 1; fi

USER_NAME="${SUDO_USER:-$USER}"
USER_HOME="$(eval echo "~$USER_NAME")"
CASE="$USER_HOME/CaseFiles"
GOLD="/opt/amnesia/golden"
WALL="/opt/amnesia/wallpapers"
LOG="/opt/amnesia/logs/unlocks.log"

unlock() {
  local src="$1" scene="$2" wp="$3" mode="${4:-linear}"
  cp -a "$src"/* "$CASE"/
  chown -R "$USER_NAME:$USER_NAME" "$CASE"
  /opt/amnesia/xfce_wallpaper.sh "$wp"
  if [[ "$mode" == "wasd" ]]; then
    python3 /opt/amnesia/run_scene.py --map "$scene"
  else
    /opt/amnesia/show_scene.sh "$scene"
  fi
  echo "[$(date -Is)] Unlocked: $src" | tee -a "$LOG"
  echo -e "\n==============================="
  echo   "  NEW EVIDENCE RECEIVED"
  echo   "==============================="
}

case "$CODE" in
  "19A7-DELTA")
    unlock "$GOLD/02" "basement" "$WALL/stage2_basement.png" "wasd"
    ;;
  "K4-OSINT")
    unlock "$GOLD/03" "portraits" "$WALL/stage3_portraits.png" "wasd"
    ;;
  "J9-META")
    unlock "$GOLD/04" "stage4" "$WALL/stage4_corkboard.png" "linear"
    ;;
  "7F-WAL")
    unlock "$GOLD/05" "finale" "$WALL/stage5_confession.png" "linear"
    ;;
  *)
    echo "Invalid unlock code."; exit 1;;
esac