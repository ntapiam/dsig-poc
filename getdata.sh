#!/usr/bin/env sh
wget https://www.cs.ucr.edu/~eamonn/time_series_data_2018/UCRArchive_2018.zip
unzip UCRArchive_2018 -P someone
rm -rf UCRArchive_2018/Missing_value_and_variable_length_datasets_adjusted
rm UCRArchive_2018.zip
