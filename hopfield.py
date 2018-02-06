import networkx as nx


w = [[0, -1, 1],
     [1, 0, 1],
     [-1, 1, 0]]

g = nx.DiGraph()

for i in range(len(w)):
    for j in range(len(w[i])):
        g.add_edge(i, j, w=w[i][j])
