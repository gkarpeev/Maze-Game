import enum
import pygame
from maze import *


class GraphicsType(enum.Enum):
    Console = 'console'
    Game = 'game'


class Graphics:
    def __init__(self):
        pass

    def __str__(self):
        raise "Error: graphics not selected"

    def draw_maze(self, maze: Maze):
        pass

    def draw_path(self, maze: Maze, path):
        pass

    def draw_visited_cells(self, maze: Maze, visited_cells):
        pass


class ConsoleGraphics:
    painted_sym = '*'
    start_sym = 'S'
    finish_sym = 'F'

    def __init__(self, maze):
        self.maze = maze

    def __str__(self):
        return GraphicsType.Console.value

    def work(self, solver):
        self.start_cell = Cell(0, 0)
        self.finish_cell = Cell(self.maze.get_height() - 1,
                                self.maze.get_width() - 1)

        self.start_cell.x, self.start_cell.y = map(int,
                                                   input(
                                                       'Please, \
                                                        write Start point\n'
                                                    ).split())
        self.finish_cell.x, self.finish_cell.y = map(int,
                                                     input(
                                                        'Please, \
                                                         write End point\n'
                                                     ).split())

        path, visited_cells = solver.solve(self.maze, self.start_cell,
                                           self.finish_cell)
        self.draw_path(self.maze, path)

        view_visited_cells = input('Do you want to see visited cells? [y/n] ')
        if view_visited_cells == 'y':
            self.draw_visited_cells(self.maze, visited_cells)

    def draw_maze(self, maze: Maze):
        print(maze)

    def draw_path(self, maze: Maze, path):
        maze_str = str(maze)
        if maze_str.endswith('\n'):
            maze_str = maze_str[:-1]
        result = [list(s) for s in maze_str.split('\n')]
        for i in range(len(path)):
            cell = path[i]
            pos_of_cell = cell * 2 + Cell(1, 1)
            if i == 0:
                result[pos_of_cell.x][pos_of_cell.y] = self.start_sym
            elif i == len(path) - 1:
                result[pos_of_cell.x][pos_of_cell.y] = self.finish_sym
            else:
                result[pos_of_cell.x][pos_of_cell.y] = self.painted_sym
        s = ""
        for i in result:
            for j in i:
                s += j
            s += '\n'
        print(s)

    def draw_visited_cells(self, maze: Maze, visited_cells):
        maze_str = str(maze)
        if maze_str.endswith('\n'):
            maze_str = maze_str[:-1]
        result = [list(s) for s in maze_str.split('\n')]
        for cell in visited_cells:
            pos_of_cell = cell * 2 + Cell(1, 1)
            result[pos_of_cell.x][pos_of_cell.y] = self.painted_sym
        s = ""
        for i in result:
            for j in i:
                s += j
            s += '\n'
        print(s)


class Color(enum.Enum):
    Background = pygame.Color('black')
    Cell = pygame.Color('black')
    Wall = pygame.Color('darkorange')
    Path_cell = pygame.Color('dark violet')
    Start_cell = pygame.Color('dark green')
    Finish_cell = pygame.Color('red')
    Visited_cell = pygame.Color('medium violet red')


class GameGraphics:
    FPS = 30
    HEIGHT_INDENT = 30
    WIDTH_INDENT = 30
    start_cell = Cell(-1, -1)
    finish_cell = Cell(-1, -1)

    def __init__(self, maze: Maze):
        self.maze = maze
        self.tile = min(30, (1200 - 2 * self.WIDTH_INDENT) // maze.width,
                        (900 - 2 * self.HEIGHT_INDENT) // maze.height)
        self.width = min(1200,
                         maze.width * self.tile + 2 * self.WIDTH_INDENT) + 3
        self.height = min(900,
                          maze.height * self.tile + 2 * self.HEIGHT_INDENT) + 3

    def convert_to_cell(self, cell):
        cell.x -= self.WIDTH_INDENT
        cell.y -= self.HEIGHT_INDENT
        if cell.x < 0 or cell.x > self.maze.width * self.tile:
            return Cell(-1, -1)
        if cell.y < 0 or cell.y > self.maze.height * self.tile:
            return Cell(-1, -1)
        return Cell(cell.y // self.tile, cell.x // self.tile)

    def work(self, solver):
        pygame.init()
        self.window = pygame.display.set_mode((self.width, self.height))
        cell_chosen_type = 0
        while True:
            self.window.fill(Color.Background.value)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        pos = pygame.mouse.get_pos()
                        cell = Cell(pos[0], pos[1])
                        if cell_chosen_type % 2 == 0:
                            self.start_cell = self.convert_to_cell(cell)
                        else:
                            self.finish_cell = self.convert_to_cell(cell)
                        cell_chosen_type += 1

            if self.start_cell != Cell(-1, -1) and \
               self.finish_cell != Cell(-1, -1):
                path, vis = solver.solve(self.maze,
                                         self.start_cell, self.finish_cell)
                self.draw_visited_cells(path, vis)
            else:
                self.draw_maze()

            pygame.display.flip()
            pygame.time.Clock().tick(self.FPS)

    def __str__(self):
        return GraphicsType.Game.value

    def draw_cell(self, cell: Cell, color):
        x, y = cell.x * self.tile + self.HEIGHT_INDENT,\
               cell.y * self.tile + self.WIDTH_INDENT
        pygame.draw.rect(self.window, color, (y, x, self.tile, self.tile))

    def draw_wall(self, first_cell: Cell, second_cell: Cell):
        if not self.maze.is_wall_between_cells(first_cell, second_cell):
            return
        if Maze.is_horizontal_line(first_cell, second_cell):
            if first_cell.x > second_cell.x:
                first_cell, second_cell = second_cell, first_cell
            x, y = second_cell.x * self.tile + self.HEIGHT_INDENT, \
                second_cell.y * self.tile + self.WIDTH_INDENT
            pygame.draw.line(self.window, Color.Wall.value,
                             (y, x), (y + self.tile, x), 3)
        else:
            if first_cell.y > second_cell.y:
                first_cell, second_cell = second_cell, first_cell
            x, y = second_cell.x * self.tile + self.HEIGHT_INDENT, \
                second_cell.y * self.tile + self.WIDTH_INDENT
            pygame.draw.line(self.window, Color.Wall.value,
                             (y, x), (y, x + self.tile), 3)

    def draw_walls(self):
        for first_cell in self.maze.get_cells():
            for second_cell in self.maze.adjacent_cells(first_cell):
                self.draw_wall(first_cell, second_cell)

    def draw_cells(self, cells, color):
        for cell in cells:
            self.draw_cell(cell, color)

    def draw_finish_and_start_cells(self):
        if self.start_cell != Cell(-1, -1):
            self.draw_cell(self.start_cell, Color.Start_cell.value)
        if self.finish_cell != Cell(-1, -1):
            self.draw_cell(self.finish_cell, Color.Finish_cell.value)

    def draw_maze(self):
        self.draw_cells(self.maze.get_cells(), Color.Cell.value)
        self.draw_finish_and_start_cells()
        self.draw_walls()

    def draw_path(self, path):
        self.draw_cells(self.maze.get_cells(), Color.Cell.value)
        self.draw_cells(path, Color.Path_cell.value)
        self.draw_finish_and_start_cells()
        self.draw_walls()

    def draw_visited_cells(self, path, visited_cells):
        self.draw_cells(self.maze.get_cells(), Color.Cell.value)
        self.draw_cells(visited_cells, Color.Visited_cell.value)
        self.draw_cells(path, Color.Path_cell.value)
        self.draw_finish_and_start_cells()
        self.draw_walls()
