from nltk.corpus import words as acceptable_words
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import wordnet as wn
from itertools import chain


class SearchModuleBaseClass:

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

    def clear_word_list(self, word_list):
        tokenized_list = set()
        for word in word_list:
            tokens = word_tokenize(word)
            words = [w.lower() for w in tokens if w.isalpha()]
            if len(words) > 0:
                tokenized_list.add(words[0])
                synonyms = wn.synsets(words[0])
                lemmas = set(chain.from_iterable([syn.lemma_names() for syn in synonyms]))
                tokenized_list = tokenized_list.union(lemmas)

        filtered_words = [word for word in tokenized_list
                          if word not in stopwords.words('english')]
                          #and self.is_english_word(word)]

        return set(filtered_words)

    def return_word_list(self, processed_query, length=3):
        raise NotImplementedError

