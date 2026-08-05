import sys
import os
import unittest
import importlib

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

sudoku_module = importlib.import_module("games.Sudoku-Game.Sudoku-Game")
solve_sudoku_backtracking = sudoku_module.solve_sudoku_backtracking
is_valid = sudoku_module.is_valid

class TestSudokuSolver(unittest.TestCase):
    def test_iterative_sudoku_solver(self):
        # Sample 9x9 Sudoku puzzle
        grid = [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]

        success = solve_sudoku_backtracking(grid)
        self.assertTrue(success)

        # Verify no 0s remain
        for r in range(9):
            for c in range(9):
                val = grid[r][c]
                self.assertNotEqual(val, 0)
                self.assertTrue(is_valid(grid, r, c, val))

if __name__ == "__main__":
    unittest.main()
