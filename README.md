Discrete Signature
==================

This suite is for testing the performance of the `dsig` feature map
introduced in [here](https://www.arxiv.org/abs/1906.05823).

To run the test you have to download the [UCR Archive 2018](https://www.cs.ucr.edu/~eamonn/time_series_data_2018/) dataset.

Usage
-----
1. Clone the repository using `git clone https://www.github.com/ntapiam/dsig-poc.git`
2. Run `sh getdata.sh` to download the data in the UCR Archive 2018
3. Execute tests by running `python3 main.py L p`. See `python3 main.py -h` for more info.
4. Output goes into a file named `results_timestamp.txt` in 3-column tab-separated format.

Reader Classes
--------------
The `util.tsreader` package provides two clases for reading data out of `.ts` and `.tsv` files.
They provide generators for all the observations in each file, they are returned as a pair `(x,y)` where `x` is a list of floats and `y` is a string reprepresenting the label of the observation.

### Example:
```python
import util.tsreader as ts
import lib
import numpy as np
from scipy.cluster import hierarchy
import matplotlib.pyplot as plt

train_reader = ts.TSVReader('UCRArchive_2018/Trace/Trace_TRAIN.tsv')
train_obs = list(train_reader.read())
train_sig = [(list(lib.dsig(x,3)),y) for x,y in train_obs]

signatures = np.array([np.array(s) for s,_ in train_sig])
Z = linkage(signatures)
dn = hierarchy.dendrogram(Z)
plt.show()
```

Feel free to fork the repository.

Address any questions to [Nikolas Tapia](mailto:tapia@wias-berlin.de).

