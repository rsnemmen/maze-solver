"""
Ad-hoc visualization: render a side-by-side MP4 of all solvers on one maze.

Requires the optional [viz] dependencies:
    pip install maze-solvers[viz]

Usage:
    from maze_solvers.maze import generate_maze, build_valid_moves
    from maze_solvers.solvers import SOLVERS
    from maze_solvers.visualize import render_video, display_video

    grid = generate_maze(20, 20)
    moves = build_valid_moves(grid, 20, 20)
    start, goal = (0, 0), (19, 19)

    snaps = {}
    for cls, name in SOLVERS:
        full = list(cls(name, start, goal, moves).solve_generator())
        sampled = full[::2]
        if full and (not sampled or sampled[-1].get('p') is None):
            sampled.append(full[-1])
        snaps[name] = sampled

    rankings = {name: rank for rank, (_, name) in enumerate(
        sorted((len(list(cls(name, start, goal, moves).solve_generator())), name)
               for cls, name in SOLVERS), 1)}

    fname = render_video(snaps, grid, rankings)
    display(display_video(fname))
"""

import io
import base64

import numpy as np
from IPython.display import HTML

try:
    import cv2
except ImportError as exc:
    raise ImportError("visualize.py requires opencv-python: pip install maze-solvers[viz]") from exc

from .solvers import SOLVERS

ALGO_COLORS = {
    "A*": (120, 0, 0),
    "Dijkstra": (0, 0, 120),
    "Greedy Best-First": (0, 100, 0),
    "BFS": (120, 60, 0),
    "DFS": (60, 0, 120),
    "Bidirectional BFS": (60, 60, 60),
    "Weighted A*": (120, 0, 60),
    "Recursive Backtrack": (100, 100, 0),
    "Wall Follower": (0, 100, 100),
}
FINAL_PATH_COLOR = (0, 255, 0)
FPS = 12
SUBPLOT_SIZE = 512
TITLE_H = 100


def render_video(snaps_dict: dict, grid_vis: np.ndarray, rankings_final: dict, filename: str = "maze_showdown.mp4") -> str:
    rows, cols = grid_vis.shape
    video_size = (SUBPLOT_SIZE * 3, SUBPLOT_SIZE * 3 + TITLE_H)
    out = cv2.VideoWriter(filename, cv2.VideoWriter_fourcc(*"mp4v"), FPS, video_size)
    max_f = max(len(s) for s in snaps_dict.values())
    base_p = grid_vis == 1
    last_img = None

    for step in range(max_f):
        img = np.zeros((video_size[1], video_size[0], 3), dtype=np.uint8)
        for i, (_, name) in enumerate(SOLVERS):
            snaps = snaps_dict.get(name, [])
            state = snaps[min(step, len(snaps) - 1)]
            sub = np.zeros((rows, cols, 3), np.uint8)
            sub[base_p] = (255, 255, 255)
            v = state["v"]
            if v.any():
                rr, cc = v.nonzero()
                sub[2 * rr + 1, 2 * cc + 1] = ALGO_COLORS[name]
            res = cv2.resize(sub, (SUBPLOT_SIZE, SUBPLOT_SIZE), interpolation=cv2.INTER_NEAREST)
            rank_text = ""
            found_p = state.get("p")
            if found_p is not None and step >= len(snaps) - 1:
                rank_text = f" #{rankings_final[name]}"
                pts = np.array([(2 * c + 1, 2 * r + 1) for r, c in found_p], np.float32)
                pts *= SUBPLOT_SIZE / cols
                cv2.polylines(res, [pts.astype(np.int32)], False, FINAL_PATH_COLOR, 14, cv2.LINE_AA)
            cv2.rectangle(res, (0, 0), (SUBPLOT_SIZE, 40), (0, 0, 0), -1)
            cv2.putText(res, name + rank_text, (15, 30), 0, 0.9, (255, 255, 255), 2)
            ri, ci = i // 3, i % 3
            img[TITLE_H + ri * SUBPLOT_SIZE:TITLE_H + (ri + 1) * SUBPLOT_SIZE, ci * SUBPLOT_SIZE:(ci + 1) * SUBPLOT_SIZE] = res
        out.write(img)
        last_img = img

    for _ in range(FPS * 3):
        out.write(last_img)

    title = np.zeros((video_size[1], video_size[0], 3), dtype=np.uint8)
    cv2.putText(title, "FINAL RANKINGS", (video_size[0] // 2 - 200, 150), 0, 1.8, (255, 255, 255), 4)
    for i, (name, rank) in enumerate(sorted(rankings_final.items(), key=lambda x: x[1])):
        cv2.putText(title, f"#{rank} {name}", (video_size[0] // 2 - 150, 250 + i * 50), 0, 1.1, (200, 200, 200), 2)
    for _ in range(FPS * 5):
        out.write(title)

    out.release()
    return filename


def display_video(file_path: str) -> HTML:
    encoded = base64.b64encode(io.open(file_path, "rb").read())
    return HTML(
        f'<video controls width="800">'
        f'<source src="data:video/mp4;base64,{encoded.decode("ascii")}" type="video/mp4" />'
        f"</video>"
    )
