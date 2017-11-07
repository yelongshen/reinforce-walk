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

read_idx('entity2id.txt', node_idx)
read_idx('relation2id.txt', rel_idx)
read_graph('train.v2.txt', graph, graph_triple, node_idx, rel_idx)
read_graph('valid.v2.txt', test_graph, test_graph_triple, node_idx, rel_idx)

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

new_train = file('train.v3.txt','w')
new_p = file('train_path.v3.txt','w')
num = 0
pnum = 0
for t in graph_triple:
	n1 = t[0]
	r = t[1]
	n2 = t[2]
	if(black.has_key(n1) or black.has_key(n2)):
		continue
	
	new_train.write(str(n1)+"\t"+str(n2)+"\t"+str(r)+"\n")
	
	p = SamplePath(n1, n2, r, graph)
	
	if(len(p) == 0):
		new_p.write("\n")
	else:
		mline = ""
		for stop in p:
			mline = mline + str(stop[0])+","+str(stop[1])+","+str(stop[2])+"|||"
		new_p.write(mline+"\n")
		pnum = pnum + 1
	num = num + 1
	if(num % 10 == 0):
		print num, pnum
new_train.close()
new_p.close()