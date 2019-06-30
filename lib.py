from numpy.random import ranf, randint
from numpy import diff, cumsum, multiply, prod
import itertools as it
import ast

def gen_signal(p, t, n=100, ran=10):
    k = randint(n-ran+1)
    x = []
    for i in range(n):
        if i >= k and i <= (k+ran):
            x.append(p[1]+t[1]*ranf())
        else:
            x.append(p[0]+t[0]*ranf())
    return x

def compress(x):
    dx = list(filter(lambda v: v.any(), diff(x, axis=0)))
    dx.insert(0,x[0])
    return cumsum(dx, axis=0)

def dsig(x,L,basis=False):
    if isinstance(x[0], (int, float)):
        x = [[val] for val in x]
    d = len(x[0])
    dx = diff(compress(x), axis=0)
    with open('compositions.txt', 'r') as fp:
        comps = list(it.islice(fp, 2**L-1))
        for comp in comps:
            comp = ast.literal_eval(comp)
            words = it.product(*[it.combinations_with_replacement(range(0,d),p) for p in comp])
            for word in words:
                inner = [1]*len(dx)
                for bracket in word:
                    outer = [prod([v[k] for k in bracket]) for v in dx]
                    inner = cumsum(multiply(inner,outer)).tolist()
                    last = inner.pop()
                    inner.insert(0,0)
                if basis:
                    yield (last,list(word))
                else:
                    yield last

def dsig_dist(x,y,dist,L):
    xsig = dsig(x,L)
    ysig = dsig(y,L)
    return sum([dist(a,b) for (a,_) in xsig for (b,_) in ysig])

def aP(n):
    """Generate partitions of n as ordered lists in ascending
    lexicographical order.

    This highly efficient routine is based on the delightful
    work of Kelleher and O'Sullivan.

    Examples
    ========

    >>> for i in aP(6): i
    ...
    [1, 1, 1, 1, 1, 1]
    [1, 1, 1, 1, 2]
    [1, 1, 1, 3]
    [1, 1, 2, 2]
    [1, 1, 4]
    [1, 2, 3]
    [1, 5]
    [2, 2, 2]
    [2, 4]
    [3, 3]
    [6]

    >>> for i in aP(0): i
    ...
    []

    References
    ==========

    .. [1] Generating Integer Partitions, [online],
        Available: http://jeromekelleher.net/generating-integer-partitions.html
    .. [2] Jerome Kelleher and Barry O'Sullivan, "Generating All
        Partitions: A Comparison Of Two Encodings", [online],
        Available: http://arxiv.org/pdf/0909.2331v2.pdf

    """
    # The list `a`'s leading elements contain the partition in which
    # y is the biggest element and x is either the same as y or the
    # 2nd largest element; v and w are adjacent element indices
    # to which x and y are being assigned, respectively.
    a = [1]*n
    y = -1
    v = n
    while v > 0:
        v -= 1
        x = a[v] + 1
        while y >= 2 * x:
            a[v] = x
            y -= x
            v += 1
        w = v + 1
        while x <= y:
            a[v] = x
            a[w] = y
            yield a[:w + 1]
            x += 1
            y -= 1
        a[v] = x + y
        y = a[v] - 1
        yield a[:w]
