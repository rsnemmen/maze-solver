from collections import deque
import numpy as np
from .base import SolverBase


class BFSSolver(SolverBase):
    def solve_generator(self):
        queue = deque([self.start])
        came_from = {self.start: None}
        visited = np.zeros((self.rows, self.cols), bool)
        visited[self.start] = True
        while queue:
            cur = queue.popleft()
            if cur == self.goal:
                yield {'v': visited.copy(), 'p': self._reconstruct(came_from)}
                return
            yield {'v': visited.copy(), 'p': None}
            for nb in self.moves[cur[0]][cur[1]]:
                if not visited[nb]:
                    visited[nb] = True
                    came_from[nb] = cur
                    queue.append(nb)


class BidirectionalBFSSolver(SolverBase):
    def solve_generator(self):
        qs, qg = deque([self.start]), deque([self.goal])
        cfs, cfg = {self.start: None}, {self.goal: None}
        vs = np.zeros((self.rows, self.cols), bool)
        vg = np.zeros((self.rows, self.cols), bool)
        vs[self.start] = True
        vg[self.goal] = True

        while qs and qg:
            for q, v_mine, v_other, cf_mine, cf_other in [
                (qs, vs, vg, cfs, cfg),
                (qg, vg, vs, cfg, cfs),
            ]:
                if not q:
                    continue
                cur = q.popleft()
                yield {'v': vs | vg, 'p': None}
                for nb in self.moves[cur[0]][cur[1]]:
                    if not v_mine[nb]:
                        v_mine[nb] = True
                        cf_mine[nb] = cur
                        q.append(nb)
                        if v_other[nb]:
                            p1: list = []
                            c = nb
                            while c is not None:
                                p1.append(c)
                                c = cfs.get(c)
                            p1.reverse()
                            p2: list = []
                            c = cfg.get(nb)
                            while c is not None:
                                p2.append(c)
                                c = cfg.get(c)
                            yield {'v': vs | vg, 'p': p1 + p2}
                            return
