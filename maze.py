import re
from collections import defaultdict


class Cell:
    x = 0
    y = 0

    def __init__(self, nx: int, ny: int):
        self.x = int(nx)
        self.y = int(ny)

    def __add__(self, other):
        return Cell(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other):
        return Cell(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scale: int):
        return Cell(self.x * scale, self.y * scale)
    
    def __truediv__(self, scale: int):
        return Cell(self.x // scale, self.y // scale)
    
    def __repr__(self):
        return '(x: {}, y: {})'.format(self.x, self.y)

    def __eq__(self, __other):
        return self.x == __other.x and self.y == __other.y

    def __ne__(self, __other):
        return not (self == __other)

    def __lt__(self, __other):
        if self.x != __other.x:
            return self.x < __other.x
        return self.y < __other.y

    def __le__(self, __other):
        return self < __other or self == __other

    def __gt__(self, __other):
        return __other < self

    def __ge__(self, __other):
        return __other <= self

    def str_to_cell(str: str):
        result = re.findall('\d{1,}', str)
        return Cell(*result)
    
    def get_two_cells(str: str):
        result = re.findall('\(.{1,}?\)', str)
        return [Cell.str_to_cell(result[0]), Cell.str_to_cell(result[1])]
    

class Wall:
    wall = True

    def __init__(self, wall: bool):
        self.wall = wall
    
    def __bool__(self):
        return self.wall

    def __repr__(self):
        return '{}'.format(self.wall)

class Maze:
    height = 10
    width = 10
    walls = defaultdict(Wall)
    move_cell = [Cell(0, 1), Cell(-1, 0), Cell(1, 0), Cell(0, -1)]
    
    horizontal_line = '─'
    vertical_line = '│'
    unset_line = ' '
    cell = ' '
    corner = '┼'
    UNICODE_BY_CONNECTIONS = {'ensw': '┼',
                              'ens': '├',
                              'enw': '┴',
                              'esw': '┬',
                              'es': '┌',
                              'en': '└',
                              'ew': '─',
                              'e': '╶',
                              'nsw': '┤',
                              'ns': '│',
                              'nw': '┘',
                              'sw': '┐',
                              's': '╷',
                              'n': '╵',
                              'w': '╴'}

    def get_height(self):
        return self.height
    
    def get_width(self):
        return self.width

    def good_cell(self, cell):
        return 0 <= cell.x < self.height and 0 <= cell.y < self.width
    
    def adjacent_cells(self, cell: Cell):
        for k in range(4):
            new_cell = cell + self.move_cell[k]
            yield new_cell
    
    def available_adjacent_cells(self, cell: Cell):
        for k in range(4):
            new_cell = cell + self.move_cell[k]
            if self.get_wall(cell, new_cell):
                continue
            yield new_cell

    def get_cells(self):
        for i in range(self.height):
            for j in range(self.width):
                yield Cell(i, j)

    def get_wall(self, first_cell: Cell, second_cell: Cell):
        return self.walls[repr(first_cell) + repr(second_cell)]

    def set_wall(self, first_cell: Cell, second_cell: Cell, wall: Wall):
        self.walls[repr(first_cell) + repr(second_cell)] = wall
        self.walls[repr(second_cell) + repr(first_cell)] = wall

    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width
        for first_cell in self.get_cells():
            for second_cell in self.adjacent_cells(first_cell):
                self.set_wall(first_cell, second_cell, Wall(True))

    def is_wall_between_cells(self, first_cell: Cell, second_cell: Cell):
        return bool(self.get_wall(first_cell, second_cell))

    def is_horizontal_line(first_cell: Cell, second_cell: Cell):
        return first_cell.y == second_cell.y

    def get_line(self, first_cell: Cell, second_cell: Cell):
        if self.is_wall_between_cells(first_cell, second_cell):
            return self.horizontal_line if Maze.is_horizontal_line(first_cell, second_cell) else self.vertical_line
        else:
            return self.unset_line
    
    def get_wall_from_line_type(self, line: str):
        return Wall(False) if line == self.unset_line else Wall(True)

    def get_maze(self):
        result = [[self.corner for i in range(2 * self.width + 1)] for j in range(2 * self.height + 1)]

        for cell in self.get_cells():
            pos_of_cell = cell * 2 + Cell(1, 1)
            result[pos_of_cell.x][pos_of_cell.y] = self.cell

        for first_cell in self.get_cells():
            pos_of_first_cell = first_cell * 2 + Cell(1, 1)
            for second_cell in self.adjacent_cells(first_cell):
                pos_of_second_cell = second_cell * 2 + Cell(1, 1)
                pos_of_wall = (pos_of_first_cell + pos_of_second_cell) / 2
                line_type = self.get_line(first_cell, second_cell)
                result[pos_of_wall.x][pos_of_wall.y] = line_type
        for x in range(2 * self.height + 1):
            for y in range(2 * self.width + 1):
                if x % 2 == 1 and y % 2 == 1:
                    continue
                pos_of_wall = Cell(x, y)
                line_type = result[pos_of_wall.x][pos_of_wall.y]
                if not self.get_wall_from_line_type(line_type):
                    continue

                new_type = ""
                add_type = "ensw"
                cur = 0
                for adj_wall in self.adjacent_cells(pos_of_wall):
                    if adj_wall.x < 0 or adj_wall.y < 0:
                        cur += 1
                        continue
                    if adj_wall.x >= 2 * self.height + 1 or adj_wall.y >= 2 * self.width + 1:
                        cur += 1
                        continue
                    if self.get_wall_from_line_type(result[adj_wall.x][adj_wall.y]):
                        new_type += add_type[cur]
                    cur += 1
                line_type = self.UNICODE_BY_CONNECTIONS[new_type]
                result[pos_of_wall.x][pos_of_wall.y] = line_type
        return result
    
    def convert_cells_to_int(self, *args):
        return [cell.x * self.width + cell.y if self.good_cell(cell) else -1 for cell in args]

    def __str__(self):
        result = self.get_maze()
        s = ""
        for i in result:
            for j in i:
                s += j
            s += '\n'
        return s
    
    def __repr__(self):
        return 'height = {}\nwidth = {}\nwalls = [\n{}\n]\n'.format(self.height, self.width, self.walls)
