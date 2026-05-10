# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A maze-solving algorithm benchmarking project. Currently a single Jupyter notebook (`maze_solvers_competition.ipynb`) that generates a random maze and visualizes 9 pathfinding algorithms side-by-side, outputting an MP4 video. The long-term goal is a standalone Python benchmarking tool that averages rankings across many generated mazes.

## Commands

```bash
# Install the package (core benchmark, no OpenCV)
pip install -e .

# Install with video-rendering support
pip install -e ".[viz]"

# Install with test dependencies
pip install -e ".[test]"

# Run the benchmark (100 trials, 20x20 maze, writes benchmark_results.txt)
maze-bench

# Custom run
maze-bench --trials 500 --size 30 --seed 42 --log results.txt

# Run tests
pytest -q

# Run the notebook interactively (one-off visualization)
jupyter lab maze_solvers_competition.ipynb

# Execute notebook headlessly (produces maze_showdown_mugambi.mp4)
jupyter nbconvert --to notebook --execute maze_solvers_competition.ipynb
```

## Jupyter Notebook Inspection

When you need to read or inspect Jupyter notebooks (`.ipynb` files) in this project, **do not** read the `.ipynb` files directly. They are JSON and difficult to parse meaningfully.

Instead, follow this workflow:

1. First, check if a markdown version already exists (e.g., `notebook.md` for `notebook.ipynb`).
2. If no markdown version exists, convert the notebook to markdown using: `jupyter nbconvert --to markdown <notebook>.ipynb --ExtractOutputPreprocessor.enabled=False`.
3. If `jupyter nbconvert` is not available, try `jupytext --to md <notebook>.ipynb` as a fallback.
4. Read and inspect the resulting `.md` file.

Notes:
- Do **not** commit generated `.md` files unless explicitly asked to.
- When summarizing a notebook, reference cells by their order (e.g., "In cell 3…") so the user can locate them easily.
- If a notebook has been recently modified, regenerate the markdown version before reading it to ensure it's up to date.

## Architecture

### Grid Representation

The maze uses a `(2n+1) × (2n+1)` pixel grid where `n = MAZE_SIZE`. Cells occupy odd-indexed coordinates; walls between them occupy even-indexed coordinates. A value of `1` means open (passable), `0` means wall. This lets wall-removal be a single array assignment.

### Solver Protocol

All 9 solvers inherit from `SolverBase` and implement `solve_generator()` as a Python **generator** that yields dicts of the form `{'v': visited_bool_array, 'p': path_or_None}` at each exploration step. The path is `None` until the goal is found, then it's a list of `(row, col)` tuples from start to goal. This single protocol handles both visualization (frame sampling) and performance ranking (total steps = `len(list(solver.solve_generator()))`).

`build_valid_moves()` pre-computes a `rows × cols` list-of-lists of valid neighbors and is shared across all solvers to avoid redundant wall checks during search.

### Ranking Metric

Algorithms are ranked by **number of generator steps** (exploration steps to reach the goal), not wall-clock time. Fewer steps = higher rank.

### Video Rendering

`render_video()` uses OpenCV to composite a 3×3 grid of 512×512 subplots into a `1536×(1536+100)` MP4 at 12 FPS. Each subplot samples frames from the solver's generator (`full_gen[::2]`), overlays the final path as a green polyline, and labels the algorithm's rank once solved.

### Solvers Implemented

| Algorithm | Strategy |
|---|---|
| A* | `f = g + h` (Manhattan heuristic) |
| Dijkstra | Uniform cost (equivalent to BFS on unit-weight grid) |
| Greedy Best-First | Pure heuristic priority |
| BFS | FIFO queue, guaranteed shortest path |
| DFS | LIFO stack, non-optimal |
| Bidirectional BFS | Simultaneous forward/backward BFS |
| Weighted A* | `f = g + W*h` with W=3 (faster, non-optimal) |
| Recursive Backtrack | Randomized DFS with explicit stack |
| Wall Follower | Right-hand rule; may not find shortest path |
