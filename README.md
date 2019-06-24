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

Feel free to fork the repository.

Address any questions to [Nikolas Tapia](mailto:tapia@wias-berlin.de).

