# This will work if ran from the root folder (the folder in which there is the subfolder code/)
import sys 
sys.path.append("code/")
import unittest
from solver import Solver 
from grid import Grid

class Test_GridLoading(unittest.TestCase):
    def test_grid0(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)
        self.assertEqual(grid.color, [[0, 0, 0], [0, 0, 0]])
        self.assertEqual(grid.value, [[5, 8, 4], [11, 1, 3]])
        self.assertFalse(grid.is_forbidden(0, 0))
        self.assertEqual(grid.cost(((0, 0), (0, 1))), 3)
        self.assertIn(((0, 0), (0, 1)), grid.all_pairs())

    def test_grid0_novalues(self):
        grid = Grid.grid_from_file("input/grid00.in",read_values=False)
        self.assertEqual(grid.value, [[1, 1, 1], [1, 1, 1]])
        self.assertFalse(grid.is_forbidden(0, 0))
        self.assertEqual(grid.cost(((0, 0), (0, 1))), 0)
        self.assertIn(((0, 0), (0, 1)), grid.all_pairs())

    def test_grid1(self):
        grid = Grid.grid_from_file("input/grid01.in",read_values=True)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)
        self.assertEqual(grid.color, [[0, 4, 3], [2, 1, 0]])
        self.assertEqual(grid.value, [[5, 8, 4], [11, 1, 3]])
        self.assertTrue(grid.is_forbidden(0, 1))
        self.assertEqual(grid.cost(((1, 0), (1, 1))), 10)
        self.assertIn(((1, 0), (1, 1)), grid.all_pairs())

    def test_grid2(self):
        grid = Grid.grid_from_file("input/grid02.in", read_values=True)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)
        
        self.assertFalse(grid.is_forbidden(1, 2))
        self.assertEqual(grid.cost(((0, 2), (1, 2))), 0)
        self.assertIn(((0, 2), (1, 2)), grid.all_pairs())

    def test_solver_greedy_grid0(self):
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        solver = Solver(grid)
        solver.run()
        self.assertGreater(len(solver.pairs), 0)  # Vérifie que des paires sont trouvées
        self.assertGreater(solver.score(), 0)  # Vérifie que le score est bien calculé et positif
    

if __name__ == '__main__':
    unittest.main()
