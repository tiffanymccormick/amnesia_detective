#!/usr/bin/env python3
import argparse, curses, os, sys, time, yaml, subprocess

# Minimal WASD runner with one player, walls, and hotspots.
# Map YAML format:
# name: "Portrait Room"
# size: [cols, rows]
# player: { x: 2, y: 10 }
# walls:    # list of segments [x1,y1,x2,y2] or single cells [x,y,x,y]
#   - [0,0,30,0]
# hotspots:
#   - id: "odd_portrait"
#     x: 24; y: 3
#     on_enter:
#       - say: "HYDE: That portrait... it’s wrong."
#       - open_file: "~/CaseFiles/CrimeScene-Scan3.jpg"
#       - say: "TIP: exiftool CrimeScene-Scan3.jpg"
#       - next_scene: true
# decor:
#   - glyph: "#"
#     positions: [[5,3],[10,3],...]

ASSETS = "/opt/amnesia"

def load_map(name):
    path = os.path.join(ASSETS, "maps", f"{name}.yaml")
    with open(path, "r") as f:
        return yaml.safe_load(f)

def wall_cells(seg):
    x1,y1,x2,y2 = seg
    cells=[]
    if x1==x2:
        ylo,yhi = sorted((y1,y2))
        for y in range(ylo,yhi+1): cells.append((x1,y))
    elif y1==y2:
        xlo,xhi = sorted((x1,x2))
        for x in range(xlo,xhi+1): cells.append((x,y1))
    else:
        cells.append((x1,y1))
    return set(cells)

def draw(stdscr, m, px, py):
    stdscr.clear()
    cols, rows = m["size"]
    title = f"Memory: {m.get('name','')}"
    stdscr.addstr(0, 0, title[:cols])
    # draw bounds
    for x in range(cols): stdscr.addch(1, x, "-")
    for x in range(cols): stdscr.addch(rows, x, "-")
    for y in range(2, rows): stdscr.addch(y, 0, "|"); stdscr.addch(y, cols-1, "|")
    # walls
    walls=set()
    for seg in m.get("walls", []):
        walls |= wall_cells(seg)
    for (x,y) in walls:
        if 1<y<rows and 0<x<cols-1:
            stdscr.addch(y, x, "#")
    # decor
    for d in m.get("decor", []):
        g = d.get("glyph","#")
        for (x,y) in d.get("positions", []):
            if 1<y<rows and 0<x<cols-1:
                stdscr.addch(y, x, g)
    # player
    stdscr.addch(py, px, "@")
    stdscr.addstr(rows+1, 0, "[WASD] move  [E] interact  [Q] exit")
    stdscr.refresh()

def say_box(msg):
    # simple stdout line; keep it minimal/compatible with terminal
    print(msg); sys.stdout.flush(); time.sleep(0.6)

def run_action(act):
    if "say" in act:
        say_box(act["say"])
    elif "open_file" in act:
        path = os.path.expanduser(act["open_file"])
        subprocess.Popen(["xdg-open", path])
    elif "next_scene" in act and act["next_scene"]:
        raise SystemExit(0)

def handle_hotspots(m, px, py):
    for h in m.get("hotspots", []):
        if px == h.get("x") and py == h.get("y"):
            for act in h.get("on_enter", []):
                run_action(act)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--map", required=True, help="map name (yaml without .yaml)")
    args = ap.parse_args()
    m = load_map(args.map)
    cols, rows = m["size"]
    px, py = m["player"]["x"], m["player"]["y"]
    walls=set()
    for seg in m.get("walls", []):
        walls |= wall_cells(seg)

    def inside(nx, ny):
        return 1<ny<rows and 0<nx<cols-1 and (nx,ny) not in walls

    def loop(stdscr):
        nonlocal px, py
        curses.curs_set(0)
        stdscr.nodelay(False)
        while True:
            draw(stdscr, m, px, py)
            ch = stdscr.getch()
            if ch in (ord('q'), ord('Q')): break
            nx, ny = px, py
            if ch in (ord('w'), ord('W')): ny -= 1
            elif ch in (ord('s'), ord('S')): ny += 1
            elif ch in (ord('a'), ord('A')): nx -= 1
            elif ch in (ord('d'), ord('D')): nx += 1
            elif ch in (ord('e'), ord('E')):
                handle_hotspots(m, px, py)
            if inside(nx, ny): px, py = nx, ny

    curses.wrapper(loop)

if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
