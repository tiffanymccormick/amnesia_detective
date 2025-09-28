#!/usr/bin/env bash
set -euo pipefail
DESKTOP="$HOME/Desktop"
mkdir -p "$DESKTOP"

ICON_DIR="$HOME/amnesia_detective/vm/icons"
icon_or() { [[ -f "$1" ]] && echo "$1" || echo "utilities-terminal"; }

cat > "$DESKTOP/Read First.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Read First
Exec=xdg-open $HOME/CaseFiles/README.txt
Icon=$(icon_or "$ICON_DIR/fileexplorer.png")
Terminal=false
EOF
chmod +x "$DESKTOP/Read First.desktop"

cat > "$DESKTOP/Open Case Files.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Open Case Files
Exec=xdg-open $HOME/CaseFiles
Icon=$(icon_or "$ICON_DIR/fileexplorer.png")
Terminal=false
EOF
chmod +x "$DESKTOP/Open Case Files.desktop"

cat > "$DESKTOP/Reset Case Files.desktop" <<EOF
[Desktop Entry]
Type=Application
Name=Reset Case Files
Exec=pkexec /opt/amnesia/reset_casefiles.sh
Icon=$(icon_or "$ICON_DIR/floppydisk.png")
Terminal=false
EOF
chmod +x "$DESKTOP/Reset Case Files.desktop"