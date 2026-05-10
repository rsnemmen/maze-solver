import heapq
import numpy as np
from .base import SolverBase


class AStarSolver(SolverBase):
    def solve_generator(self):
        frontier = [(0, 0, self.start)]
        came_from = {self.start: None}
        cost = {self.start: 0}
        visited = np.zeros((self.rows, self.cols), bool)
        counter = 1
        while frontier:
            _, _, cur = heapq.heappop(frontier)
            visited[cur] = True
            if cur == self.goal:
                yield {'v': visited.copy(), 'p': self._reconstruct(came_from)}
                return
            yield {'v': visited.copy(), 'p': None}
            for nb in self.moves[cur[0]][cur[1]]:
                nc = cost[cur] + 1
                if nb not in cost or nc < cost[nb]:
                    cost[nb] = nc
                    priority = nc + abs(nb[0] - self.goal[0]) + abs(nb[1] - self.goal[1])
                    heapq.heappush(frontier, (priority, counter, nb))
                    came_from[nb] = cur
                    counter += 1


class WeightedAStarSolver(SolverBase):
    W = 3.0

    def solve_generator(self):
        frontier = [(0, self.start)]
        came_from = {self.start: None}
        cost = {self.start: 0}
        visited = np.zeros((self.rows, self.cols), bool)
        while frontier:
            _, cur = heapq.heappop(frontier)
            visited[cur] = True
            if cur == self.goal:
                yield {'v': visited.copy(), 'p': self._reconstruct(came_from)}
                return
            yield {'v': visited.copy(), 'p': None}
            for nb in self.moves[cur[0]][cur[1]]:
                nc = cost[cur] + 1
                if nb not in cost or nc < cost[nb]:
                    cost[nb] = nc
                    h = abs(nb[0] - self.goal[0]) + abs(nb[1] - self.goal[1])
                    heapq.heappush(frontier, (nc + self.W * h, nb))
                    came_from[nb] = cur
