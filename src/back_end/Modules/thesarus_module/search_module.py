from py_thesaurus import Thesaurus
from nltk.corpus import wordnet as wn
from itertools import chain
from src.back_end.SearchModuleBaseClass import SearchModuleBaseClass


class SearchModule(SearchModuleBaseClass):
    def return_word_list(self, processed_query, length=100):
        word_list = set()
        for word in processed_query.split():
            word = word.replace("\"", "")
            word = word.replace("\'", "")
            word = word.replace("-", "")
            word = word.replace("_", "")
            word = word.replace(".", "")
            word = word.replace(",", "")
            if self.is_english_word(word):
                synonyms = wn.synsets(word)
                lemmas = set(chain.from_iterable([syn.lemma_names() for syn in synonyms]))
                word_list = word_list.union(lemmas)
                instance = Thesaurus(word)
                syns = instance.get_synonym()
                antns = instance.get_antonym()
                word_list = word_list.union(syns, antns)
        word_list = list(filter(lambda x: len(x) == length, word_list))
        print("Thesarus Search Module\nWord Count: " + str(len(word_list)))
        return word_list