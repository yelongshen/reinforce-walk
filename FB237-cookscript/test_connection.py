import os
import sys

def read_idx(mf, midx):
	f = file(mf)
	for line in f:
		items = line.strip().split('\t')
		n_str = items[0]
		n_id = int(items[1])
		midx[n_str] = n_id
	f.close()


def read_graph(mf, mgraph, ndict, ldict):
	f = file(mf)
	for line in f:
		items = line.strip().split('\t')
		n_1 = ndict[items[0]]
		n_2 = ndict[items[1]]
		n_link = ldict[items[2]]
		if(not mgraph.has_key(n_1)):
			mgraph[n_1] = {}
		if(not mgraph.has_key(n_2)):
			mgraph[n_2] = {}
		if(not mgraph[n_1].has_key(n_2)):
			mgraph[n_1][n_2] = 1
		if(not mgraph[n_2].has_key(n_1)):
			mgraph[n_2][n_1] = 1
			

node_idx = {}
rel_idx = {}
graph = {}

test_graph = {}
read_idx('entity2id.txt', node_idx)
read_idx('relation2id.txt', rel_idx)
read_graph('train.v2.txt', graph, node_idx, rel_idx)
read_graph('valid.v2.txt', test_graph, node_idx, rel_idx)

black = {}
for i in graph:
	n = len(graph[i])
	if(n > 200):
		black[i] = n

#remove black node in the training and testing graph.
def removeBlack(mgraph, mblack):
	for n in mgraph.keys():
		if(mblack.has_key(n)):
			for nei in mgraph[n].keys():
				del mgraph[nei][n]
			del mgraph[n]
removeBlack(graph, black)
removeBlack(test_graph, black)
def shortestpath(n1, n2, mgraph):
	seed = {}
	seed[n1] = 0;
	#if(n1 == n2):
	#	return 0
	for p in range(0,4):
		arrive = {}
		for x in seed:
			arrive[x] = seed[x]
		
		for x in seed:
			d = seed[x]
			if(not mgraph.has_key(x)):
				continue;
			for n in mgraph[x]:
				if(arrive.has_key(n)):
					continue
				dn = d + 1
				arrive[n] = dn
		seed = arrive
	
	if(seed.has_key(n2)):
		return seed[n2], len(seed)
	return -1, len(seed)
e = 0
avg = 0
pdict = {}
for n1 in test_graph:
	for n2 in test_graph[n1]:
		p,c = shortestpath(n1,n2,graph)
		if( p >= 0):
			avg = avg + 1.0 / c
		if(not pdict.has_key(p)):
			pdict[p] = 0
		pdict[p] = pdict[p] + 1
		e = e + 1
		if(e % 1000 == 0):
			print 'loading ',e, avg / e
print pdict