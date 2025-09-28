#!/usr/bin/env bash
set -euo pipefail

USER_NAME="${SUDO_USER:-$USER}"
USER_HOME="$(eval echo "~$USER_NAME")"

echo "[*] Installing forensic + desktop tools..."
sudo apt-get update
sudo apt-get install -y --no-install-recommends \
  xfce4 xfce4-terminal thunar lightdm \
  poppler-utils qpdf exiftool sqlite3 binwalk steghide unzip zip xxd file \
  ripmime mpack python3 curl wget

echo "[*] Installing Antiquity font..."
sudo mkdir -p /usr/local/share/fonts
sudo install -m 0644 vm/fonts/antiquity-print.ttf /usr/local/share/fonts/antiquity-print.ttf
sudo fc-cache -fv >/dev/null

echo "[*] Staging runtime data..."
sudo mkdir -p /opt/amnesia/{wallpapers,golden,logs,cutscenes,maps}
sudo cp -a vm/wallpapers/*.png /opt/amnesia/wallpapers/
sudo cp -a cutscenes/*.txt /opt/amnesia/cutscenes/ || true
sudo cp -a cutscenes/maps/*.yaml /opt/amnesia/maps/ || true
sudo cp -a clues/* /opt/amnesia/golden/

echo "[*] Installing scripts..."
sudo install -m 0755 scripts/unlock_case.sh     /opt/amnesia/unlock_case.sh
sudo install -m 0755 scripts/reset_casefiles.sh /opt/amnesia/reset_casefiles.sh
sudo install -m 0755 scripts/show_scene.sh      /opt/amnesia/show_scene.sh
sudo install -m 0755 scripts/xfce_wallpaper.sh  /opt/amnesia/xfce_wallpaper.sh
sudo install -m 0755 scripts/place_shortcuts.sh /opt/amnesia/place_shortcuts.sh
sudo install -m 0755 scripts/run_scene.py       /opt/amnesia/run_scene.py
sudo chown -R "$USER_NAME:$USER_NAME" /opt/amnesia

echo "[*] Seed CaseFiles with Stage 1..."
mkdir -p "$USER_HOME/CaseFiles"
rm -rf "$USER_HOME/CaseFiles"/*
cp -a /opt/amnesia/golden/01/* "$USER_HOME/CaseFiles/"
chown -R "$USER_NAME:$USER_NAME" "$USER_HOME/CaseFiles"

echo "[*] Place desktop shortcuts..."
sudo -u "$USER_NAME" /opt/amnesia/place_shortcuts.sh

echo "[*] Apply Stage 1 wallpaper..."
sudo -u "$USER_NAME" /opt/amnesia/xfce_wallpaper.sh "/opt/amnesia/wallpapers/stage1_study.png"

echo "[*] Build complete. Try: /opt/amnesia/unlock_case.sh 19A7-DELTA"