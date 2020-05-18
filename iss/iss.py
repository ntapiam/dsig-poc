import itertools as it
import more_itertools as mit
import functools as fnt
import numpy as np
from concurrent.futures import ThreadPoolExecutor

from .decorators import time_this


class Iss:
    def __init__(self, level=4):
        self._level = level
        self._words = self._gen_words(level)
        self._sig = np.array([])
        self._idx = np.power(2, range(level + 1))

    @property
    def sig(self):
        return self._sig

    @property
    def sig_basis(self):
        return list(zip(self.sig, self.words))

    @property
    def level(self):
        return self._level

    @property
    def basis(self):
        return self._words

    @level.setter
    def level(self, level):
        self._words = self._gen_words(level, self._words)
        self._level = level

    def _compress(self, x):
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

    def compute_parallel(self, x):
        """Computes the iterated-sums signature of a time series

        :param x: Time series
        :param L: Maximum level of the signature to be computed
        :param basis: Flag used to output basis elements together with
            signature componentes (default=False)
        :returns: A list of doubles representing the signature entries
        :rtype: list
        """
        # Return empty list if no data
        x = np.array(x)
        if not (x.ndim and x.size):
            return self
        # Delete repeated entries and compute increments
        dx = np.diff(self._compress(x))
        # Compute entries for each basis element
        with ThreadPoolExecutor() as executor:
            sig = executor.map(lambda c: self._compute_entry(dx, c), self._words)
        return list(sig)

    def compute(self, x):
        """Computes the iterated-sums signature of a time series

        :param x: Time series
        :param L: Maximum level of the signature to be computed
        :param basis: Flag used to output basis elements together with
            signature componentes (default=False)
        :returns: A list of doubles representing the signature entries
        :rtype: list
        """
        # Return empty list if no data
        x = np.array(x)
        if not (x.ndim and x.size):
            return []
        # Delete repeated entries and compute increments
        dx = np.diff(self._compress(x))
        # Compute entries for each basis element
        sig = map(lambda c: self._compute_entry(dx, c), self._words)
        return list(sig)

    def _compute_entry(self, dx, comp):
        if not (dx.ndim and dx.size):
            return 0
        exponents = np.reshape(comp, (-1, 1))
        dxs = np.tile(dx, (np.size(comp), 1))
        mat = np.power(dxs, exponents)
        mat[0, :] = np.cumsum(mat[0, :])
        redux = fnt.reduce(self._inner_shift, mat)
        return redux[-1]

    def _inner_shift(self, a, x):
        a = np.pad(a, (1, 0))[:-1]
        return np.cumsum(np.multiply(a, x))

    def _gen_words(self, level, prev=[]):
        # Generate compositions
        print(f"Generating basis up to level {level}...")
        if level < self._level:
            return prev[: 2 ** level - 1]
        else:
            low = self._level if prev else 0
            parts = map(self._aP, range(low, level + 1))
            parts = it.chain.from_iterable(parts)
            uniqs = map(set, map(it.permutations, parts))
            comps = it.chain.from_iterable(uniqs)
            prev = it.chain(prev, comps)
            return list(prev)

    def _aP(self, n):
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
            Available:
            http://jeromekelleher.net/generating-integer-partitions.html
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
