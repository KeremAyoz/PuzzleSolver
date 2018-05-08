import unittest
from json import dumps
from src.back_end.Data.data_reader import read_full_data
from src.back_end.solver.Solve import solve, countSolved


class test_dictionary_module(unittest.TestCase):

    def test_return_word_list(self):
        full_data = read_full_data()
        with open("results.json", "a+") as result_file:
            for puzzle in full_data:
                solution_count = solve(None, puzzle['date'])
                print(puzzle['date'] + ": " + str(solution_count))
                result_file.write(dumps({puzzle['date']: solution_count}))


if __name__ == '__main__':
    unittest.main()
