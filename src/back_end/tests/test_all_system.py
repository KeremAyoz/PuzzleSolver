import unittest
from json import dumps
from src.back_end.Data.data_reader import read_full_data, read_data_from_date
from src.back_end.solver.Solve import solve, countSolved


class test_dictionary_module(unittest.TestCase):

    def test_return_word_list(self):
        full_data = read_full_data()
        #full_data = [read_data_from_date('2018-02-23')]
        solutions = []
        with open("results.json", "w") as result_file:
            for puzzle in full_data:
                solution_count = solve(None, puzzle['date'])
                print(puzzle['date'] + ": " + str(solution_count))
                t = {puzzle['date']: solution_count}
                solutions.append(t)
                result_file.write(dumps(solutions))


if __name__ == '__main__':
    unittest.main()
