import itertools
import threading

from src.back_end.Data.data_reader import read_data_from_date


class DFS:

    def __init__(self, callback):
        self.bests = [[]]*1
        self.queue = [[]]*1
        self.threads = []
        self.procedure = [0,1,2,3,4,5,6,7,8,9]
        self.callback = callback


    def threading_wrap(self, start, goal, date):
        puzzle_json = read_data_from_date(date)
        sol = puzzle_json['solution_cells']

        def count_solved(array):
            count = 0
            for j in range(len(sol)):
                if array[sol[j]['y']-1][sol[j]['x']-1] == sol[j]['solution'].lower():
                    count += 1
            return count

        for i in range(1):
            self.threads.append(threading.Thread(target=self.depth_first_search, args=(start, goal, i,)))
            self.threads[i].start()

        for i in range(1):
            self.threads[i].join()

        # Join the threads' best results
        final_results = list(itertools.chain.from_iterable(self.bests))
        # Find the closest solution
        final_results = max(final_results, key=lambda x: count_solved(x.puzzle))
        print(final_results)
        return final_results

    def depth_first_search(self, start, goal, id):

        # While queue is not empty
        allProcedures = start.orderProcedure()

        for procedure in allProcedures:
            # Form a one element queue consisting of start
            self.queue[id] = [start]

            # While queue is not empty
            while (self.queue[id]):

                # Select randomly
                stateWillBeExpanded = self.queue[id][0]

                # If goal node is found in front of the queue, announce success
                if stateWillBeExpanded.puzzle == goal.puzzle:
                    print("Success: " + str(self.queue[id][0]) + "\n")
                    self.bests[id].append(self.queue[id][0])
                    return self.bests[id]

                # Expand the state with min score
                newStates = stateWillBeExpanded.makeAllPlacements(procedure)

                # Add the non-expandable states to the best results list
                if len(newStates) == 0:
                    self.bests[id].append(stateWillBeExpanded)

                # Delete the first path in queue
                del self.queue[id][0]

                # Add the newly expanded paths
                for states in newStates:
                    self.queue[id].insert(0, states)

        # Return the best results
        return self.bests
