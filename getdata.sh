#!/usr/bin/env sh
wget https://www.cs.ucr.edu/~eamonn/time_series_data_2018/UCRArchive_2018.zip
unzip -P someone UCRArchive_2018 -x */Missing_value_and_variable_length_datasets_adjusted/*
rm UCRArchive_2018.zip
