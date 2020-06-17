import numpy as np
from concurrent.futures import ThreadPoolExecutor

from .decorators import time_this
from . import preftree


class Iss:
    def __init__(self, level=4):
        self._tree = preftree.pTree(level)
        self._level = level
        self._sig = np.array([])
        self._dx = []
        self._powers = np.array([])

    @property
    def sig(self):
        return self._sig[:, -1]

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
        return self._tree.basis

    @level.setter
    def level(self, level):
        self._tree.level = level
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
        # Clean the data 
        if not self._pre_process(x) : return []
        # Compute entries for each basis element
        self._prepare_workspace()
        for k in range(1,1<<self._level):
            self._sig[k] = self._compute_index(k)
        return self

    def _pre_process(self,x):
        x = np.array(x)
        # Return empty list if no data
        if not (x.ndim and x.size):
            return False
        # Delete repeated entries and compute increments
        self._dx = np.diff(self._compress(x))
        return True

    def _prepare_workspace(self):
        # Save powers of dx 
        self._powers = np.zeros( (self._level+1,self._dx.size) )
        self._powers[0] =  np.ones(self._dx.size)
        for i in range(1,self._level):
            self._powers[i] = np.power(self._dx, i)
        # Allocate enough memory
        self._sig = np.zeros( (1<<self._level,self._dx.size) )
        self._sig[0] = np.ones(self._dx.size)

    def _compute_index(self, k ):
        parent = self._tree.parents[k]
        key = self._tree.key[k]
        inner = np.pad( self._sig[parent] , (1, 0))[:-1]
        outer = self._powers[key]
        return np.cumsum(inner * outer) 
