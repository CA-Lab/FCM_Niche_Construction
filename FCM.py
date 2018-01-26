# -*- coding: utf-8 -*-

"""
Modelacion de modelo mental con tres nodos basado
en el articulo de Salmeron 2013
"""
import pycxsimulator
import networkx as nx
import random as rd
import matplotlib.pyplot as plt
import math as mt
from pprint import pprint


U_global = []  # Utilidad global

state_h = []  # Estado del nodo happiness

state_g = []  # Estado del nodo greeness

state_n = []  # Estado del nodo neighbors happiness perception

positions = None

G = 0.8


def init():
    global time, g, U_global, state_h, state_g, state_n, positions

    time = 0

    g = nx.DiGraph()

    nds = ['h', 'g', 'n']

    g.add_nodes_from(nds)

    # El valor de los nodos esta entre 0 y 1 [0,1] y cuando es el caso,
    # la función es un sigmoidal Salmeron 2013:8

    g.add_edge('g', 'h', w=0.5)
    g.add_edge('n', 'h', w=1)
    g.add_edge('n', 'g', w=1)

    g.node['h']['s'] = 0
    g.node['g']['s'] = 0.1
    g.node['n']['s'] = 0

    positions = nx.random_layout(g)


def draw():
    plt.cla()
    nx.draw(g, edge_color='c',
            cmap=plt.cm.RdBu,
            vmin=0, vmax=1, alpha=0.75, pos=positions)
    nx.draw_networkx_labels(g, pos=positions)
    plt.axis('image')
    plt.title('t = ' + str(time))


def sigmoid(x):
    """ sigmoide """
    return 1 / (1 + mt.e ** -x)


def step():

    global time, g, U_global, state_h, state_g, state_n, G

    state_h.append(g.node['h']['s'])
    state_g.append(g.node['g']['s'])
    state_n.append(g.node['n']['s'])
    print g.node['h']['s'], g.node['g']['s'], g.node['n']['s']

    g1 = g.copy()

    g1.node['h']['s'] = sum([(g.node[j]['s'] * g[j]['h']['w'])
                             for j in g.predecessors('h')])
    g1.node['n']['s'] = sum([(g.node[j]['s'] * g[j]['n']['w'])
                             for j in g.predecessors('n')])
    g1.node['g']['s'] = sum([(g.node[j]['s'] * g[j]['g']['w'])
                             for j in g.predecessors('g')]) + G
    # Time
    time += 1

    g = g1.copy()


# Los FCM no actualizan los pesos de las conecciones,
# por eso añaden Hebbian learning

pycxsimulator.GUI().start(func=[init, draw, step])

pprint(state_h)

plt.cla()
plt.plot(state_h, 'r^', state_g, 'g^', state_n, 'b^')
plt.savefig('estados.png')
