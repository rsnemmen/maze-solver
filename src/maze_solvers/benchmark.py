from __future__ import annotations
import random
import statistics
from dataclasses import dataclass

from .maze import generate_maze, build_valid_moves
from .solvers import SOLVERS


@dataclass
class TrialResult:
    solver_name: str
    steps: int
    path_length: int
    solved: bool


@dataclass
class SolverStats:
    name: str
    mean_steps: float
    median_steps: float
    mean_path_length: float
    success_rate: float
    win_rate: float


def run_trial(maze_size: int, seed: int) -> list[TrialResult]:
    """Run all solvers on one randomly generated maze. Seed controls both maze generation and randomized solvers."""
    random.seed(seed)
    rng = random.Random(seed)
    start = (0, 0)
    goal = (maze_size - 1, maze_size - 1)
    grid = generate_maze(maze_size, maze_size, rng=rng)
    moves = build_valid_moves(grid, maze_size, maze_size)

    results: list[TrialResult] = []
    for cls, name in SOLVERS:
        solver = cls(name, start, goal, moves)
        steps = 0
        path: list | None = None
        for state in solver.solve_generator():
            steps += 1
            if state["p"] is not None:
                path = state["p"]
        results.append(TrialResult(
            solver_name=name,
            steps=steps,
            path_length=len(path) if path else 0,
            solved=path is not None,
        ))
    return results


def aggregate(all_trials: list[list[TrialResult]]) -> list[SolverStats]:
    """Aggregate per-trial results into per-solver statistics."""
    from collections import defaultdict
    by_solver: dict[str, list[TrialResult]] = defaultdict(list)
    for trial in all_trials:
        for r in trial:
            by_solver[r.solver_name].append(r)

    n_trials = len(all_trials)
    stats: list[SolverStats] = []
    for _, name in SOLVERS:
        rows = by_solver[name]
        solved_rows = [r for r in rows if r.solved]
        success_rate = len(solved_rows) / n_trials if n_trials else 0.0

        step_counts = [r.steps for r in rows]
        mean_steps = statistics.mean(step_counts) if step_counts else 0.0
        median_steps = statistics.median(step_counts) if step_counts else 0.0
        mean_path = (
            statistics.mean(r.path_length for r in solved_rows) if solved_rows else 0.0
        )

        # win = fewest steps among solvers that solved, for this trial
        wins = 0
        for trial in all_trials:
            solved_in_trial = [r for r in trial if r.solved]
            if not solved_in_trial:
                continue
            min_steps = min(r.steps for r in solved_in_trial)
            solver_row = next((r for r in trial if r.solver_name == name), None)
            if solver_row and solver_row.solved and solver_row.steps == min_steps:
                wins += 1
        win_rate = wins / n_trials if n_trials else 0.0

        stats.append(SolverStats(
            name=name,
            mean_steps=mean_steps,
            median_steps=median_steps,
            mean_path_length=mean_path,
            success_rate=success_rate,
            win_rate=win_rate,
        ))

    stats.sort(key=lambda s: s.mean_steps)
    return stats


def format_table(stats: list[SolverStats], n_trials: int, maze_size: int) -> str:
    header = (
        f"Maze Benchmark  |  {n_trials} trials  |  {maze_size}x{maze_size} maze\n"
        + "-" * 78 + "\n"
        + f"{'Rank':<5} {'Algorithm':<22} {'Mean Steps':>10} {'Med Steps':>10} "
        + f"{'Mean Path':>10} {'Win%':>6} {'Success%':>9}\n"
        + "-" * 78
    )
    rows = []
    for rank, s in enumerate(stats, 1):
        rows.append(
            f"{rank:<5} {s.name:<22} {s.mean_steps:>10.1f} {s.median_steps:>10.1f} "
            f"{s.mean_path_length:>10.1f} {s.win_rate * 100:>6.1f} {s.success_rate * 100:>9.1f}"
        )
    return header + "\n" + "\n".join(rows) + "\n"
