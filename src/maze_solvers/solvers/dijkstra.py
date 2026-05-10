import heapq
import numpy as np
from .base import SolverBase


class DijkstraSolver(SolverBase):
    def solve_generator(self):
        frontier = [(0, self.start)]
        came_from = {self.start: None}
        cost = {self.start: 0}
        visited = np.zeros((self.rows, self.cols), bool)
        while frontier:
            c, cur = heapq.heappop(frontier)
            visited[cur] = True
            if cur == self.goal:
                yield {'v': visited.copy(), 'p': self._reconstruct(came_from)}
                return
            yield {'v': visited.copy(), 'p': None}
            for nb in self.moves[cur[0]][cur[1]]:
                nc = c + 1
                if nb not in cost or nc < cost[nb]:
                    cost[nb] = nc
                    heapq.heappush(frontier, (nc, nb))
                    came_from[nb] = cur
