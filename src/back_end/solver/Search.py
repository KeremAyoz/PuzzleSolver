from src.back_end.solver.Puzzle import Puzzle
from random import randint, shuffle
import copy
import itertools
'''
class MagneficentSolver:

    def createConstraints(self):
        constraints = []
        across = self.geometry['Across']
        down = self.geometry['Down']
        for cell in self.geometry['cells']


    def __init__(self,geometry):
        self.geometry = geometry
'''

class DFS:

    def __init__(self):
        self.bests = []
        self.queue = []
        self.procedure = [0,1,2,3,4,5,6,7,8,9]
        # shuffle(self.procedure)
    # Store all paths visited in queue

    def depth_firts_search(self, start, goal):
        # Form a one element queue consisting of start
        self.queue.insert(0, [start])
        flag = True
        # While queue is not empty
        allProcedures = list(itertools.permutations(self.procedure))
        for procedure in allProcedures:
            while(self.queue):

                # Select randomly
                stateWillBeExpanded = self.queue[0][-1]
                # If goal node is found in front of the queue, announce success
                if stateWillBeExpanded.puzzle == goal.puzzle:
                    print("Success: " + str(self.queue[0]) + "\n")
                    self.bests.append(self.queue[0][-1])
                    return self.bests

                # Expand the state with min score
                newStates = stateWillBeExpanded.makeAllPlacements(flag, procedure)
                print(stateWillBeExpanded)
                if len(newStates) > 0:
                    if flag:
                        flag = False
                    else:
                        flag = True
                else:
                    self.bests.append(stateWillBeExpanded)

                # Remove the cycling paths
                '''
                for a in newStates:
                    if a in self.queue[0]:
                        newStates.remove(a)
                '''

                firstPath = copy.deepcopy(self.queue[0])

                # Delete the first path in queue
                del self.queue[0]

                # Add the newly expanded paths
                for states in newStates:

                    # Build the new paths with newStates in the terminal position
                    expandedPath = copy.deepcopy(firstPath)
                    expandedPath.append(states)
                    self.queue.insert(0, expandedPath)

        return self.bests
