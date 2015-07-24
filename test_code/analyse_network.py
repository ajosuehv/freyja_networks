import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import pylab
import operator
#import d3py
from networkx.readwrite import json_graph
G = nx.Graph()

#file = open('enfermos100_apoptosis_all.sif', 'r')
#file = open('enfermos100_autofagia_all.sif', 'r')
#file = open('enfermos100_cluster_proliferativo_all.sif', 'r')
#file = open('enfermos100_p53_all.sif', 'r')

new_list = list()
new_lsort = list()

for line in file:
    lsort = line.split();
    lsort.sort();
    new_lsort.append(lsort)
    new_list.append(lsort[1])
    new_list.append(lsort[2])
    
new_set = set(new_list)
G.add_nodes_from(list(new_set))

edges = []

for lista in new_lsort:
   temp = (lista[1],lista[2])
   edges.append(temp)
#print edges
#print new_set
edges_set = set(edges)

G.add_edges_from(list(edges_set))

#print nx.degree(G).values()
BC =  nx.betweenness_centrality(G, k=None, normalized=True, weight=None, endpoints=False, seed=None)
#print min(BC.items(), key=lambda x: x[1]) #min(BC, key=BC.get)
for i in xrange(1,101):
  MBC = max(BC.iteritems(), key=operator.itemgetter(1))
  print MBC
  del BC[MBC[0]]

#print nx.edge_betweenness_centrality(G, normalized=True, weight=None)

def save_graph(graph,file_name):
    #initialze Figure
    plt.figure(num=None, figsize=(500, 500), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph,pos)
    nx.draw_networkx_edges(graph,pos)
    nx.draw_networkx_labels(graph,pos)

    cut = 1.00
    xmax = cut * max(xx for xx, yy in pos.values())
    ymax = cut * max(yy for xx, yy in pos.values())
    plt.xlim(0, xmax)
    plt.ylim(0, ymax)

    plt.savefig(file_name,bbox_inches="tight")
    pylab.close()
    del fig

#print json_graph.node_link_data(G)

#Assuming that the graph g has nodes and edges entered
#save_graph(G,"my_graph.pdf")
#with d3py.NetworkXFigure(G, width=1000, height=1000) as p:
#    p += d3py.ForceLayout()
#    p.css['.node'] = {'fill': 'blue', 'stroke': 'magenta'}
#    p.show()
#it can also be saved in .svg, .png. or .ps formats
