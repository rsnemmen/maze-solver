import random as _random
import numpy as np


def generate_maze(rows: int, cols: int, rng: _random.Random | None = None) -> np.ndarray:
    """Perfect maze via randomized DFS. Grid is (2*rows+1) x (2*cols+1); cells at odd coords, walls at even."""
    if rng is None:
        rng = _random.Random()
    start = (0, 0)
    grid = np.zeros((2 * rows + 1, 2 * cols + 1), dtype=np.uint8)
    stack = [start]
    visited = np.zeros((rows, cols), dtype=bool)
    visited[start] = True
    grid[2 * start[0] + 1, 2 * start[1] + 1] = 1
    dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while stack:
        r, c = stack[-1]
        neighs = [
            (r + dr, c + dc, dr, dc)
            for dr, dc in dirs
            if 0 <= r + dr < rows and 0 <= c + dc < cols and not visited[r + dr, c + dc]
        ]
        if neighs:
            nr, nc, dr, dc = rng.choice(neighs)
            grid[2 * r + 1 + dr, 2 * c + 1 + dc] = 1
            grid[2 * nr + 1, 2 * nc + 1] = 1
            visited[nr, nc] = True
            stack.append((nr, nc))
        else:
            stack.pop()
    return grid


def build_valid_moves(grid: np.ndarray, rows: int, cols: int) -> list[list[list[tuple[int, int]]]]:
    """Pre-compute valid neighbour moves for each cell."""
    moves: list[list[list[tuple[int, int]]]] = [[[] for _ in range(cols)] for _ in range(rows)]
    for r in range(rows):
        for c in range(cols):
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                if 0 <= r + dr < rows and 0 <= c + dc < cols and grid[2 * r + 1 + dr, 2 * c + 1 + dc] == 1:
                    moves[r][c].append((r + dr, c + dc))
    return moves
