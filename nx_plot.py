import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(g):
    plt.figure()
    pos = nx.circular_layout(g, scale=0.5)

    node_scale = 11000

    nx.draw_networkx_nodes(g, pos,
                           node_size=[node_scale * g.node[n]['dvc']
                                      for n in g.nodes],
                           node_color="grey")

    nx.draw_networkx_labels(g,
                            pos,
                            labels={n: "c%s DVC=%s" % (n, g.node[n]['dvc'])
                                    for n in g.nodes},
                            font_color='white',
                            font_size=9,
                            font_family='sans-serif')

    nx.draw_networkx_edges(g, pos,
                           width=6,
                           alpha=0.5,
                           edge_color='black')

    nx.draw_networkx_edge_labels(g, pos,
                                 {e: g.get_edge_data(*e)['weight']
                                  for e in g.edges},
                                 label_pos=0.3)

    plt.axis('off')  # don't print useless scale
    

