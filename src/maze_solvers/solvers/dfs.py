import random
import numpy as np
from .base import SolverBase


class DFSSolver(SolverBase):
    def solve_generator(self):
        stack = [self.start]
        came_from = {self.start: None}
        visited = np.zeros((self.rows, self.cols), bool)
        while stack:
            cur = stack.pop()
            if visited[cur]:
                continue
            visited[cur] = True
            if cur == self.goal:
                yield {'v': visited.copy(), 'p': self._reconstruct(came_from)}
                return
            yield {'v': visited.copy(), 'p': None}
            for nb in self.moves[cur[0]][cur[1]]:
                if not visited[nb]:
                    came_from[nb] = cur
                    stack.append(nb)


class RecursiveBacktrackSolver(SolverBase):
    def solve_generator(self):
        path = [self.start]
        came_from = {self.start: None}
        visited = np.zeros((self.rows, self.cols), bool)
        while path:
            cur = path[-1]
            visited[cur] = True
            if cur == self.goal:
                yield {'v': visited.copy(), 'p': self._reconstruct(came_from)}
                return
            yield {'v': visited.copy(), 'p': None}
            unvisited = [nb for nb in self.moves[cur[0]][cur[1]] if not visited[nb]]
            if unvisited:
                nxt = random.choice(unvisited)
                came_from[nxt] = cur
                path.append(nxt)
            else:
                path.pop()
