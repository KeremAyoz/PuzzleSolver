import json
import unittest
from src.back_end.Data.data_reader import read_full_data, read_data_from_date
from src.back_end.Modules.dictionary_search_module.search_module import SearchModule as dict_search_module
from src.back_end.Modules.google_search_module.search_module import SearchModule as google_search_module
from src.back_end.Modules.wikipedia_search_module.SearchModule import SearchModule as wiki_search_module
from src.back_end.Modules.datamuse.search_module import SearchModule as datamuse_seacrh


class test_dictionary_module(unittest.TestCase):

    def test_return_word_list(self):
        word_list = set()
        data = read_full_data()
        gsm = google_search_module()
        dsm = dict_search_module()
        wsm = wiki_search_module()
        datamuse = datamuse_seacrh()
        results = []
        for puzzle in data:
            total = 0
            true = 0
            false = 0
            invalid = 0
            with open("results.json", "w") as result_file:
                down_clues = puzzle['clues']['Down']
                across_clues = puzzle['clues']['Across']
                for clue in down_clues:
                    try:
                        total += 1
                        search_query = clue['hint']
                        key = clue['key']
                        answer = puzzle['solutions']['Down'][key]
                        word_list.clear()
                        word_list = set()
                        word_list = word_list.union(
                            gsm.return_word_list(search_query, useSelenium=True),
                            dsm.return_word_list(search_query, useSelenium=True),
                            wsm.return_word_list(search_query, useSelenium=True),
                            datamuse.return_word_list(search_query)
                        )
                        if answer.lower() in word_list:
                            print("found answer for: " + search_query)
                            true += 1
                        else:
                            false += 1
                    except Exception as e:
                        print("exception", str(e))
                        invalid += 1
                for clue in across_clues:
                    try:
                        total += 1
                        search_query = clue['hint']
                        key = clue['key']
                        answer = puzzle['solutions']['Across'][key]
                        word_list.clear()
                        word_list = set()
                        word_list = word_list.union(
                            gsm.return_word_list(search_query, useSelenium=True),
                            dsm.return_word_list(search_query, useSelenium=True),
                            wsm.return_word_list(search_query, useSelenium=True),
                            datamuse.return_word_list(search_query)
                        )
                        if answer.lower() in word_list:
                            print("found answer for: " + search_query)
                            true += 1
                        else:
                            false += 1
                    except Exception as e:
                        print("exception: ", str(e))
                        invalid += 1
                results.append({puzzle['date']: str(true), 'invalid': invalid > 0})
                print(json.dumps({puzzle['date']: str(true), 'invalid': invalid > 0}))
                result_file.seek(0)
                result_file.truncate()
                result_file.write(json.dumps(results))
'''
    def test_for_date(self):
        date = "2018-04-26"
        puzzle = read_data_from_date(date)
        print(puzzle)
        total = 0
        true = 0
        false = 0
        invalid = 0
        word_list = set()
        gsm = google_search_module()
        dsm = dict_search_module()
        wsm = wiki_search_module()
        datamuse = datamuse_seacrh()
        down_clues = puzzle['clues']['Down']
        across_clues = puzzle['clues']['Across']
        for clue in down_clues:
            try:
                total += 1
                search_query = clue['hint']
                key = clue['key']
                answer = puzzle['solutions']['Down'][key]
                word_list.clear()
                word_list = set()
                word_list = word_list.union(
                    gsm.return_word_list(search_query, useSelenium=True),
                    dsm.return_word_list(search_query, useSelenium=True),
                    wsm.return_word_list(search_query, useSelenium=True),
                    datamuse.return_word_list(search_query)
                )
                if answer.lower() in word_list:
                    print("found answer for: " + search_query)
                    true += 1
                else:
                    false += 1
            except Exception as e:
                print("exception", str(e))
                invalid += 1
        for clue in across_clues:
            try:
                total += 1
                search_query = clue['hint']
                key = clue['key']
                answer = puzzle['solutions']['Across'][key]
                word_list.clear()
                word_list = set()
                word_list = word_list.union(
                    gsm.return_word_list(search_query, useSelenium=True),
                    dsm.return_word_list(search_query, useSelenium=True),
                    wsm.return_word_list(search_query, useSelenium=True),
                    datamuse.return_word_list(search_query)
                )
                if answer.lower() in word_list:
                    print("found answer for: " + search_query)
                    true += 1
                else:
                    false += 1
            except Exception as e:
                print("exception: ", str(e))
                invalid += 1

        print("total : " + str(total))
        print("true : " + str(true))
        print("false : " + str(false))
        print("invalid : " + str(invalid))
'''
if __name__ == '__main__':
    unittest.main()
