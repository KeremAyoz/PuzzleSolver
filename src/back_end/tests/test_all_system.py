import unittest
from json import dumps
from src.back_end.Data.data_reader import read_full_data
from src.back_end.solver.Solve import solve, countSolved


class test_dictionary_module(unittest.TestCase):

    def test_return_word_list(self):
        full_data = read_full_data()
        with open("results.json", "a+") as result_file:
            for puzzle in full_data:
                solution = solve(None, puzzle['date'])
                solution_count = countSolved(solution.puzzle)
                result_file.write(dumps({puzzle['date']: solution_count}))


if __name__ == '__main__':
    unittest.main()
