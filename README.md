# 2023-01 ICRAR Data Science Exercise

## General instructions

1. Clone this repository into your own GitHub account.
1. All your work will be done in your repository.
1. Inspect the data and understand what is available.
1. When going through the exercise, create git commits and pushes, making a history of changes that can be inspected later.
1. The exercise should be completed in Python 3.9+.
1. Your cloned git repository should be structured and populated using a standard Python project template for application development, which other people might reuse.
1. Create a __README__ file in the root of your repository, explaining how to run your code.
1. At the end of the exercise, you will __have__ to push your code to your GitHub repository and allow access to the following Git-Ids: [KevinVinsen](https://github.com/KevinVinsen) and [awicenec](https://github.com/awicenec). 

## Details

The two objectives of this exercise are:
1. Produce cleaned and consolidated data files suitable for loading by another process (which is not part of this exercise).
1. Produce a visualisation showing significant events/features in the data.

### Objective 1

You need to clean and consolidate the CSV data files in the data directory and produce four output CSV files, one for each month.
The cadence of the output data files needs to be strictly hourly (i.e. 00:00:00, 01:00:00, 02:00:00, etc.) and complete, i.e. 24 rows for every day in the monthly file.
The output file should contain the same column names as the input files.

When you encounter missing rows in the original data files, use the following rules:

1. If the top of the hour (00 minutes) entry is missing or empty, the data for 10 minutes to the hour should be used.
1. If that is also unavailable, use the data for 10 minutes past the hour.
1. If neither of these values is available, record NaNs for all the data columns.

No matter what, the __observe_time__ column should always contain the respective top of the hour time, and should never contain a NaN.

You should use a standard Python project template, similar to the [example project layout](#Example project template) shown below, for this part of the exercise. __A Jupyter notebook is not an acceptable solution for this objective.__

### Example project template
```
2023-01-data-science-exercise/
├── README.md
├── data
│   ├── 2022-06
│   ├── 2022-07
│   ├── 2022-08
│   └── 2022-09
├── jupyter
│   └── notebook.ipynb
├── requirements.txt
├── src
│   ├── __init__.py
│   └── code.py
└── tests
    ├── __init__.py
    └── test_code.py
```


### Objective 2

For the visualisation, think about a situation, where you have to explain and describe the data to somebody and verify that your cleaning actually worked as expected.
What would you show and how would you show it?
Given that we have actually not told you anything about what the data actually is, this really needs to concentrate on what you can derive from looking at the data, i.e. plotting it in various ways.

The python package/tools (MatPlotLib, Plotly, Jupyter) you use to produce the visualisation is up to you.
__Jupyter notebooks are acceptable for this objective.__