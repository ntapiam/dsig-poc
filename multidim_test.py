import lib
import util.tsreader as ts
import numpy as np

def knn_pred(x,data):
    dmatrix = []
    for v in data:
        dmatrix.append(np.linalg.norm(x-v[0],1))
    k = np.argmin(dmatrix)
    return data[k][1]

dataset = 'AtrialFibrillation'
basename = 'Multivariate2018_ts'
fr_train = ts.TSReader(basename + '/' + dataset + '/' + dataset + '_TRAIN.ts')
fr_test = ts.TSReader(basename + '/' + dataset + '/' + dataset + '_TEST.ts')

print('computing training set')
sig_train = [(np.array(list(lib.dsig(list(x),3))), y) for (x,y) in fr_train.read_data()]

correct = 0

for x,y in fr_test.read_data():
    x = np.array(list(lib.dsig(list(x), 3)))
    print(len(x), list(x))
    pclass = knn_pred(x, sig_train)
    print('predicted:', pclass, 'correct:', y)
    if pclass == y:
        correct += 1

rate = (1-correct/len(sig_test))*100
print('error rate: %f%%' % rate)
