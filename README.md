



## Require package for this automated analysis
pandas
seaborn
matplotlib
scipy
numpy
argparse
tabulate
uv

## To run this file after package requirement  then we have to run the file using uv
# uv run autolysis.py datasetname.csv
uv run autolysis.py goodreads.csv
uv run autolysis.py media.csv
uv run autolysis.py happiness.csv

## Data Analysis Results

## Data Summary
           overall      quality  repeatability
count  2652.000000  2652.000000    2652.000000
mean      3.047511     3.209276       1.494721
std       0.762180     0.796743       0.598289
min       1.000000     1.000000       1.000000
25%       3.000000     3.000000       1.000000
50%       3.000000     3.000000       1.000000
75%       3.000000     4.000000       2.000000
max       5.000000     5.000000       3.000000

## Missing Values
date              99
language           0
type               0
title              0
by               262
overall            0
quality            0
repeatability      0
dtype: int64

## Analysis Narrative
Narrative generation failed.

## Visualizations
![Correlation Heatmap](correlation_heatmap.png)