import re
from maze import *
from builder import *
from solver import *
from graphics import *

class Interface:
    def __init__(self):
        pass

    def get_builder(self, generator: BuilderGenerator = BuilderGenerator.Cruscal):
        generator_name = BuilderGenerator(generator).name
        generator = BuilderGenerator[generator_name]
        if generator == BuilderGenerator.Cruscal:
            return MazeCruscalBuilder()
        elif generator == BuilderGenerator.DFS:
            return MazeDFSBuilder()
        return MazeBuilder()

    def get_solver(self, algorithm: SolverAlgorithm = SolverAlgorithm.BFS):
        algorithm_name = SolverAlgorithm(algorithm).name
        algorithm = SolverAlgorithm[algorithm_name]
        if algorithm == SolverAlgorithm.BFS:
            return MazeSolverBFS()
        elif algorithm == SolverAlgorithm.AStar:
            return MazeSolverAStar()
        return MazeSolver()
    
    def get_graphics(self, maze: Maze, graphics: GraphicsType = GraphicsType.Console):
        graphics_name = GraphicsType(graphics).name
        graphics = GraphicsType[graphics_name]
        if graphics == GraphicsType.Console:
            return ConsoleGraphics(maze)
        elif graphics == GraphicsType.Game:
            return GameGraphics(maze)
        return Graphics()

    def save_maze(self, maze: Maze, filename: str):
        fout = open(filename, "w")
        fout.write(str(maze))
        fout.close()

    def upload_maze(self, filename: str):
        fin = open(filename, "r")
        height = 0
        width = 0
        uploaded_maze = []
        for s in fin:
            s = re.sub(r'\n', '', s)
            uploaded_maze.append(s)
            width = len(s) // 2
            height += 1
        height //= 2
        maze = Maze(height, width)

        for first_cell in maze.get_cells():
            pos_of_first_cell = first_cell * 2 + Cell(1, 1)
            for second_cell in maze.adjacent_cells(first_cell):
                pos_of_second_cell = second_cell * 2 + Cell(1, 1)
                pos_of_wall = (pos_of_first_cell + pos_of_second_cell) / 2
                line_type = uploaded_maze[pos_of_wall.x][pos_of_wall.y]
                maze.set_wall(first_cell, second_cell, maze.get_wall_from_line_type(line_type))

        fin.close()
        return maze


interface = Interface()

upload = input('Do you want upload Maze? [y/n] ')
if upload == 'y':
    filename = input('Please, write Filename: ')
    maze = interface.upload_maze(filename)
else:
    builder_type = input('Please, select Maze Generator:\n1. {}\n2. {}\n'.format(BuilderGenerator.Cruscal.value, BuilderGenerator.DFS.value))
    if builder_type == '1':
        builder_type = BuilderGenerator.Cruscal
    elif builder_type == '2':
        builder_type = BuilderGenerator.DFS

    builder = interface.get_builder(builder_type)
    height, width = map(int, input('Please, write Height and Width of Maze\n').split())
    maze = builder.build(height, width)


solver_type = input('Please, select Solver Algorithm:\n1. {}\n2. {}\n'.format(SolverAlgorithm.BFS.value, SolverAlgorithm.AStar.value))
if solver_type == '1':
    solver_type = SolverAlgorithm.BFS
elif solver_type == '2':
    solver_type = SolverAlgorithm.AStar

solver = interface.get_solver(solver_type)

graphics_type = input('Please, select Graphics:\n1. {}\n2. {}\n'.format(GraphicsType.Console.value, GraphicsType.Game.value))
if graphics_type == '1':
    graphics_type = GraphicsType.Console
elif graphics_type == '2':
    graphics_type = GraphicsType.Game
graphics = interface.get_graphics(maze, graphics_type)

save = input('Do you want to save Maze? [y/n] ')
if save == 'y':
    filename = input('Please, write Filename: ')
    interface.save_maze(maze, filename)
graphics.work(solver)
