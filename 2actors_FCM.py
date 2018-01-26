# -*- coding: utf-8 -*-

"""Modelacion de modelo mental con tres nodos basado en el articulo de Salmeron 2013"""

import networkx as nx
import random as rd
import matplotlib.pyplot as plt
import math as mt

#initialization

#time = [] tiempo

U_global = [] #Utilidad global

state_1h = [] #Estado del nodo happiness

state_1g = [] #Estado del nodo greeness

state_1n = [] #Estado del nodo neighbors happiness perception

state_2h = [] #Estado del nodo happiness

state_2g = [] #Estado del nodo greeness

state_2n = [] #Estado del nodo neighbors happiness perception

def init():
    global time, f, g, z, U_global, state_1h, state_1g, state_1n, state_2h, state_2g, state_2n

    time = 0
    
    g = nx.DiGraph()

    f = nx.DiGraph()

    #h = nx.DiGraph()

    #nds = ['1h','1g','1n']

    agnt1 = ['1h','1g','1n']

    agnt2 = ['2h','2g','2n']
    
    f.add_nodes_from(agnt1)

    g.add_nodes_from(agnt2)

    #h.add_nodes_from(nds)

#El valor de los nodos esta entre 0 y 1 [0,1] y cuando es el caso, la función es un sigmoidal Salmeron 2013:8    
    
    for i in g.nodes():
        for j in f.nodes():
            if i != j:
                f.add_edge(i, j)
                f.add_edge(j,i)


    for i in g.nodes():
        for j in g.nodes():
            if i != j:
                g.add_edge(i, j)
                g.add_edge(j,i)


    z = nx.compose(f,g)            

    z.add_edge('1h','2n') ###Connecting happines node of agent 1 to the nieghbors node of agent2, as agent 2  perceives the happines of agent 1### 
    z.add_edge('2h','1n') ###Connecting happines node of agent 2 to the nieghbors node of agent1, as agent 1  perceives the happines of agent 2### 

    
    for i in z.nodes():
        z.node[i]['s'] = 0


    for i,j in z.edges():
        z[i][j]['w'] = rd.random()

    positions = nx.random_layout(z)

def draw():

    plt.cla()
    #nodeSize = [100*g.node[i]['s'] for i in g.nodes(g)]
    nx.draw(z, edge_color = 'c', cmap = plt.cm.RdBu, vmin = 0, vmax = 1, alpha=0.75)
    plt.axis('image')
    plt.title('t = ' + str(time))
    
#Steps

def sigmoid(x):

    return 1 / (1 + mt.e ** -x) #función sigmoide

def step():

    global time, f, g, z, U_global, state_1h, state_1g, state_1n, state_2h, state_2g, state_2n
    time +=1
    
    for i in z.nodes():
    #i_state = f(g.node[i]['s'] + sum(wij) g.neighbors['s'])    

        suma_Wij = 0

        for j in z.neighbors(i):
            suma_Wij += z[i][j]['w'] * z.node[j]['s']
            
        z.node[i]['s']= sigmoid(z.node[i]['s'] + suma_Wij)

        #print g.node[i]['s']

        if z.node[i] == z.node['1h']:
            state_1h.append(z.node[i]['s'])
        if z.node[i] == z.node['1g']:
            state_1g.append(z.node[i]['s'])
        if z.node[i] == z.node['1n']:
            state_1n.append(z.node[i]['s'])

        if z.node[i] == z.node['2h']:
            state_2h.append(z.node[i]['s'])
        if z.node[i] == z.node['2g']:
            state_2g.append(z.node[i]['s'])
        if z.node[i] == z.node['2n']:
            state_2n.append(z.node[i]['s'])

        for i in z.nodes():
            suma =  z.node['1h']['s'] + z.node['1g']['s'] + z.node['1n']['s'] + z.node['2h']['s'] + z.node['2g']['s'] + z.node['2n']['s']
        U_global.append(suma)

            
    
#Los FCM no actualizan los pesos de las conecciones, por eso añaden Hebbian learning


import pycxsimulator
pycxsimulator.GUI().start(func=[init,draw,step])


plt.cla()
#plt.plot(time_list, energy_state_g, 'b+')
#plt.plot(time_list, energy_state_o, 'r-')
fig, (ax1, ax2) = plt.subplots(2, sharey=True)
ax1.plot(state_1h, 'r^', state_1g, 'g^', state_1n, 'b^')
ax1.set(title= 'Local states', ylabel='Nodes state')
ax2.plot(state_2h, 'rs', state_2g, 'gs', state_2n, 'bs')
ax2.set(title= 'Time', ylabel='Nodes state')
#ax2.plot(U_global, 'bo')
#ax2.set(xlabel='Time', ylabel='Global state')
fig.savefig('estados.svg')

plt.cla()
plt.plot(U_global, 'bo')
plt.savefig('global.svg')
#plt.savefig('learning_plot_erdos.svg')


# nx.draw(g)
# pl.show()
