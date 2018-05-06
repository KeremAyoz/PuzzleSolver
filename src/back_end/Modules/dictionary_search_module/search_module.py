from src.back_end.SearchModuleBaseClass import SearchModuleBaseClass
import requests
from bs4 import BeautifulSoup
from src.back_end.SeleniumGoogleSearchParser import parse_google_search


class SearchModule(SearchModuleBaseClass):

    def return_word_list(self, processed_query, length=None, useSelenium=False):
        word_list = set()
        if useSelenium:
            word_list = parse_google_search(processed_query, site="dictionary.com")
        else:
            query = processed_query.replace(" ", "+")

            r = requests.get(
                'https://www.google.com/search?q={}&as_sitesearch=dictionary.com&lr=lang_en'
                .format(query))
            soup = BeautifulSoup(r.content, "html.parser")
            result_elements = soup.text
            for word in result_elements.split():
                word_list.add(word)

        # Process word list
        word_list = self.clear_word_list(word_list)
        word_list = list(filter(lambda x: len(x) == length, word_list))
        print("Dictionary Search Module\nWord Count: " + str(len(word_list)))
        return word_list