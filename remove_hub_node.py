import os
import sys
import copy
import random

print 'usage: hub_threshold(int) output_path{str}'
if(len(sys.argv) < 2):
	print 'the number of parameters should be 2'

def read_idx(mf):
	midx = {}
	f = file(mf)
	for line in f:
		items = line.strip().split('\t')
		n_str = items[0]
		n_id = int(items[1])
		midx[n_str] = n_id
	f.close()
	return midx
node_idx = read_idx('FB237-raw/entity2id.txt')
rel_idx = read_idx('FB237-raw/relation2id.txt')

def read_graph_triple(mf, ndict, ldict):
	f = file(mf)
	mtriple = []
	for line in f:
		items = line.strip().split('\t')
		n_1 = ndict[items[0]]
		n_link = ldict[items[1]]
		n_2 = ndict[items[2]]
		mtriple.append([n_1, n_link, n_2])
	return mtriple

graph_triple = read_graph_triple('FB237-raw/train.txt', node_idx, rel_idx)
test_graph_triple = read_graph_triple('FB237-raw/test.txt', node_idx, rel_idx)
valid_graph_triple = read_graph_triple('FB237-raw/valid.txt', node_idx, rel_idx)


def triple2graph(mtriple, relNum):
	mgraph = {}
	for t in mtriple:
		n_1 = t[0]
		n_link = t[1]
		n_2 = t[2]
		
		# append direct link into graph.
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
		mgraph[n_2][n_1].append(n_link + relNum)
	return mgraph
graph = triple2graph(graph_triple, len(rel_idx))
test_graph = triple2graph(test_graph_triple, len(rel_idx))
valid_graph = triple2graph(valid_graph_triple, len(rel_idx))

hub_threshold = int(sys.argv[1])

hub_nodes = {}
for i in graph:
	n = len(graph[i])
	if(n > hub_threshold):
		hub_nodes[i] = n

def removeHubinGraph(mgraph, mhub):
	for n in mgraph.keys():
		if(mhub.has_key(n)):
			for nei in mgraph[n].keys():
				del mgraph[nei][n]
			del mgraph[n]
#remove hub node in the training, testing and dev graph.
removeHubinGraph(graph, hub_nodes)
removeHubinGraph(test_graph, hub_nodes)
removeHubinGraph(valid_graph, hub_nodes)

def removeHubinTriple(mtriple, hub_nodes):
	num = len(mtriple)
	for i in range(0, num):
		j = num - 1 - i
		t = mtriple[j]
		
		n1 = t[0]
		r = t[1]
		n2 = t[2]
		if(hub_nodes.has_key(n1) or hub_nodes.has_key(n2)):
			del mtriple[j]
			continue

removeHubinTriple(graph_triple, hub_nodes)
removeHubinTriple(test_graph_triple, hub_nodes)
removeHubinTriple(valid_graph_triple, hub_nodes)

def saveTriple(mtriple, fn):
	mf = file(fn,'w')
	for t in mtriple:
		mf.write(str(t[0])+'\t'+str(t[1])+'\t'+str(t[2])+'\n')
	mf.close()
op = sys.argv[2]
saveTriple(graph_triple, op+'/train.txt')
saveTriple(test_graph_triple, op+'/test.txt')
saveTriple(valid_graph_triple, op+'/valid.txt')

print 'remove hub nodes with over ', hub_threshold, ' neighbors'
print 'cooked train data : ',len(graph_triple)
print 'cooked test data : ',len(test_graph_triple)
print 'cooked valid data : ',len(valid_graph_triple)

