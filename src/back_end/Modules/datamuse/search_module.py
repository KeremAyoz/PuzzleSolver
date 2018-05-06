import requests

from src.back_end.SearchModuleBaseClass import SearchModuleBaseClass


class SearchModule(SearchModuleBaseClass):

    def return_word_list(self, processed_query, length=3):
        query = processed_query.replace(" ", "+")
        query = query.lower()

        r = requests.get(
            'https://api.datamuse.com/words?ml={}'
            .format(query))

        results = r.json()
        word_list = []
        for result in results:
            word_list.append(result['word'])

        word_list = list(filter(lambda x: len(x) == length, word_list))
        print("Datamuse Search Module\nWord Count: " + str(len(word_list)))
        return word_list