import threading
import sys

class DFS:

    def __init__(self, callback):
        self.bests = []
        self.queue = []
        self.threads = []
        self.procedure = [0,1,2,3,4,5,6,7,8,9]
        self.callback = callback

    def countSolved(self, array):
        count = 0
        for i in range(len(array)):
            for j in range(len(array[i])):
                if array[i][j] != '1' and array[i][j] != '0':
                    count += 1
        return count

    def threading_wrap(self, start, goal):
        for i in range(1):
            self.threads.append(threading.Thread(target=self.depth_firts_search, args=(start, goal, i,)))
            self.threads[i].start()

        for i in range(1):
            self.threads[i].join()

        final_results = list(self.bests)
        final_results = list(filter(lambda x: self.countSolved(x.puzzle) < 9, final_results))
        print("Filtre? " + str(len(final_results)))
        return final_results

    def depth_firts_search(self, start, goal, id):
        # Form a one element queue consisting of start
        self.queue.insert(0, start)
        # While queue is not empty
        allProcedures = start.orderProcedure()
        for procedure in allProcedures:
            while self.queue:
                # Select randomly
                stateWillBeExpanded = self.queue[0]

                # If goal node is found in front of the queue, announce success
                if stateWillBeExpanded.puzzle == goal.puzzle:
                    print("Success: " + str(self.queue[0]) + "\n")
                    print(len(self.queue))
                    self.bests.append(self.queue[0])
                    return self.bests

                # Expand the state with min score
                newStates = stateWillBeExpanded.makeAllPlacements(procedure)

                if len(newStates) == 0:
                    self.bests.append(stateWillBeExpanded)

                # Delete the first path in queue
                del self.queue[0]

                # Add the newly expanded paths
                for states in newStates:
                    self.queue.insert(0, states)

        return self.bests
