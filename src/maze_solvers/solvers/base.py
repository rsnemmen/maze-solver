from typing import Generator
import numpy as np


class SolverBase:
    """
    Base class for all maze solvers.

    Subclasses implement solve_generator(), a generator that yields one dict per
    exploration step:
        {'v': bool_ndarray, 'p': list[tuple] | None}
    'v' is the visited-cells mask; 'p' is the path from start to goal once found,
    None until then. The generator returns (StopIteration) when done.
    """

    def __init__(
        self,
        name: str,
        start: tuple[int, int],
        goal: tuple[int, int],
        moves: list[list[list[tuple[int, int]]]],
    ) -> None:
        self.name = name
        self.start = start
        self.goal = goal
        self.moves = moves
        self.rows = len(moves)
        self.cols = len(moves[0])

    def _reconstruct(self, came_from: dict) -> list[tuple[int, int]]:
        path, curr = [], self.goal
        while curr is not None:
            path.append(curr)
            curr = came_from.get(curr)
        return path[::-1]

    def solve_generator(self) -> Generator[dict, None, None]:
        raise NotImplementedError
