import networkx as nx
from multiprocessing import Pool
import itertools
from networkx.algorithms import bipartite

def average_dict(d):
    d_sum = 0
    for k, v in d.iteritems():
    	d_sum += v
    return d_sum/len(d)

def sum_dict(d):
    d_sum = 0
    for k, v in d.iteritems():
    	d_sum += v
    return d_sum

def chunks(l,n):
    """Divide a list of nodes `l` in `n` chunks"""
    l_c = iter(l)
    while 1:
        x = tuple(itertools.islice(l_c,n))
        if not x:
            return
        yield x

def _betreduce(bt1,bt2):
    """Sum betweenness values of two dictionaries with nodes as keys"""
    for n in bt1:
        bt1[n] += bt2[n]
    return bt1

def _betmap((G,normalized,weight,sources)):
    """Pool for multiprocess only accepts functions with one argument. This function
    uses a tuple as its only argument.
    """
    return nx.betweenness_centrality_source(G,normalized,weight,sources)

def betweenness_centrality_parallel(G,processes=None):
    """Parallel betweenness centrality  function"""
    p = Pool(processes=processes)
    node_divisor = len(p._pool)*4
    node_chunks = list(chunks(G.nodes(),G.order()/node_divisor))
    num_chunks = len(node_chunks)
    bt_sc = p.map(_betmap,
                  zip([G]*num_chunks,
                      [True]*num_chunks,
                      [None]*num_chunks,
                      node_chunks))
    bt_c = reduce(_betreduce,bt_sc)
    return bt_c
