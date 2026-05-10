import random
import pytest

from maze_solvers.maze import generate_maze, build_valid_moves
from maze_solvers.solvers import SOLVERS, BFSSolver, AStarSolver, DijkstraSolver, BidirectionalBFSSolver


ROWS, COLS = 10, 10
START = (0, 0)
GOAL = (ROWS - 1, COLS - 1)


@pytest.fixture(scope="module")
def maze_moves():
    random.seed(0)
    grid = generate_maze(ROWS, COLS, rng=random.Random(0))
    return build_valid_moves(grid, ROWS, COLS)


@pytest.mark.parametrize("cls,name", SOLVERS)
def test_solver_finds_path(maze_moves, cls, name):
    solver = cls(name, START, GOAL, maze_moves)
    path = None
    for state in solver.solve_generator():
        if state["p"] is not None:
            path = state["p"]
    assert path is not None, f"{name} did not find a path"
    assert path[0] == START, f"{name} path does not start at START"
    assert path[-1] == GOAL, f"{name} path does not end at GOAL"


def test_optimal_solvers_agree_on_path_length(maze_moves):
    """BFS, A*, Dijkstra, and Bidirectional BFS must all find the same shortest path length."""
    lengths = {}
    for cls, name in [(BFSSolver, "BFS"), (AStarSolver, "A*"), (DijkstraSolver, "Dijkstra"), (BidirectionalBFSSolver, "Bidirectional BFS")]:
        solver = cls(name, START, GOAL, maze_moves)
        path = None
        for state in solver.solve_generator():
            if state["p"] is not None:
                path = state["p"]
        assert path is not None
        lengths[name] = len(path)

    values = list(lengths.values())
    assert all(v == values[0] for v in values), f"Optimal solvers disagree on path length: {lengths}"
