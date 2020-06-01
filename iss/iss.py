import itertools as it
import more_itertools as mit
import functools as fnt
import numpy as np
from concurrent.futures import ThreadPoolExecutor

from .decorators import time_this
from . import preftree


class Iss:
    def __init__(self, level=4):
        self._words = preftree.Node()
        self._words.expand(level)
        self._level = level
        self._sig = np.array([])
        self._dx = []

    @property
    def sig(self):
        return self._sig[:, -1]

    def sig_by_key(self, key):
        node = self._words.lookup(key)
        return node.value if node else None

    @property
    def sig_full(self):
        return self._sig

    @property
    def sig_basis(self):
        return list(zip(self.sig, self.basis))

    @property
    def level(self):
        return self._level

    @property
    def basis(self):
        return [t.key for t in self._words.bfs()]

    @level.setter
    def level(self, level):
        if level > self._level:
            self._words.expand(level)
        else:
            self._words.contract(level)
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

    def compute(self, x):
        """Computes the iterated-sums signature of a time series

        :param x: Time series
        :returns: A matrix of doubles representing the signature entries
        :rtype: list
        """
        x = np.array(x)
        # Return empty list if no data
        if not (x.ndim and x.size):
            return []
        # Delete repeated entries and compute increments
        self._dx = np.diff(self._compress(x))
        # Compute entries for each basis element
        self._sig = np.stack(list(self._words.bfs(self._compute_entry)))
        return self

    def _compute_entry(self, parent, child):
        if parent.key == ():
            parent.value = np.ones(self._dx.size)
            inner = parent.value
        else:
            inner = np.pad(parent.value, (1, 0))[:-1]
        outer = np.power(self._dx, child.key[-1])
        child.value = np.cumsum(inner * outer)
        return child.value
