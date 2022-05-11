import random
import enum
import resource
from collections import deque
from maze import *
from dataStructures import DSU


resource.setrlimit(resource.RLIMIT_STACK,
                   (resource.RLIM_INFINITY, resource.RLIM_INFINITY))


class BuilderGenerator(enum.Enum):
    Cruscal = 'MST generator'
    DFS = 'DFS generator'


class MazeBuilder:
    def __init__(self):
        pass

    def __str__(self):
        raise "Error: generator not selected"

    def build(self, height: int, width: int):
        return Maze(height, width)


class MazeCruscalBuilder(MazeBuilder):
    def __init__(self):
        pass

    def __str__(self):
        return BuilderGenerator.Cruscal.value

    def build(self, height: int, width: int):
        maze = Maze(height, width)
        walls = list(maze.walls.items())
        random.shuffle(walls)
        dsu = DSU(height * width)
        for wall in walls:
            first_cell, second_cell = Cell.get_two_cells(wall[0])
            if dsu.merge(*maze.convert_cells_to_int(first_cell, second_cell)):
                maze.set_wall(first_cell, second_cell, Wall(False))
        return maze


class MazeDFSBuilder(MazeBuilder):
    def __init__(self):
        pass

    def __str__(self):
        return BuilderGenerator.DFS.value

    def build(self, height: int, width: int):
        maze = Maze(height, width)
        dq = deque()
        cells = [cell for cell in maze.get_cells()]
        random.shuffle(cells)
        dsu = DSU(height * width)
        for cell in cells:
            dq.append(cell)
            while dq:
                first_cell = dq.pop()
                adj_cells = [tmp for tmp in maze.adjacent_cells(first_cell)]
                random.shuffle(adj_cells)
                for second_cell in adj_cells:
                    if dsu.merge(*maze.convert_cells_to_int(first_cell,
                                                            second_cell)):
                        maze.set_wall(first_cell, second_cell, Wall(False))
                        dq.append(second_cell)
        return maze
