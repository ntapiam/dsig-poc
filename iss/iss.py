import itertools as it
import functools as fnt
import numpy as np



def _compress(x):
    """Compresses a time series by deleting repeated values

    :param x: Time series to be compressed
    :returns: The compressed version of x
    :rtype: list
    """

    # Compute all increments and keep only the non-zero entries
    dx = list(filter(lambda v: v != 0, np.diff(x)))
    # Recover the initial value
    dx.insert(0, x[0])
    # Return the comulative sum of the increments
    return np.cumsum(dx)


def compute(x, L, basis=False):
    """Computes the iterated-sums signature of a time series

    :param x: Time series
    :param L: Maximum level of the signature to be computed
    :param basis: Flag used to output basis elements together with
        signature componentes (default=False)
    :returns: A list of doubles representing the signature entries
    :rtype: list
    """
    # Return empty list if no data
    if not x:
        return []
    # Delete repeated entries and compute increments
    dx = np.diff(_compress(x))
    # Generate compositions
    parts = it.chain.from_iterable(map(_aP, range(1, L + 1)))
    uniqs = map(set, map(it.permutations, parts))
    comps = it.chain.from_iterable(uniqs)

    # Compute entries for each basis element
    sig = map(lambda c: _compute_entry(dx, c), comps)
    return list(sig)


def _compute_entry(dx, comp):
    if np.size(dx) == 0:
        return 0
    exponents = np.reshape(comp, (-1, 1))
    dxs = np.tile(dx, (np.size(comp), 1))
    mat = np.power(dxs, exponents)
    start = np.ones(np.size(dx))
    mat[0,:] = np.cumsum(mat[0,:])
    redux = fnt.reduce(_inner_shift, mat)
    return redux[-1]


def _inner_shift(a, x, only=False):
    a = np.pad(a, (1, 0))[:-1]
    return np.cumsum(np.multiply(a, x))


def _aP(n):
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
    #  The list `a`'s leading elements contain the partition in which
    #  y is the biggest element and x is either the same as y or the
    #  2nd largest element; v and w are adjacent element indices
    #  to which x and y are being assigned, respectively.
    a = [1] * n
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
            yield a[: w + 1]
            x += 1
            y -= 1
        a[v] = x + y
        y = a[v] - 1
        yield a[:w]
