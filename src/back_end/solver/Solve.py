from Puzzle import Puzzle
from Search import DFS
from random import randint
import copy

# Puzzle of 24.04.18
q1 = (1, (0, 1), 4, 'h', False)
q2 = (1, (0, 1), 5, 'v', False)
q3 = (2, (0, 2), 5, 'v', False)
q4 = (3, (0, 3), 5, 'v', False)
q5 = (4, (0, 4), 4, 'v', False)
q6 = (5, (1, 1), 5, 'h', False)
q7 = (5, (1, 1), 4, 'v', False)
q8 = (6, (2, 1), 5, 'h', False)
q9 = (7, (3, 1), 5, 'h', False)
q10 = (8, (4, 1), 5, 'h', False)
geo = [q1, q2, q3, q4, q5, q6, q7, q8, q9, q10]

# Word Lists
l1 = ["cant", "tent", "even", "fore", "brut", "base", "band", "halt", "hand", "list", "dirk", "raul", "mesa", "bhaq", "doer", "lyes"]
l2 = ["basic", "ratio", "value", "radio", "alone", "arive", "tuple", "state", "handy", "quart", "table", "poker", "balmy", "umber", "adobe", "nines"]
l3 = ["basic", "ratio", "value", "radio", "alone", "arive", "tuple", "state", "handy", "quart", "table", "poker", "balmy", "umber", "adobe", "nines"]
l4 = ["basic", "ratio", "value", "radio", "alone", "arive", "tuple", "state", "handy", "quart", "table", "poker", "balmy", "umber", "adobe", "nines"]
l5 = ["cant", "tent", "even", "fore", "brut", "base", "band", "halt", "hand", "list", "dirk", "raul", "mesa", "bhaq", "doer", "lyes"]
l6 = ["basic", "ratio", "value", "radio", "alone", "arive", "tuple", "state", "handy", "quart", "table", "poker", "balmy", "umber", "adobe", "nines"]
l7 = ["cant", "tent", "even", "fore", "brut", "base", "band", "halt", "hand", "list", "dirk", "raul", "mesa", "bhaq", "doer", "lyes"]
l8 = ["basic", "ratio", "value", "radio", "alone", "arive", "tuple", "state", "handy", "quart", "table", "poker", "balmy", "umber", "adobe", "nines"]
l9 = ["basic", "ratio", "value", "radio", "alone", "arive", "tuple", "state", "handy", "quart", "table", "poker", "balmy", "umber", "adobe", "nines"]
l10 = ["basic", "ratio", "value", "radio", "alone", "arive", "tuple", "state", "handy", "quart", "table", "poker", "balmy", "umber", "adobe", "nines"]
wordLists = [l1, l2, l3, l4, l5, l6, l7, l8, l9, l10]

# Puzzle, 0 means black block, 1 means white block
puzzle = [['0', '1', '1', '1', '1'], ['1', '1', '1', '1', '1'], ['1', '1', '1', '1', '1'], ['1', '1', '1', '1', '1'], ['1', '1', '1', '1', '0']]

puzzleSolved = [['0', 'b', 'a', 'n', 'd'], ['r', 'a', 'd', 'i', 'o'], ['a', 'l', 'o', 'n', 'e'], ['u', 'm', 'b', 'e', 'r'], ['l', 'y', 'e', 's', '0']]
# Built todays puzzle
todays = Puzzle(geo, wordLists, puzzle)
todaysSolved = Puzzle(geo, wordLists, puzzleSolved)
s = DFS()
s.depth_firts_search(todays, todaysSolved)
