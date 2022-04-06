import resource
from maze import *


resource.setrlimit(resource.RLIMIT_STACK, (resource.RLIM_INFINITY, resource.RLIM_INFINITY))


class DSU:
    parent = []
    rank = []
    def __init__(self, n: int):
        self.parent = [i for i in range(n)]
        self.rank = [0] * n
    
    def get_parent(self, v: int):
        if self.parent[v] == v:
            return v
        self.parent[v] = self.get_parent(self.parent[v])
        return self.parent[v]

    def merged(self, v: int, u: int):
        v = self.get_parent(v)
        u = self.get_parent(u)
        return v == u

    def merge(self, v: int, u: int):
        if v == -1 or u == -1:
            return False
        v = self.get_parent(v)
        u = self.get_parent(u)
        if self.merged(u, v):
            return False
        if self.rank[v] < self.rank[u]:
            v, u = u, v
        self.parent[u] = v
        if self.rank[u] == self.rank[v]:
            self.rank[v] += 1
        return True


class PathHistoryStorage:
    previous = [[]]
    visited = [[]]
    height = 0
    width = 0

    def __init__(self, height: int, width: int):
        self.previous = [[Cell(x, y) for y in range(width)] for x in range(height)]
        self.visited = [[False for y in range(width)] for x in range(height)]
        self.height = height
        self.width = width
    
    def good_cell(self, cell):
        return 0 <= cell.x < self.height and 0 <= cell.y < self.width

    def get_path(self, start: Cell, finish: Cell):
        path = []
        while len(path) <= self.height * self.width:
            path.append(finish)
            if start == finish:
                break
            finish = self.previous[finish.x][finish.y]
        if len(path) > self.height * self.width:
            # raise "Error: no path founded"
            return []
        return path[::-1]
    
    def is_visited(self, cell: Cell):
        return self.visited[cell.x][cell.y]

    def get_visited_cells(self):
        result = []
        for i in range(self.height):
            for j in range(self.width):
                cell = Cell(i, j)
                if self.is_visited(cell):
                    result.append(cell)
        return result
    
    def add_visited_cell(self, previous_cell: Cell, cell: Cell):
        self.visited[cell.x][cell.y] = True
        self.previous[cell.x][cell.y] = previous_cell
