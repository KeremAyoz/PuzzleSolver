from random import randint
import copy


class Puzzle:

    # Puzzle geometry that stores tuples with following form:
    # (Question number, starting position, ending length,  vertical/horizontal)
    # Example --> (1, (0,0), 4, 'v')
    geometry = []

    # Word lists for all clues. It contains 8,9 lists that contains possible words for clues.
    wordLists = []

    # Fixed 5 by 5 puzzle area, which is a char double array
    puzzle = []

    def __init__(self, geometry, wordLists, puzzle):
        self.geometry = geometry
        self.wordLists = wordLists
        self.puzzle = puzzle

    def __str__(self):
        string = ""
        string += "*************\n"
        for line in self.puzzle:
            string += str(line) + "\n"
        string += "*************\n"
        return string

    def constraintCheck(self, element, wordList):
        constraints = []
        newWordList = wordList
        if element[3] == 'v':
            for i in range(0, element[2]):
                curElem = self.puzzle[element[1][0] + i][element[1][1]]
                if curElem != '1':
                    newWordList = filter(lambda x: x[i] == curElem, newWordList)
        else:
            for i in range(0, element[2]):
                curElem = self.puzzle[element[1][0]][element[1][1] + i]
                if curElem != '1':
                    newWordList = filter(lambda x: x[i] == curElem, newWordList)
        return newWordList

    def fillTheWord(self, element, word):
        newPuzzle = copy.deepcopy(self.puzzle)
        if element[3] == 'v':
            for i in range(0, element[2]):
                newPuzzle[element[1][0] + i][element[1][1]] = word[i]
        else:
            for i in range(0, element[2]):
                newPuzzle[element[1][0]][element[1][1] + i] = word[i]
        return newPuzzle

    def makeAllPlacements(self, flag):
        newPuzzleStates = []
        if flag:
            for i in range(len(self.geometry)):
                if self.geometry[i][3] == 'h' and not self.geometry[i][4]:
                    currentWordList = self.constraintCheck(self.geometry[i], self.wordLists[i])
                    for word in currentWordList:
                        newPuzzle = self.fillTheWord(self.geometry[i], word)
                        newGeo = copy.deepcopy(self.geometry)
                        newGeo[i] = (self.geometry[i][0], self.geometry[i][1], self.geometry[i][2], self.geometry[i][3], True)
                        newPuzzleStates.append(Puzzle(newGeo, self.wordLists, newPuzzle))
                    break
            flag = not flag
        else:
            for i in range(len(self.geometry)):
                if self.geometry[i][3] == 'v' and not self.geometry[i][4]:
                    currentWordList = self.constraintCheck(self.geometry[i], self.wordLists[i])
                    for word in currentWordList:
                        newPuzzle = self.fillTheWord(self.geometry[i], word)
                        newGeo = copy.deepcopy(self.geometry)
                        newGeo[i] = (self.geometry[i][0], self.geometry[i][1], self.geometry[i][2], self.geometry[i][3], True)
                        newPuzzleStates.append(Puzzle(newGeo, self.wordLists, newPuzzle))
                    break
            flag = not flag

        return newPuzzleStates
