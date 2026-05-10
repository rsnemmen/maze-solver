import numpy as np
from .base import SolverBase


class WallFollowerSolver(SolverBase):
    def solve_generator(self):
        dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        cur = self.start
        facing = (0, 1)
        path = [cur]
        visited = np.zeros((self.rows, self.cols), bool)
        safety_limit = max(2500, self.rows * self.cols * 4)

        while cur != self.goal:
            visited[cur] = True
            yield {'v': visited.copy(), 'p': None}
            idx = dirs.index(facing)
            moved = False
            for i in range(-1, 3):
                d = dirs[(idx + i) % 4]
                nxt = (cur[0] + d[0], cur[1] + d[1])
                if nxt in self.moves[cur[0]][cur[1]]:
                    cur, facing = nxt, d
                    path.append(cur)
                    moved = True
                    break
            if not moved or len(path) > safety_limit:
                break

        visited[cur] = True
        yield {'v': visited.copy(), 'p': path if cur == self.goal else None}
