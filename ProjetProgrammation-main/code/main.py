from grid import Grid
from solver import *
import os


grid = Grid(2, 3)
print(grid)

data_path = os.path.join(os.path.dirname(__file__), "../input/")

file_name = data_path + "grid11.in"
grid1 = Grid.grid_from_file(file_name)
print(grid1)

file_name = data_path + "grid00.in"
grid = Grid.grid_from_file(file_name, read_values=True)
print(grid)

solver = SolverEmpty(grid)
solver.run()
print("The final score of SolverEmpty is:", solver.score()) # Question : comment ça marche solverempty score ???

rsolver = Solver(grid)
rsolver.run()
print("The final score of the Solver is : ", rsolver.score())

msolver = SolverMatching(grid)
msolver.run()
print("The final score of the MatchingSolver is : ", msolver.score())

msolver1, rsolver1 = SolverMatching(grid1), Solver(grid1)
print(msolver.score(), rsolver.score())

grid.plot()


