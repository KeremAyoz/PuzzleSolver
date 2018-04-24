from src.back_end.solver.Puzzle import Puzzle
from src.back_end.solver.Search import DFS
from src.back_end.google_search_module.search_module import SearchModule as GSM
from random import randint
import copy

# Puzzle of 24.04.18
q1 = (1, (0, 1), 4, 'h', False)
q2 = (1, (0, 1), 5, 'v', False)
q3 = (2, (0, 2), 5, 'v', False)
q4 = (3, (0, 3), 5, 'v', False)
q5 = (4, (0, 4), 4, 'v', False)
q6 = (5, (1, 0), 5, 'h', False)
q7 = (5, (1, 0), 4, 'v', False)
q8 = (6, (2, 0), 5, 'h', False)
q9 = (7, (3, 0), 5, 'h', False)
q10 = (8, (4, 0), 4, 'h', False)
geo = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]

# Word Lists
'''
l1 = ["cant", "tent", "even", "fore", "brut", "base", "band", "halt", "hand", "list", "dirk", "raul", "mesa", "bhaq", "doer", "lyes"]
l2 = ["basic", "ratio", "value", "radio", "alone", "arive", "tuple", "state", "handy", "quart", "table", "poker", "balmy", "umber", "adobe", "nines"]
l3 = ["basic", "ratio", "value", "radio", "alone", "arive", "tuple", "state", "handy", "quart", "table", "poker", "balmy", "umber", "adobe", "nines"]
l4 = ["basic", "ratio", "value", "radio", "alone", "arive", "tuple", "state", "handy", "quart", "table", "poker", "balmy", "umber", "adobe", "nines"]
l5 = ["cant", "tent", "even", "fore", "brut", "base", "band", "halt", "hand", "list", "dirk", "raul", "mesa", "bhaq", "doer", "lyes"]
l6 = ["basic", "ratio", "value", "radio", "alone", "arive", "tuple", "state", "handy", "quart", "table", "poker", "balmy", "umber", "adobe", "nines"]
l7 = ["cant", "tent", "even", "fore", "brut", "base", "band", "halt", "hand", "list", "dirk", "raul", "mesa", "bhaq", "doer", "lyes"]
l8 = ["basic", "ratio", "value", "radio", "alone", "arive", "tuple", "state", "handy", "quart", "table", "poker", "balmy", "umber", "adobe", "nines"]
l9 = ["basic", "ratio", "value", "radio", "alone", "arive", "tuple", "state", "handy", "quart", "table", "poker", "balmy", "umber", "adobe", "nines"]
l10 = ["cant", "tent", "even", "fore", "brut", "base", "band", "halt", "hand", "list", "dirk", "raul", "mesa", "bhaq", "doer", "lyes"]

wordLists = [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10]
'''
# Puzzle, 0 means black block, 1 means white block
puzzle = [['0', '1', '1', '1', '1'], ['1', '1', '1', '1', '1'], ['1', '1', '1', '1', '1'], ['1', '1', '1', '1', '1'], ['1', '1', '1', '1', '0']]

puzzleSolved = [['0', 'b', 'a', 'n', 'd'], ['r', 'a', 'd', 'i', 'o'], ['a', 'l', 'o', 'n', 'e'], ['u', 'm', 'b', 'e', 'r'], ['l', 'y', 'e', 's', '0']]
# Built todays puzzle

clues_accross = ["Pink floyd or Maroon 5", "Communicate between squad cars", "All by oneself", "Reddish-brown", "Corrosive cleaning compounds"]
clues_down = ["Pleasantly warm, as weather", "Maker of Flash Player and Photoshop", "Golf course halves", "Someone who isn't just all talk", "Castro who recently as Cuban president"]
l1 = GSM().return_word_list(clues_accross[0], length=4, useSelenium=True)
# l1.append("band")
l2 = GSM().return_word_list(clues_down[0], length=5, useSelenium=True)
# l2.append("balmy")
l3 = GSM().return_word_list(clues_down[1], length=5, useSelenium=True)
# l3.append("adobe")
l4 = GSM().return_word_list(clues_down[2], length=5, useSelenium=True)
# l4.append("nines")
l5 = GSM().return_word_list(clues_down[3], length=4, useSelenium=True)
# l5.append("doer")
l6 = GSM().return_word_list(clues_accross[1], length=5, useSelenium=True)
# l6.append("radio")
l7 = GSM().return_word_list(clues_down[4], length=4, useSelenium=True)
# l7.append("raul")
l8 = GSM().return_word_list(clues_accross[2], length=5, useSelenium=True)
# l8.append("alone")
l9 = GSM().return_word_list(clues_accross[3], length=5, useSelenium=True)
#l9.append("umber")
l10 = GSM().return_word_list(clues_accross[4], length=4, useSelenium=True)
l10.append("lyes")
wordLists = [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10]
print(wordLists)
todays = Puzzle(geo, wordLists, puzzle)
todaysSolved = Puzzle(geo, wordLists, puzzleSolved)
s = DFS()
solutions = s.depth_firts_search(todays, todaysSolved)
for solution in solutions:
    print(solution)
