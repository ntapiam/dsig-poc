from lib import *
from dtw import dtw
import numpy as np
from math import sqrt
import time

# generate samples for each class
def generate_data(p, t, n=100):
	x = []
	y = []
	for k in range(n):
		x.append(gen_signal(p[0][:],t))
		y.append(gen_signal(p[1][:],t))

	# prepare data
	data = np.append(x,y,axis=0)
	labels = np.array([0]*n+[1]*n)
	return data, labels

# some functions
def twidist(x,y):
	d, _, _, _ = dtw(compress(x),compress(y), lambda a,b: (b-a)**2)
	return sqrt(d)

def dsdist(x,y):
	xsig = dsig(x,6)
	ysig = dsig(y,6)
	return sqrt(sum([(b-a)**2 for (a,_) in xsig for (b,_) in ysig]))

def knn_pred(x,data,dist):
	dmatrix = []
	for v in data:
		dmatrix.append(dist(x,v[0]))
	k = np.argmin(dmatrix)
	return data[k][1]

# split data into training and target
def prepare_data(data, labels):
	train_idx = np.random.choice(len(data), round(len(data)*0.5), replace=False)
	test_idx = np.array(list(set(range(len(data)))-set(train_idx)))
	x_train = data[train_idx]
	y_train = labels[train_idx]
	x_test = data[test_idx]
	y_test = labels[test_idx]
	return list(zip(x_train, y_train)), list(zip(x_test, y_test))


# test twi distance
def test_twi(train, test):
	correct = 0
	t = time.perf_counter()
	for x in test:
		k = knn_pred(x[0], train, twidist)
		if k == x[1]:
			correct += 1
	print("processed %i inputs in %f s" % (len(test), time.perf_counter()-t))
	rate = (1-correct/len(test))*100
	print("twi error rate: %f \n" % rate)
	return rate

def test_dsig(train, test):
	correct = 0
	L = 10 #signature level
	# compute all signatures
	print("computing signatures")
	x_train = [a[0] for a in train]
	x_test = [a[0] for a in test]
	t = time.perf_counter()
	sig_train = [(np.array(dsig(x,L)),y) for (x,y) in train]
	sig_test = [(np.array(dsig(x,L)),y) for (x,y) in test]
	t2 = time.perf_counter()
	print("computed %i level %i signatures in %f seconds" % (len(train)+len(test),L,t2-t))
	for x in sig_test:
		k = knn_pred(x[0], sig_train, lambda a,b: np.linalg.norm(b-a))
		if k == x[1]:
			correct += 1

	endtime = time.perf_counter()
	print("processed %i inputs in %f s" % (len(x_test), endtime-t2))
	print("total process time %f s" % (endtime-t))
	rate = (1-correct/len(x_test))*100
	print("dsig error rate: %f \n" % rate)
	return rate

errors = []
for k in range(50):
	data, labels = generate_data([[0,1],[-.05, 1]],[0,1])
	train, test = prepare_data(data, labels)
	errors.append(test_twi(train, test))

print("tested twi distance 50 times, mean error:", np.mean(errors),"\n")

errors = []
for k in range(50):
	data, labels = generate_data([[0,1],[-.05, 1]],[0,1])
	train, test = prepare_data(data, labels)
	errors.append(test_dsig(train, test))

print("tested dsig distance 50 times, mean error:", np.mean(errors))
