from Puzzle import Puzzle
from random import randint
import copy


class DFS:

    # Store all paths visited in queue
    queue = []

    def depth_firts_search(self, start, goal):
        # Form a one element queue consisting of start
        self.queue.insert(0, [start])
        flag = True
        # While queue is not empty
        while(self.queue):

            # Select randomly
            stateWillBeExpanded = self.queue[0][-1]
            print(stateWillBeExpanded)
            # If goal node is found in front of the queue, announce success
            if stateWillBeExpanded == goal:
                print("Success: " + str(self.queue[0]) + "\n")
                return

            # Expand the state with min score
            newStates = stateWillBeExpanded.makeAllPlacements(flag)

            # Remove the cycling paths
            for a in newStates:
                if a in self.queue[0]:
                    newStates.remove(a)

            firstPath = copy.deepcopy(self.queue[0])

            # Delete the first path in queue
            del self.queue[0]

            # Add the newly expanded paths
            for states in newStates:

                # Build the new paths with newStates in the terminal position
                expandedPath = copy.deepcopy(firstPath)
                expandedPath.append(states)
                self.queue.insert(0, expandedPath)

            flag = not flag
