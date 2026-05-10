import random
import numpy as np
import pytest

from maze_solvers.maze import generate_maze, build_valid_moves


ROWS, COLS = 15, 15
START = (0, 0)
GOAL = (ROWS - 1, COLS - 1)


@pytest.fixture(scope="module")
def maze():
    return generate_maze(ROWS, COLS, rng=random.Random(42))


def test_start_cell_is_open(maze):
    assert maze[2 * START[0] + 1, 2 * START[1] + 1] == 1


def test_goal_cell_is_open(maze):
    assert maze[2 * GOAL[0] + 1, 2 * GOAL[1] + 1] == 1


def test_grid_shape(maze):
    assert maze.shape == (2 * ROWS + 1, 2 * COLS + 1)


def test_maze_is_connected(maze):
    """BFS from start must reach goal, proving the maze is fully connected."""
    from collections import deque
    moves = build_valid_moves(maze, ROWS, COLS)
    visited = set()
    queue = deque([START])
    visited.add(START)
    while queue:
        cur = queue.popleft()
        if cur == GOAL:
            return
        for nb in moves[cur[0]][cur[1]]:
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
    pytest.fail("BFS did not reach GOAL — maze is not fully connected")


def test_reproducibility():
    g1 = generate_maze(10, 10, rng=random.Random(7))
    g2 = generate_maze(10, 10, rng=random.Random(7))
    assert np.array_equal(g1, g2)
