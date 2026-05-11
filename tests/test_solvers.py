import random
import pytest

from maze_solvers.maze import generate_maze, build_valid_moves
from maze_solvers.solvers import (
    SOLVERS, BFSSolver, AStarSolver, DijkstraSolver, BidirectionalBFSSolver,
    WallFollowerSolver,
)


ROWS, COLS = 10, 10
START = (0, 0)
GOAL = (ROWS - 1, COLS - 1)
SEEDS = list(range(10))

SOLVERS_NO_WF = [(cls, name) for cls, name in SOLVERS if cls is not WallFollowerSolver]


def _make_moves(seed, rows=ROWS, cols=COLS):
    grid = generate_maze(rows, cols, rng=random.Random(seed))
    return build_valid_moves(grid, rows, cols)


def _run(cls, name, start, goal, moves, seed=0):
    random.seed(seed)
    solver = cls(name, start, goal, moves)
    path = None
    for state in solver.solve_generator():
        if state["p"] is not None:
            path = state["p"]
    return path


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


# ---------------------------------------------------------------------------
# Stronger property tests
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("seed", SEEDS)
@pytest.mark.parametrize("cls,name", SOLVERS)
def test_solvers_solve_across_seeds(cls, name, seed):
    """Every solver finds a valid path on 10 different mazes."""
    moves = _make_moves(seed)
    path = _run(cls, name, START, GOAL, moves, seed=seed)
    assert path is not None, f"{name} did not find a path on seed {seed}"
    assert path[0] == START
    assert path[-1] == GOAL


@pytest.mark.parametrize("seed", SEEDS)
@pytest.mark.parametrize("cls,name", SOLVERS)
def test_path_is_contiguous(cls, name, seed):
    """Every step in the returned path must be an adjacent cell (no wall crossings)."""
    moves = _make_moves(seed)
    path = _run(cls, name, START, GOAL, moves, seed=seed)
    assert path is not None, f"{name} returned no path on seed {seed}"
    for i in range(len(path) - 1):
        a, b = path[i], path[i + 1]
        assert b in moves[a[0]][a[1]], (
            f"{name} seed {seed}: step {i} goes {a}->{b} but that move is not valid"
        )


@pytest.mark.parametrize("seed", SEEDS)
def test_all_non_wf_solvers_return_identical_path_on_perfect_maze(seed):
    """On a perfect maze (spanning tree), every non-wall-follower solver must return
    the unique simple start-to-goal path — identical cell sequence, not just equal length."""
    moves = _make_moves(seed)
    paths = {}
    for cls, name in SOLVERS_NO_WF:
        paths[name] = _run(cls, name, START, GOAL, moves, seed=seed)
        assert paths[name] is not None, f"{name} returned no path on seed {seed}"

    reference_name, reference_path = next(iter(paths.items()))
    for name, path in paths.items():
        assert path == reference_path, (
            f"Paths diverge on seed {seed}: {reference_name} vs {name}\n"
            f"  {reference_name}: {reference_path}\n"
            f"  {name}: {path}"
        )


@pytest.mark.parametrize("cls,name", SOLVERS)
def test_start_equals_goal(cls, name):
    """When start == goal every solver should return a single-cell path immediately."""
    if cls is BidirectionalBFSSolver:
        pytest.xfail("known: BidirectionalBFS doesn't handle start==goal — returns spurious multi-cell path")
    moves = _make_moves(seed=0)
    cell = (0, 0)
    path = _run(cls, name, cell, cell, moves, seed=0)
    assert path is not None, f"{name} returned no path for start==goal"
    assert path == [cell], f"{name} returned {path!r} instead of [{cell!r}] for start==goal"


@pytest.mark.parametrize("seed", SEEDS)
def test_wall_follower_trail_valid(seed):
    """Wall follower is held to a weaker contract: must reach the goal and every
    step in its trail (which may revisit cells) must be a valid adjacency."""
    moves = _make_moves(seed)
    path = _run(WallFollowerSolver, "Wall Follower", START, GOAL, moves, seed=seed)
    assert path is not None, f"Wall Follower did not reach goal on seed {seed}"
    assert path[0] == START
    assert path[-1] == GOAL
    for i in range(len(path) - 1):
        a, b = path[i], path[i + 1]
        assert b in moves[a[0]][a[1]], (
            f"Wall Follower seed {seed}: step {i} goes {a}->{b} but that move is not valid"
        )
