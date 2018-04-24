
import requests
from bs4 import BeautifulSoup
from src.back_end.SearchModuleBaseClass import SearchModuleBaseClass
from src.back_end.SeleniumGoogleSearchParser import parse_google_search


class SearchModule(SearchModuleBaseClass):

    def return_word_list(self, processed_query, length=None, useSelenium=False):
        word_list = set()
        if useSelenium:
            word_list = parse_google_search(processed_query)
        else:
            query = processed_query.replace(" ", "+")

            r = requests.get(
                'https://www.google.com/search?q={}'
                .format(query))
            soup = BeautifulSoup(r.content, "html.parser")
            result_elements = soup.text
            print(soup.prettify())
            for word in result_elements.split():
                word_list.add(word)

        # Process word list
        word_list = self.clear_word_list(word_list)
        print("found word count: " + str(len(word_list)))
        return word_list


if __name__ == '__main__':
    print(SearchModule().return_word_list("Growth on old bread", 10 , useSelenium=True))
