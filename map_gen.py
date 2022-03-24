import random
import sys

sys.setrecursionlimit(12000)


class DFSGenerator:
    def __init__(self, w, h):
        self.width = w
        self.height = h
        self.visited = [[0 for _ in range(self.width)] for _ in range(self.height)]
        self.map = [[1 for _ in range(self.width * 3)] for _ in range(self.height * 3)]
        self.passes = {}
        self.walls = {}
        self.GenerateMap()

    def DFS(self, coords):
        self.visited[coords[0]][coords[1]] = 1
        available_neighbours = self.GetNeighbours(coords, (self.height, self.width))

        while len(available_neighbours) > 0:
            direction = random.randint(0, len(available_neighbours) - 1)
            neighbour = available_neighbours[direction]

            if self.visited[neighbour[0]][neighbour[1]] == 0:
                self.AddPass(coords, neighbour)
                self.DFS(neighbour)

            del available_neighbours[direction]

    def GetNeighbours(self, coords, borders, condition_manager=(lambda coord: False)):
        neighbors = [(i, j) for i, j in zip([coords[0] - 1, coords[0] + 1, coords[0], coords[0]],
                                            [coords[1], coords[1], coords[1] + 1, coords[1] - 1])]
        i = 0
        while i < len(neighbors):
            coord = neighbors[i]
            if coord[0] < 0 or coord[0] >= borders[0] or coord[1] >= borders[1] or coord[1] < 0 or condition_manager(
                    coord):
                del neighbors[i]
            else:
                i += 1

        return neighbors

    def GenerateMap(self):
        self.DFS((0, 0))
        for v in self.passes.keys():
            for to in self.passes[v]:
                if v[0] == to[0]:
                    start = min(v[1], to[1])
                    end = max(v[1], to[1])
                    for i in range(1 + 3 * start, 1 + 3 * end + 1):
                        self.map[1 + 3 * v[0]][i] = 0
                elif v[1] == to[1]:
                    start = min(v[0], to[0])
                    end = max(v[0], to[0])
                    for i in range(1 + 3 * start, 1 + 3 * end + 1):
                        self.map[i][1 + 3 * v[1]] = 0

    def AddPass(self, coords, neighbour):
        if coords not in self.passes.keys():
            self.passes[coords] = []
        self.passes[coords].append(neighbour)

