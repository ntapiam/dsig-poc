#!/usr/bin/env python3
import lib
import util.tsreader as ts
import numpy as np

def knn_pred(x,data):
    dmatrix = []
    for v in data:
        dmatrix.append(np.linalg.norm(x-v[0],1))
    k = np.argmin(dmatrix)
    return data[k][1]

L = 2

dataset = 'UWaveGestureLibrary'
basename = 'Multivariate2018_ts'
fr_train = ts.TSReader(basename + '/' + dataset + '/' + dataset + '_TRAIN.ts')
fr_test = ts.TSReader(basename + '/' + dataset + '/' + dataset + '_TEST.ts')

print('computing training set')
sig_train = [(np.array(list(lib.dsig(list(x),L))), y) for (x,y) in fr_train.read_data()]

correct = 0
total = 0

for x,y in fr_test.read_data():
    x = np.array(list(lib.dsig(list(x), L)))
    pclass = knn_pred(x, sig_train)
    print('predicted:', pclass, 'correct:', y)
    if pclass == y:
        correct += 1
    total += 1

rate = (1-correct/total)*100
print('error rate: %f%%' % rate)
