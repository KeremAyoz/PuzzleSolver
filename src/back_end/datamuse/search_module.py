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

        return list(filter(lambda x: len(x) == length, word_list))


print(SearchModule().return_word_list("Driverless car company developed by Google", length=5))