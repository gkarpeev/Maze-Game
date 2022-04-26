import enum
from collections import deque
import resource
from maze import *
from dataStructures import PathHistoryStorage
from queue import PriorityQueue


resource.setrlimit(resource.RLIMIT_STACK,
                   (resource.RLIM_INFINITY, resource.RLIM_INFINITY))


class SolverAlgorithm(enum.Enum):
    BFS = 'BFS solver'
    AStar = 'AStar solver'


class MazeSolver:
    def __init__(self):
        pass

    def __str__(self):
        raise "Error: algorithm not selected"

    def solve(self, start: Cell, finish: Cell):
        raise "Error: algorithm not selected"


class MazeSolverBFS:
    def __init__(self):
        pass

    def __str__(self):
        return SolverAlgorithm.BFS.value

    def solve(self, maze: Maze, start: Cell, finish: Cell):
        if start == finish:
            return [start]
        dq = deque()
        storage = PathHistoryStorage(maze.get_height(), maze.get_width())
        dq.append(start)
        storage.add_visited_cell(start, start)
        while dq:
            cell = dq.popleft()
            for next_cell in maze.available_adjacent_cells(cell):
                if storage.is_visited(next_cell):
                    continue
                dq.append(next_cell)
                storage.add_visited_cell(cell, next_cell)
                if next_cell == finish:
                    dq.clear()
                    break
        return storage.get_path(start, finish), storage.get_visited_cells()


class MazeSolverAStar:
    def __init__(self):
        pass

    def __str__(self):
        return SolverAlgorithm.AStar.value

    def heuristic_function(cell: Cell, finish: Cell):
        return abs((finish - cell).x) + abs((finish - cell).y)

    def distance_function(distance: int, cell: Cell, finish: Cell):
        return distance + MazeSolverAStar.heuristic_function(cell, finish)

    def solve(self, maze: Maze, start: Cell, finish: Cell):
        storage = PathHistoryStorage(maze.get_height(), maze.get_width())
        q = PriorityQueue()
        q.put((0, 0, start, start))
        while q:
            heuristic_distance, real_distance, previous_cell, cell = q.get()
            if storage.is_visited(cell):
                continue
            storage.add_visited_cell(previous_cell, cell)
            if cell == finish:
                break
            for next_cell in maze.available_adjacent_cells(cell):
                if storage.is_visited(next_cell):
                    continue
                q.put((MazeSolverAStar.distance_function(
                        real_distance + 1, next_cell, finish),
                       real_distance + 1, cell, next_cell))
        return storage.get_path(start, finish), storage.get_visited_cells()
