# Maze Solvers

Benchmark 9 classical pathfinding algorithms across hundreds of randomly generated mazes to find which ones explore most efficiently on average.

## Algorithms

| Algorithm | Optimal path? | Strategy |
|---|---|---|
| A* | Yes | `f = g + h` (Manhattan heuristic) |
| Dijkstra | Yes | Uniform cost |
| Greedy Best-First | No | Pure heuristic priority |
| BFS | Yes | Level-by-level |
| DFS | No | Deep-first, non-optimal |
| Bidirectional BFS | Yes | Simultaneous forward/backward |
| Weighted A* (W=3) | No | Over-emphasised heuristic |
| Recursive Backtrack | No | Randomised DFS |
| Wall Follower | No | Right-hand rule |

## Install

```bash
pip install -e .
```

## Usage

Without installing:

```bash
python benchmark.py
python benchmark.py --trials 500 --size 30 --seed 42 --log results.txt
```

Or via the installed CLI (after `pip install -e .`):

```bash
maze-bench
maze-bench --trials 500 --size 30 --seed 42 --log results.txt
```

Both entry points run trials in parallel across all CPU cores by default. Use `--workers N` to control the pool size, or `--workers 1` to run serially (useful for small trial counts where process startup overhead dominates).

Example output:

```
Maze Benchmark  |  100 trials  |  20x20 maze
------------------------------------------------------------------------------
Rank  Algorithm              Mean Steps  Med Steps  Mean Path   Win%  Success%
------------------------------------------------------------------------------
1     Greedy Best-First           113.5      106.5       61.8  49.0     100.0
...
```

**Mean Steps** — average number of cells popped from the frontier before reaching the goal (lower = more efficient exploration).  
**Win%** — fraction of mazes where this algorithm had the fewest exploration steps.  
**Mean Path** — average path length; only optimal algorithms (BFS, A*, Dijkstra, Bidirectional BFS) will consistently match the true shortest path.

## Development

```bash
pip install -e ".[test]"
pytest -q
```

## Visualization (optional)

The notebook `maze_solvers_competition.ipynb` renders a side-by-side MP4 of all solvers on one maze. For ad-hoc use from Python, see `src/maze_solvers/visualize.py` (requires `pip install -e ".[viz]"`).
