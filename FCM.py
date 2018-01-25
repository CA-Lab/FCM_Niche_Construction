# -*- coding: utf-8 -*-

"""Modelacion de modelo mental con tres nodos basado en el articulo de Salmeron 2013"""

import networkx as nx
import random as rd
import matplotlib.pyplot as plt
import math as mt

#initialization

#time = [] tiempo

U_global = [] #Utilidad global

state_h = [] #Estado del nodo happiness

state_g = [] #Estado del nodo greeness

state_n = [] #Estado del nodo neighbors happiness perception

def init():
    global time, g, U_global, state_h, state_g, state_n

    time = 0
    
    g = nx.DiGraph()

    #h = nx.DiGraph()

    nds = ['h','g','n']
    
    g.add_nodes_from(nds)

    #h.add_nodes_from(nds)

#El valor de los nodos esta entre 0 y 1 [0,1] y cuando es el caso, la función es un sigmoidal Salmeron 2013:8    
    
    for i in g.nodes():
        for j in g.nodes():
            if i != j:
                g.add_edge(i, j)
                g.add_edge(j,i)


    for i in g.nodes():
        g.node[i]['s'] = 0


    for i,j in g.edges():
        g[i][j]['w'] = rd.random()

    positions = nx.random_layout(g)

def draw():

    plt.cla()
    #nodeSize = [100*g.node[i]['s'] for i in g.nodes(g)]
    nx.draw(g, edge_color = 'c', cmap = plt.cm.RdBu, vmin = 0, vmax = 1, alpha=0.75)
    plt.axis('image')
    plt.title('t = ' + str(time))
    
#Steps

def sigmoid(x):

    return 1 / (1 + mt.e ** -x) #función sigmoide

def step():

    global time, g, U_global, state_h, state_g, state_n
    time +=1
    
    for i in g.nodes():
    #i_state = f(g.node[i]['s'] + sum(wij) g.neighbors['s'])    

        suma_Wij = 0

        for j in g.neighbors(i):
            suma_Wij += g[i][j]['w'] * g.node[j]['s']
            
        g.node[i]['s']= sigmoid(g.node[i]['s'] + suma_Wij)

        #print g.node[i]['s']

        if g.node[i] == g.node['h']:
            state_h.append(g.node[i]['s'])
        if g.node[i] == g.node['g']:
            state_g.append(g.node[i]['s'])
        if g.node[i] == g.node['n']:
            state_n.append(g.node[i]['s'])

        for i in g.nodes():
            suma =  g.node['h']['s'] + g.node['g']['s'] + g.node['n']['s']
        U_global.append(suma)

            
        #print state_h
        #print state_g
        #print state_n

#Los FCM no actualizan los pesos de las conecciones, por eso añaden Hebbian learning


import pycxsimulator
pycxsimulator.GUI().start(func=[init,draw,step])


plt.cla()
#plt.plot(time_list, energy_state_g, 'b+')
#plt.plot(time_list, energy_state_o, 'r-')
fig, (ax1, ax2) = plt.subplots(2, sharey=True)
ax1.plot(state_h, 'r^', state_g, 'g^', state_n, 'b^' )
ax1.set(title= 'Local and global states', ylabel='Nodes state')
ax2.plot(U_global, 'bo')
ax2.set(xlabel='Time', ylabel='Global state')
fig.savefig('estados.svg')
#plt.savefig('learning_plot_small.svg')
#plt.savefig('learning_plot_erdos.svg')


# nx.draw(g)
# pl.show()
