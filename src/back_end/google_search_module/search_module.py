from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from nltk.corpus import stopwords
from nltk.corpus import words as acceptable_words
from nltk.tokenize import word_tokenize


class SearchModule:
    def __init__(self):
        self.dictionary = dict.fromkeys(acceptable_words.words(), None)

    def is_english_word(self, word):
        # creation of this dictionary would be done outside of
        #     the function because you only need to do it once.
        try:
            x = self.dictionary[word]
            return True
        except KeyError:
            return False

    def clear_word_list(self,word_list):
        tokenized_list = set()
        for word in word_list:
            tokens = word_tokenize(word)
            words = [w.lower() for w in tokens if w.isalnum()]
            if len(words) > 0:
                tokenized_list.add(words[0])

        filtered_words = [word for word in tokenized_list
                          if word not in stopwords.words('english')
                          and self.is_english_word(word)]

        return set(filtered_words)

    def return_word_list(self, processed_query, length=100):
        word_list = set()
        driver = webdriver.Chrome()
        driver.get("https://www.google.com")
        search_element = driver.switch_to.active_element
        search_element.send_keys(processed_query)
        search_element.send_keys(Keys.ENTER)
        driver.implicitly_wait(10)
        result_elements = driver.find_elements_by_class_name("rc")
        print(result_elements)
        for result in result_elements:
            for word in result.text.split():
                word_list.add(word)

        driver.close()
        # Process word list
        return self.clear_word_list(word_list)


if __name__ == '__main__':
    print(SearchModule().return_word_list("Growth on old bread", 10))
