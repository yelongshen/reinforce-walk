import os
import sys

ftrain = 'train.v2.txt'
ftest = 'test.v2.txt'
fvalid = 'valid.v2.txt'

edict = {}
rdict = {}
def pushDict(mkey, mdict):
    if(not mdict.has_key(mkey)):
        mdict[mkey] = len(mdict)
    return mdict[mkey]

def saveDict(mdict, fn):
    f = file(fn, 'w')
    for mkey in mdict:
        f.write(mkey+'\t'+str(mdict[mkey])+'\n')
    f.close()
def loadDict(fn):
    f = file(fn)
    for line in f:
        items = line.strip().split('\t')
        e1 = items[0]
        e2 = items[1]
        r = items[2]
        pushDict(e1, edict)
        pushDict(e2, edict)
        pushDict(r, rdict)
    f.close()


loadDict(ftrain)
loadDict(ftest)
loadDict(fvalid)
saveDict(edict,'entity2id.txt')
saveDict(rdict,'relation2id.txt')
