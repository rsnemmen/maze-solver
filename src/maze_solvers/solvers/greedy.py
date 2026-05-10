import heapq
import random
import numpy as np
from .base import SolverBase


class GreedySolver(SolverBase):
    def solve_generator(self):
        frontier = [(0, random.random(), self.start)]
        came_from = {self.start: None}
        visited = np.zeros((self.rows, self.cols), bool)
        while frontier:
            _, _, cur = heapq.heappop(frontier)
            visited[cur] = True
            if cur == self.goal:
                yield {'v': visited.copy(), 'p': self._reconstruct(came_from)}
                return
            yield {'v': visited.copy(), 'p': None}
            for nb in self.moves[cur[0]][cur[1]]:
                if nb not in came_from:
                    h = abs(nb[0] - self.goal[0]) + abs(nb[1] - self.goal[1])
                    heapq.heappush(frontier, (h, random.random(), nb))
                    came_from[nb] = cur
