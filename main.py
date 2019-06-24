#!/usr/bin/env python3
from lib import *
import numpy as np
import time
import os
from math import isnan
import datetime
import argparse

# some functions
def knn_pred(x,data,dist):
    dmatrix = []
    for v in data:
        dmatrix.append(dist(x,v[0]))
    k = np.argmin(dmatrix)
    return data[k][1]

def test_dsig(train, test, dist, L=4):
    correct = 0
    # compute all signatures
    print("computing signatures")
    t = time.perf_counter()
    sig_train = [(np.array(dsig(x,L)),y) for (x,y) in train]
    sig_test = [(np.array(dsig(x,L)),y) for (x,y) in test]
    dt2 = time.perf_counter()-t
    print("computed %i level %i signatures in %f seconds" % (len(train)+len(test),L,dt2))
    for x in sig_test:
        k = knn_pred(x[0], sig_train, dist)
        if k == x[1]:
            correct += 1
    dt = time.perf_counter()-t
    print("processed %i inputs in %f s" % (len(sig_test), dt-dt2))
    print("total process time %f s" % dt)
    rate = (1-correct/len(sig_test))*100
    print("dsig error rate: %f \n" % rate)
    return rate, dt

def distance(a,b):
    return np.linalg.norm(b-a, p)

errors = {}
runtime = {}
parser = argparse.ArgumentParser(description='Run tests on the UCR Archive 2018')
parser.add_argument('L', nargs='?', default=4, type=int, choices=range(1,11), help='Max. signature level. Must be between 1 and 10 (default: 4)', metavar='L')
parser.add_argument('p', nargs='?', default=1, type=float, help='Norm exponent (default: 1)')
args = parser.parse_args()
p = args.p
L = args.L
# execute tests for each dir
now = datetime.datetime.now()
filename = 'results_' + now.strftime('%Y%m%d_%H%M%S') + '.txt'
with open(filename, 'w') as fout:
    fout.write('Parameters: L=%i p=%f\n' % (L,p))
    fout.write('Dataset\tError rate\tTime\n')
    for dirname, subdirs, files in os.walk('UCRArchive_2018/'):
        train = []
        test = []
        basename = os.path.basename(dirname)
        if not basename: continue
        print("Getting data from:", basename)
        with open(dirname + '/' + basename + '_TRAIN.tsv', 'r') as fp:
            for line in fp:
                sample = line.split('\t')
                train.append((list(filter(lambda p: not isnan(p), map(float,sample[1:]))),int(sample[0])))
        with open(dirname + '/' + basename + '_TEST.tsv', 'r') as fp:
            for line in fp:
                sample = line.split('\t')
                test.append((list(filter(lambda p: not isnan(p), map(float,sample[1:]))),int(sample[0])))
        rate, dt = test_dsig(train, test, distance, L)
        fout.write("%s\t%f\t%f\n" % (basename, rate, dt))
        errors[basename] = rate
        runtime[basename] = dt
    fout.write("\nTotal time: %f\n" % sum(runtime.values()))

print("Total running time:", sum(runtime.values()))
