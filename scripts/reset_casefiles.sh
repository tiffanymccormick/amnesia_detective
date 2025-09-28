#!/usr/bin/env bash
set -euo pipefail
USER_NAME="${SUDO_USER:-$USER}"
USER_HOME="$(eval echo "~$USER_NAME")"
CASE="$USER_HOME/CaseFiles"

rm -rf "$CASE"
mkdir -p "$CASE"
cp -a /opt/amnesia/golden/01/* "$CASE"/
chown -R "$USER_NAME:$USER_NAME" "$CASE"
/opt/amnesia/xfce_wallpaper.sh "/opt/amnesia/wallpapers/stage1_study.png"
echo "$(date -Is) reset" >> /opt/amnesia/logs/reset.log