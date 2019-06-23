from lib import *
import numpy as np
import time
import os

# some functions
def knn_pred(x,data,dist):
	dmatrix = []
	for v in data:
		dmatrix.append(dist(x,v[0]))
	k = np.argmin(dmatrix)
	return data[k][1]

def test_dsig(train, test):
	correct = 0
	L = 4 #signature level
	# compute all signatures
	print("computing signatures")
	t = time.perf_counter()
	sig_train = [(np.array(dsig(x,L)),y) for (x,y) in train]
	sig_test = [(np.array(dsig(x,L)),y) for (x,y) in test]
	dt2 = time.perf_counter()-t
	print("computed %i level %i signatures in %f seconds" % (len(train)+len(test),L,dt2))
	for x in sig_test:
		k = knn_pred(x[0], sig_train, lambda a,b: np.linalg.norm(b-a))
		if k == x[1]:
			correct += 1
	dt = time.perf_counter()-t
	print("processed %i inputs in %f s" % (len(sig_test), dt-dt2))
	print("total process time %f s" % dt)
	rate = (1-correct/len(sig_test))*100
	print("dsig error rate: %f \n" % rate)
	return rate, dt

errors = {}
runtime = {}
# execute tests for each dir
with open('results.txt', 'a') as fout:
	for dirname, subdirs, files in os.walk('UCRArchive_2018/'):
		train = []
		test = []
		basename = os.path.basename(dirname)
		if not basename: continue
		print("Getting data from:", basename)
		with open(dirname + '/' + basename + '_TRAIN.tsv', 'r') as fp:
			for line in fp:
				sample = line.split('\t')
				train.append((list(map(float,sample[1:])),int(sample[0])))
		with open(dirname + '/' + basename + '_TEST.tsv', 'r') as fp:
			for line in fp:
				sample = line.split('\t')
				test.append((list(map(float,sample[1:])),int(sample[0])))
		rate, dt = test_dsig(train, test)
		fout.write("%s %f %f\n" % (basename, rate, dt))
		errors[basename] = rate
		runtime[basename] = dt

print("Total running time:", sum(runtime.values()))
