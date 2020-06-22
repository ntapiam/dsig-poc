ISS
====

Python package for computing iterated-sums signatures, as defined in [DEFT20].
For the moment, only one-dimensional time series are supported.

Usage
-----
First, initialize the package by importing it and creating an instance of the `Iss` class:
```python3
>>> from iss import Iss
>>> s = Iss()
```
The constructor takes a single integer, representing the level of the signature (default: 4).

Then, use the `Iss.compute(x)` method. It takes a single list `x` of `float`s. It outputs an `n`-by-`m` matrix, where `n = len(x) - 1` and `m = 2 ** level - 1`.

**Example:**
```python3
>>> from iss import Iss
>>> s = Iss()
>>> x = [0, 1, 3, 6]
>>> s.compute(x)
array([[ 1,  0,  1,  0,  0,  0,  1,  0,  0,  0,  0,  0,  0,  0,  1],
       [ 3,  2,  5,  0,  4,  2,  9,  0,  0,  0,  0,  8,  2,  4, 17],
       [ 6, 11, 14,  6, 31, 17, 36,  0, 12,  6, 18, 89, 29, 49, 98]])
```

The result of `Iss.compute(x)` is stored in `Iss.sig`. The basis can be recovered by `Iss.basis`.

People
------
- Maintainer: [Nikolas Tapia](https://www.wias-berlin.de/people/tapia)
- Contributors: Diego Caudillo, Joscha Diehl

References
---------
[DEFT20] J. Diehl, K. Ebrahimi-Fard, N. Tapia. [_Time-warping invariants of multidimensional time series_](https://doi.org/10.1007/s10440-020-00333-x). Acta Appl. Math. (2020)
