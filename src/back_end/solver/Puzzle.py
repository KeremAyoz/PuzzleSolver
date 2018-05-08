from random import randint
import copy
import itertools


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
                    newWordList = list(filter(lambda x: x[i] == curElem, newWordList))
        else:
            for i in range(0, element[2]):
                curElem = self.puzzle[element[1][0]][element[1][1] + i]
                if curElem != '1':
                    newWordList = list(filter(lambda x: x[i] == curElem, newWordList))
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

    def orderProcedure(self):
        #Get horizontals
        hori = []
        verti = []
        for i in range(len(self.geometry)):
            if self.geometry[i][3] == 'h':
                hori.append(i)
            else:
                verti.append(i)
        allNewProcedures = []
        allHori = list(itertools.permutations(hori))
        allVerti = list(itertools.permutations(verti))
        for h in allHori:
            for v in allVerti:
                newPros = []
                #Combine arrays alternating order
                for i in range(10):
                    if i % 2 == 0:
                        newPros.append(h[i//2])
                    else:
                        newPros.append(v[i//2])
                allNewProcedures.append(newPros)
        return allNewProcedures

    def decideProcedure(self,solutions,wordLists):
        #Get the answers list
        found = []
        not_found = []

        #All sized 5
        solh = []
        solv = []
        keyh = []
        keyv = []

        for value in solutions['Across'].values():
            solh.append(value)
        for value in solutions['Down'].values():
            solv.append(value)

        for value in solutions['Across'].keys():
            keyh.append(value)
        for value in solutions['Down'].keys():
            keyv.append(value)

        # Horizontal
        for i in range(5):
            # Get converted index
            ind = -1
            for j in range(len(self.geometry)):
                if self.geometry[j][3] == 'h' and self.geometry[j][0] == keyh[i]:
                    ind = j
                    break
            # Check if it exists
            if solh[i].lower() in wordLists[ind]:
                found.append(ind)
            else:
                not_found.append(ind)
        # Vertical
        for i in range(5):
            # Get converted index
            ind = -1
            for j in range(len(self.geometry)):
                if self.geometry[j][3] == 'v' and self.geometry[j][0] == keyv[i]:
                    ind = j
                    break
            # Check if it exists
            if solv[i].lower() in wordLists[ind]:
                found.append(ind)
            else:
                not_found.append(ind)
        return found,not_found

    def optimizeFoundedProcedure(self, procedure):
        h = []
        v = []
        result = []
        for p in procedure:
            if self.geometry[p][3] == 'v':
                v.append(p)
            else:
                h.append(p)

        num = min(len(h), len(v))
        result = [None] * (num * 2)
        result[::2] = h[:num]
        result[1::2] = v[:num]
        result.extend(h[num:])
        result.extend(v[num:])
        return result

    def combineResults(self,solutions,wordLists):
        f, nf = self.decideProcedure(solutions,wordLists)
        f = self.optimizeFoundedProcedure(f)
        final = f + nf
        return final


    def makeAllPlacements(self, procedure):
        newPuzzleStates = []
        for i in procedure:
            if not self.geometry[i][4]:
                currentWordList = self.constraintCheck(self.geometry[i], self.wordLists[i])
                for word in currentWordList:
                    newPuzzle = self.fillTheWord(self.geometry[i], word)
                    newGeo = copy.deepcopy(self.geometry)
                    newGeo[i] = (self.geometry[i][0], self.geometry[i][1], self.geometry[i][2], self.geometry[i][3], True)
                    newPuzzleStates.append(Puzzle(newGeo, self.wordLists, newPuzzle))
                break
        return newPuzzleStates
