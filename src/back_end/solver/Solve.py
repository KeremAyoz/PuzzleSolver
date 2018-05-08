from pandas._libs import json

from src.back_end.Data.data_reader import read_data_from_date
from src.back_end.Modules.dictionary_search_module.search_module import SearchModule as dict_search_module
from src.back_end.Modules.google_search_module.search_module import SearchModule as google_search_module
from src.back_end.solver.Puzzle import Puzzle
from src.back_end.solver.Search import DFS
from src.back_end.Modules.wikipedia_search_module.SearchModule import SearchModule as wiki_search_module
from src.back_end.Modules.thesarus_module.search_module import SearchModule as thesarus_search_module
from src.back_end.Modules.datamuse.search_module import SearchModule as datamuse_seacrh
from random import randint
from copy import copy, deepcopy

def getGeometryFromJson(json):

    def searchCell(cells, key):
        for cell in cells:
            if cell['key'] == key:
                return cell['y'] - 1 , cell['x'] - 1

    solutions = json['solutions']
    geometry = []
    cells = json['cells']
    for direction in solutions:
        for solutionKey, solutionValue in solutions[direction].items():
            length = len(solutionValue)
            d = 'h'
            if direction == "Down":
                d = 'v'
            indices = searchCell(cells,solutionKey)
            geometry.append((solutionKey, indices, length, d , False))

    return geometry


def getConstraintsFromGeometry(geometry):

    def checkIntersection(geo1index, geo1, geo2index, geo2):
        if geo1[3] == geo2[3]:
            return None
        else:
            horizontal = geo2
            horizontal_index = geo2index
            vertical = geo1
            vertical_index = geo1index
            if geo1[3] == 'h':
                horizontal = geo1
                horizontal_index = geo1index
                vertical = geo2
                vertical_index = geo2index

            horizontal_coordinates = []
            vertical_coordinates = []
            for x in range(horizontal[2]):
                horizontal_coordinates.append((horizontal[1][0], horizontal[1][1] + x))
            for y in range(vertical[2]):
                vertical_coordinates.append((vertical[1][0]+ y, vertical[1][1]))

            crossing = [value for value in horizontal_coordinates if value in vertical_coordinates]
            # crossing = list((set(horizontal_coordinates).intersection(set(vertical_coordinates))))
            if len(crossing) == 0:
                return None

            intersection_x = abs(horizontal[1][0] - crossing[0][0])
            intersection_y = abs(vertical[1][1] - crossing[0][1])
            return (horizontal_index, intersection_x), (vertical_index, intersection_y)

    constraints = []
    for i in range(len(geometry)):
        for j in range(i+1, len(geometry)):
            if i != j:
                g1 = geometry[i]
                g2 = geometry[j]
                intersection = checkIntersection(i, g1, j, g2)
                if intersection:
                    constraints.append(intersection)

    return constraints


def getClues(puzzle_json, geometry):
    unordered_clues = puzzle_json['clues']
    ordered_clues = []
    for geo in geometry:
        if geo[3] == 'h':
            for clue in unordered_clues['Across']:
                if clue['key'] == geo[0]:
                    ordered_clues.append(clue['hint'])
        else:
            for clue in unordered_clues['Down']:
                if clue['key'] == geo[0]:
                    ordered_clues.append(clue['hint'])
    return ordered_clues


def reduceLists(constraints, wordLists):
    isChanged = True
    while isChanged:
        for everyConstraint in constraints:
            reducedSecond = set()
            for everyWord in wordLists[everyConstraint[0][0]]:
                # Reduced version of second by looking to first
                sec = list(filter(lambda x: x[everyConstraint[1][1]] == everyWord[everyConstraint[0][1]],
                                  wordLists[everyConstraint[1][0]]))
                # Add the new items to set
                for item in sec:
                    reducedSecond.add(item)
            # Equate the reduced version to actual list
            if set(wordLists[everyConstraint[1][0]]) == set(list(reducedSecond)):
                isChanged = False
            wordLists[everyConstraint[1][0]] = list(reducedSecond)

            reducedFirst = set()
            for everyWord in wordLists[everyConstraint[1][0]]:
                # Reduced version of second by looking to first
                fir = list(filter(lambda x: x[everyConstraint[0][1]] == everyWord[everyConstraint[1][1]],
                                  wordLists[everyConstraint[0][0]]))
                if fir != wordLists[everyConstraint[1][0]]:
                    isChanged = True
                # Add the new items to set
                for item in fir:
                    reducedFirst.add(item)
                # Equate the reduced version to actual list
            if set(wordLists[everyConstraint[0][0]]) == set(list(reducedFirst)):
                isChanged = False
            wordLists[everyConstraint[0][0]] = list(reducedFirst)
    return wordLists


def puzzleTo2DArray(puzzle_json):
    array = [['1', '1', '1', '1', '1'],
             ['1', '1', '1', '1', '1'],
             ['1', '1', '1', '1', '1'],
             ['1', '1', '1', '1', '1'],
             ['1', '1', '1', '1', '1'] ]

    for cell in puzzle_json['cells']:
        if cell['color'] == 'black':
            array[cell['y'] - 1][cell['x'] - 1] = '0'
    return array


def puzzleToSolvedPuzzle(puzzle_json):
    array = [['0', '0', '0', '0', '0'],
             ['0', '0', '0', '0', '0'],
             ['0', '0', '0', '0', '0'],
             ['0', '0', '0', '0', '0'],
             ['0', '0', '0', '0', '0']]

    for cell in puzzle_json['solution_cells']:
        if cell['color'] != 'black':
            array[cell['y'] - 1][cell['x'] - 1] = cell['solution'].lower()

    return array

def countSolved(array):
    count = 0
    for i in range(len(array)):
        for j in range(len(array[i])):
            if array[i][j] != '1' and array[i][j] != '0':
                count += 1
    return count


def solve(callback, date):
    puzzle_json = read_data_from_date(date)
    geometry = getGeometryFromJson(puzzle_json)
    constraints = getConstraintsFromGeometry(geometry)
    clues = getClues(puzzle_json,geometry)
    wordLists = []
    tsm = thesarus_search_module()
    gsm = google_search_module()
    dsm = dict_search_module()
    wsm = wiki_search_module()
    datamuse = datamuse_seacrh()
    i = 0
    for clue in clues:
        word_list = set()
        print("\n" + clue)
        word_list = word_list.union(
            #tsm.return_word_list(clue),
            gsm.return_word_list(clue, length=geometry[i][2], useSelenium=False),
            datamuse.return_word_list(clue, length=geometry[i][2]),
            dsm.return_word_list(clue, length=geometry[i][2], useSelenium=False),
            wsm.return_word_list(clue, length=geometry[i][2], useSelenium=False)
        )
        wordLists.append(word_list)
        i += 1

    #Reduce the wordList got from the search modules
    wordLists = reduceLists(constraints, wordLists)
    todays = Puzzle(geometry, wordLists, puzzleTo2DArray(puzzle_json))
    todaysSolved = Puzzle(geometry, wordLists, puzzleToSolvedPuzzle(puzzle_json))
    '''
    # Comment out here to test
    f, n = todays.decideProcedure(puzzle_json['solutions'],wordLists)
    return len(f)
    '''
    s = DFS(callback)
    solutions = s.threading_wrap(todays, todaysSolved, date)

    return solutions
