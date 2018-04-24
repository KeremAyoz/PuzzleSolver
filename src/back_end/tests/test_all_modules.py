import unittest
from src.back_end.Data.data_reader import read_full_data
from src.back_end.dictionary_search_module.search_module import SearchModule as dict_search_module
from src.back_end.google_search_module.search_module import SearchModule as google_search_module
from src.back_end.wikipedia_search_module.SearchModule import SearchModule as wiki_search_module
from src.back_end.thesarus_module.search_module import SearchModule as thesarus_search_module


class test_dictionary_module(unittest.TestCase):
    def test_return_word_list(self):
        total = 0
        true = 0
        false = 0
        invalid = 0
        word_list = set()
        data = read_full_data()
        tsm = thesarus_search_module()
        gsm = google_search_module()
        dsm = dict_search_module()
        wsm = wiki_search_module()
        for puzzle in data:
            down_clues = puzzle['clues']['Down']
            across_clues = puzzle['clues']['Across']
            for clue in down_clues:
                try:
                    total += 1
                    search_query = clue['hint']
                    key = clue['key']
                    answer = puzzle['solutions']['Down'][key]
                    word_list.clear()
                    word_list = tsm.return_word_list(search_query)
                    word_list = word_list.union(
                        gsm.return_word_list(search_query, useSelenium=True),
                        dsm.return_word_list(search_query, useSelenium=True),
                        wsm.return_word_list(search_query, useSelenium=True)
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
                    word_list = tsm.return_word_list(search_query)
                    word_list = word_list.union(
                        gsm.return_word_list(search_query, useSelenium=True),
                        dsm.return_word_list(search_query, useSelenium=True),
                        wsm.return_word_list(search_query, useSelenium=True)
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


if __name__ == '__main__':
    unittest.main()
