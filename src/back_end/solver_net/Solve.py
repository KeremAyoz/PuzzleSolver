
import matplotlib.pyplot as plt
import networkx as nx

constraints = [((0, 0), (5, 0)),
               ((0, 1), (6, 0)),
               ((0, 2), (7, 0)),
               ((0, 3), (8, 0)),
               ((1, 0), (9, 0)),
               ((5, 1), (1, 1)),
               ((6, 1), (1, 2)),
               ((7, 1), (1, 3)),
               ((8, 1), (1, 4)),
               ((5, 2), (2, 1)),
               ((6, 2), (2, 2)),
               ((7, 2), (2, 3)),
               ((8, 2), (2, 4)),
               ((9, 1), (2, 0)),
               ((5, 3), (3, 1)),
               ((6, 3), (3, 2)),
               ((7, 3), (3, 3)),
               ((8, 3), (3, 4)),
               ((9, 2), (3, 0)),
               ((5, 4), (4, 1)),
               ((6, 4), (4, 2)),
               ((7, 4), (4, 3)),
               ((4, 0), (9, 3))]

clues = ["Pink floyd or Maroon 5", "Communicate between squad cars", "All by oneself", "Reddish-brown",
         "Corrosive cleaning compounds", "Pleasantly warm, as weather", "Maker of Flash Player and Photoshop",
         "Golf course halves", "Someone who isn't just all talk", "Castro who recently as Cuban president"]

l0 = ["band", "qwer"]
l1 = ["radio", "ratio"]
l2 = ["alone", "trump"]
l3 = ["umber", "under"]
l4 = ["lyes", "fres"]
l5 = ["balmy", "salmy"]
l6 = ["adobe", "grade"]
l7 = ["nines", "dedes"]
l8 = ["doer", "high"]
l9 = ["raul", "faul"]

wordLists = [l0, l1, l2, l3, l4, l5, l6, l7, l8, l9]

G = nx.Graph()

for i in range(len(wordLists)):
    for eachWord in wordLists[i]:
        # Currently checked node
        G.add_node((eachWord, i))
        for j in range(len(constraints)):
            if constraints[j][0][0] == i:
                reduced = list(filter(lambda x: x[constraints[j][1][1]] == eachWord[constraints[j][0][1]], wordLists[constraints[j][1][0]]))
                #Connect the satisfactory nodes in the graph to the node
                for newNodes in reduced:
                    # Connected node
                    G.add_node((newNodes, constraints[j][1][0]))
                    G.add_edge((eachWord, i), (newNodes, constraints[j][1][0]))
            elif constraints[j][1][0] == i:
                reduced = list(filter(lambda x: x[constraints[j][0][1]] == eachWord[constraints[j][1][1]],
                                      wordLists[constraints[j][0][0]]))
                # Connect the satisfactory nodes in the graph to the node
                for newNodes in reduced:
                    # Connected node
                    G.add_node((newNodes, constraints[j][0][0]))
                    G.add_edge((eachWord, i), (newNodes, constraints[j][0][0]), weight = j)

nx.draw_circular(G, with_labels = True)
plt.show()

