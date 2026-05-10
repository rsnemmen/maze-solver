from .base import SolverBase
from .astar import AStarSolver, WeightedAStarSolver
from .dijkstra import DijkstraSolver
from .greedy import GreedySolver
from .bfs import BFSSolver, BidirectionalBFSSolver
from .dfs import DFSSolver, RecursiveBacktrackSolver
from .wall_follower import WallFollowerSolver

SOLVERS: list[tuple[type[SolverBase], str]] = [
    (AStarSolver, "A*"),
    (DijkstraSolver, "Dijkstra"),
    (GreedySolver, "Greedy Best-First"),
    (BFSSolver, "BFS"),
    (DFSSolver, "DFS"),
    (BidirectionalBFSSolver, "Bidirectional BFS"),
    (WeightedAStarSolver, "Weighted A*"),
    (RecursiveBacktrackSolver, "Recursive Backtrack"),
    (WallFollowerSolver, "Wall Follower"),
]

__all__ = [
    "SolverBase",
    "AStarSolver",
    "WeightedAStarSolver",
    "DijkstraSolver",
    "GreedySolver",
    "BFSSolver",
    "BidirectionalBFSSolver",
    "DFSSolver",
    "RecursiveBacktrackSolver",
    "WallFollowerSolver",
    "SOLVERS",
]
