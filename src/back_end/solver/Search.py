from src.back_end.solver.Puzzle import Puzzle
from random import randint, shuffle
import copy
import itertools
import threading
import pprint
import sys

class DFS:

    def __init__(self, callback):
        self.bests = [[]]*10
        self.queue = [[]]*10
        self.threads = []
        self.procedure = [0,1,2,3,4,5,6,7,8,9]
        self.callback = callback
        # shuffle(self.procedure)
    # Store all paths visited in queue

    def threading_wrap(self, start, goal):
        for i in range(10):
            self.threads.append(threading.Thread(target=self.depth_firts_search, args=(start, goal, i,)))
            self.threads[i].start()

        for i in range(10):
            self.threads[i].join()

        return list(itertools.chain.from_iterable(self.bests))

    def depth_firts_search(self, start, goal, id):
        # Form a one element queue consisting of start
        self.queue[0].insert(0, [start])
        flag = True
        # While queue is not empty
        allProcedures = list(itertools.permutations(self.procedure[id:] + self.procedure[:id]))
        for procedure in allProcedures:
            #print(procedure)
            while(len(self.queue[id]) > 0):

                # Select randomly
                stateWillBeExpanded = self.queue[id][0][-1]
                if id == 0:
                    counter = counter + 1
                    if counter % 50 == 0:
                        self.callback.set_puzzle_as(stateWillBeExpanded.puzzle)
                # If goal node is found in front of the queue, announce success
                if stateWillBeExpanded.puzzle == goal.puzzle:
                    print("Success: " + str(self.queue[id][0]) + "\n")
                    sys.exit()
                    self.bests[id].append(self.queue[id][0])
                    return self.bests[id]

                # Expand the state with min score
                newStates = stateWillBeExpanded.makeAllPlacements(flag, procedure)
                print(stateWillBeExpanded)
                if len(newStates) > 0:
                    if flag:
                        flag = False
                    else:
                        flag = True
                else:
                    self.bests[id].append(stateWillBeExpanded)

                # Remove the cycling paths
                '''
                for a in newStates:
                    if a in self.queue[0]:
                        newStates.remove(a)
                '''

                firstPath = copy.deepcopy(self.queue[id][0])

                # Delete the first path in queue
                del self.queue[id][0]

                # Add the newly expanded paths
                for states in newStates:

                    # Build the new paths with newStates in the terminal position
                    expandedPath = copy.deepcopy(firstPath)
                    expandedPath.append(states)
                    self.queue[id].insert(0, expandedPath)

        return self.bests
