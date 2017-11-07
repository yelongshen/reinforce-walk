import os
import sys

print 'usage: data_folder(str) max_path_len(int)'
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


def read_graph_triple(mf):
	f = file(mf)
	mtriple = []
	for line in f:
		items = line.strip().split('\t')
		n_1 = int(items[0])
		n_link = int(items[1])
		n_2 = int(items[2])
		mtriple.append([n_1, n_link, n_2])
	return mtriple

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
folder = sys.argv[1]
graph_triple = read_graph_triple(folder + '/train.txt')
test_graph_triple = read_graph_triple(folder + '/test.txt')
valid_graph_triple = read_graph_triple(folder + '/valid.txt')

graph = triple2graph(graph_triple, len(rel_idx))
test_graph = triple2graph(test_graph_triple, len(rel_idx))
valid_graph = triple2graph(valid_graph_triple, len(rel_idx))


def SearchNHopNeighbors(n1, n2, mgraph, mp):
	seed = {}
	seed[n1] = 0;
	for p in range(0,mp):
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

def test_graph_connect(base_g, test_g, maxP):
	e = 0
	avg = 0
	pdict = {}
	for n1 in test_g:
		for n2 in test_g[n1]:
			p,c = SearchNHopNeighbors(n1,n2,base_g,maxP)
			if( p >= 0):
				avg = avg + 1.0 / c
			if(not pdict.has_key(p)):
				pdict[p] = 0
			pdict[p] = pdict[p] + 1
			e = e + 1
			if(e % 1000 == 0):
				print 'loading ',e, avg / e
	print pdict
	unreach = 0
	if(pdict.has_key(-1)):
		unreach = pdict[-1]
	print 'success reach pair :', e - unreach
	print 'unreach pair :', unreach 
	print 'reachable percentage : ', (e-unreach) * 1.0 / e
maxPath = int(sys.argv[2])

print 'test data connectivity'
test_graph_connect(graph, test_graph, maxPath)

print 'valid data connectivity'
test_graph_connect(graph, valid_graph, maxPath)
