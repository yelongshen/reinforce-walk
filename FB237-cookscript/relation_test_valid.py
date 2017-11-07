import os
import sys
import copy
import random
def read_idx(mf, midx):
	f = file(mf)
	for line in f:
		items = line.strip().split('\t')
		n_str = items[0]
		n_id = int(items[1])
		midx[n_str] = n_id
	f.close()

def read_graph(mf, mgraph, mtriple, ndict, ldict):
	f = file(mf)
	for line in f:
		items = line.strip().split('\t')
		n_1 = ndict[items[0]]
		n_2 = ndict[items[1]]
		n_link = ldict[items[2]]
		# append link into graph.
		if(not mgraph.has_key(n_1)):
			mgraph[n_1] = {}
		if(not mgraph[n_1].has_key(n_2)):
			mgraph[n_1][n_2] = []
		mgraph[n_1][n_2].append(n_link)
		
		# append reverse link into graph.
		if(not mgraph.has_key(n_2)):
			mgraph[n_2] = {}
		if(not mgraph[n_2].has_key(n_1)):
			mgraph[n_2][n_1] = []
		mgraph[n_2][n_1].append(n_link + len(ldict))
		
		mtriple.append([n_1, n_link, n_2])

node_idx = {}
rel_idx = {}

graph = {}
graph_triple = []

test_graph = {}
test_graph_triple = []

valid_graph = {}
valid_graph_triple = []


read_idx('entity2id.txt', node_idx)
read_idx('relation2id.txt', rel_idx)
read_graph('train.v2.txt', graph, graph_triple, node_idx, rel_idx)
read_graph('test.v2.txt', test_graph, test_graph_triple, node_idx, rel_idx)
read_graph('valid.v2.txt', valid_graph, valid_graph_triple, node_idx, rel_idx)

black = {}
for i in graph:
	n = len(graph[i])
	if(n > 100):
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
removeBlack(valid_graph, black)
def revR(r):
	global rel_idx
	if(r >= len(rel_idx)):
		return r - len(rel_idx)
	else:
		return r + len(rel_idx)

def SampleNextEdge(n1, n2, r, n, path, mgraph):
	mlink = []
	for nei in mgraph[n]:
		for nei_r in mgraph[n][nei]:
			if(n == n1 and nei == n2 and r == nei_r):
				continue
			if(n == n2 and nei == n1 and revR(r) == nei_r):
				continue
			if([n, nei_r, nei] in path):
				continue
			if([nei, revR(nei_r), n] in path):
				continue
			mlink.append([n, nei_r, nei])
	
	if(len(mlink) == 0):
		return [n, -1, -1]
		# return empty node
	ln = len(mlink)
	s = random.randint(0, ln-1)
	return mlink[s]
	
def SamplePath(n1, n2, r, mgraph):
	for i in range(0, 5000):
		path = []
		isfound = False
		n = n1
		for f in range(0,5):
			p = SampleNextEdge(n1, n2, r, n, path, mgraph)
			if(p[2] == -1):
				break
			path.append(p)
			
			n = p[2]
			if(n == n2):
				isfound = True
				break
			
		if(isfound):
			return path
	return []

def stat_remove_hubnode(mtriple, mblack, rdict, ndict):
	num = 0
	for t in graph_triple:
		n1 = t[0]
		r = t[1]
		n2 = t[2]
		if(mblack.has_key(n1) or mblack.has_key(n2)):
			continue
		
		if(not rdict.has_key(r)):
			rdict[r] = 0
		if(not ndict.has_key(n1)):
			ndict[n1] = 0
		if(not ndict.has_key(n2)):
			ndict[n2] = 0
		rdict[r] = rdict[r] + 1
		num = num + 1
		#if(num % 1000 == 0):
		#	print num
rt_dict = {}
nt_dict = {}
print 'test', len(test_graph_triple)
stat_remove_hubnode(test_graph_triple, black, rt_dict, nt_dict)
print 'test r', len(rt_dict), 'test n', len(nt_dict)

rv_dict = {}
nv_dict = {}
print 'valid', len(valid_graph_triple)
stat_remove_hubnode(valid_graph_triple, black, rv_dict, nv_dict)
print 'valid r', len(rv_dict), 'valid n', len(nv_dict)

def overlap(d1, d2):
	o = 0;
	for mk in d1:
		if(d2.has_key(mk)):
			o = o + 1
	return o

r_o = overlap(rt_dict,rv_dict)
print 'overlap r', r_o

n_o = overlap(nt_dict,nv_dict)
print 'overlap n', n_o
