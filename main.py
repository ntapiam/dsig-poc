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
        x.append(gen_signal(p[0][:], t))
        y.append(gen_signal(p[1][:], t))

    # prepare data
    data = np.append(x, y, axis=0)
    labels = np.array([0]*n+[1]*n)
    return data, labels


# some functions
def twidist(x, y):
    d, _, _, _ = dtw(compress(x), compress(y), lambda a, b: (b-a)**2)
    return sqrt(d)


def dsdist(x, y):
    xsig = dsig(x, 6)
    ysig = dsig(y, 6)
    return sqrt(sum([(b-a)**2 for (a, _) in xsig for (b, _) in ysig]))


def knn_pred(x, data, dist):
    dmatrix = []
    for v in data:
        dmatrix.append(dist(x, v[0]))
    k = np.argmin(dmatrix)
    return data[k][1]


# split data into training and target
def prepare_data(data, labels):
    train_idx = np.random.choice(len(data), round(len(data)*0.8), replace=False)
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
    dt = time.perf_counter() - t
    print("processed %i inputs in %f s" % (len(test), dt))
    rate = (1-correct/len(test))*100
    print("twi error rate: %f \n" % rate)
    return rate, dt


def test_dsig(train, test):
    correct = 0
    L = 3  # signature level
    # compute all signatures
    print("computing signatures")
    t = time.perf_counter()
    sig_train = [(np.array(dsig(x, L)), y) for (x, y) in train]
    sig_test = [(np.array(dsig(x, L)), y) for (x, y) in test]
    dt2 = time.perf_counter()-t
    print("computed %i level %i signatures in %f seconds" % (len(train)+len(test), L, dt2))
    for x in sig_test:
        k = knn_pred(x[0], sig_train, lambda a, b: np.linalg.norm(b-a))
        if k == x[1]:
            correct += 1
    dt = time.perf_counter()-t
    print("processed %i inputs in %f s" % (len(sig_test), dt2))
    print("total process time %f s" % dt)
    rate = (1-correct/len(sig_test))*100
    print("dsig error rate: %f \n" % rate)
    return rate, dt


if __name__ == "__main__":
    errors_twi = []
    errors_dsig = []
    time_twi = []
    time_dsig = []
    N = 50
    for k in range(N):
        print("k = %i --------" % k)
        data, labels = generate_data([[0, 1], [-.05, 1]], [0, 1])
        train, test = prepare_data(data, labels)
        rate, dt = test_twi(train, test)
        errors_twi.append(rate)
        time_twi.append(dt)
        rate, dt = test_dsig(train, test)
        errors_dsig.append(rate)
        time_dsig.append(dt)

    print("tested twi distance %i times, mean error:" % N, np.mean(errors_twi), ", total time: %f s" % sum(time_twi))
    print("tested dsig distance %i times, mean error:" % N, np.mean(errors_dsig), ", total time: %f s" % sum(time_dsig))
