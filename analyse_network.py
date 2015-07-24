import networkx as nx
import analyse_network_fun as anfun
import matplotlib.pyplot as plt
from matplotlib import pylab
from multiprocessing import Pool
import time
import itertools
import d3py
from networkx.readwrite import json_graph
from networkx.algorithms import bipartite

import networkx as nx
from multiprocessing import Pool
import itertools
from networkx.algorithms import bipartite

G=nx.Graph()

#file = open('enfermos100_apoptosis_all.sif', 'r')
#file = open('enfermos100_autofagia_all.sif', 'r')
#file = open('enfermos100_cluster_proliferativo_all.sif', 'r')
#file = open('enfermos100_p53_all.sif', 'r')

new_list = list()
new_lsort = list()

for line in file1:
    lsort = line.split();
    lsort.sort();
    new_lsort.append(lsort)
    new_list.append(lsort[1])
    new_list.append(lsort[2])
    
for line in file2:
    lsort = line.split();
    lsort.sort();
    new_lsort.append(lsort)
    new_list.append(lsort[1])
    new_list.append(lsort[2])
s_nodes = set(new_list)
G.add_nodes_from(list(s_nodes))

print "***      Graph Load Done!      ***"

edges = []

for lista in new_lsort:
   temp = (lista[1],lista[2])
   edges.append(temp)
edges_set = set(edges)
G.add_edges_from(list(edges_set))

#nx.average_neighbor_degree(G, weight='weight')
print nx.edge_betweenness_centrality(G, normalized=True, weight=None)
# "***Starting Analysis***"

clustering = nx.clustering(G)

#Neighbor_conectivity_Distribution
average_neighbors = nx.average_degree_connectivity(G)
#for k,v in average_neighbors.iteritems():
#    print "average_neighbors "+str(k)+","+str(v)

#for node in G.nodes():
#    print G.degree(node)

c_centrality =  nx.closeness_centrality(G)
d_centrality =  nx.degree_centrality(G)
betweeness_centrality = anfun.betweenness_centrality_parallel(G,8)

shortest_path_length = 0

radius = 1
diameter = 0 

for g in nx.connected_component_subgraphs(G):
    if nx.radius(g) < radius :
       radius = nx.radius(g)
    if nx.diameter(g)> diameter:
       diameter = nx.diameter(g)
   # print (nx.average_shortest_path_length(g))

print "clustering coefficient = " + str(anfun.average_dict(clustering))
print "number of conected components = " + str(nx.number_connected_components(G))
print "diameter = " + str(diameter) 
print "radius = " + str(radius) 
print "centralization = non connected graph"
print "shortest Paths (connPairs) = " 
print "characteristic Path Length= "
print "Average Neighbors ="
print "nodeCount=" +str(len(s_nodes))
print "density = " + str(anfun.average_dict(d_centrality))
print "density = " + str(nx.density(G))
print " heterogeneity="
print  nx.shortest_path_length(G)
print "betweeness centrality = " + str(anfun.average_dict(betweeness_centrality))





 



    #for k, v in nx.shortest_path(g).iteritems():
        #if len(v)>1 and len(v)<5:
	   #shortest_path += len(v)
	   #print len(v)
	#for kk,vv in v.iteritems():
	#    if len(vv)>1 and len(vv)<5:
	#        print len(vv)
	#        shortest_path += len(vv)
#print anfun.betweenness_centrality_parallel(G,8)
#print shortest_path_length


#print anfun.sum_dict(average_neighbors)
#print "avNeighbors =" + str(anfun.sum_dict(average_neighbors)/len(s_nodes))
#print "closenes= " + str(anfun.average_dict(c_centrality))
#print "betweenes centrality"
#print betweenness_centrality_parallel(G,8)
#print nx.betweenness_centrality(G, k=None, normalized=True, weight=None, endpoints=False, seed=None)
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
with d3py.NetworkXFigure(G, width=2000, height=2000) as p:
    p += d3py.ForceLayout()
    p.css['.node'] = {'fill': 'blue', 'stroke': 'magenta'}
    p.show()
#it can also be saved in .svg, .png. or .ps formats
