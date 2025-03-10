# 2023-01 ICRAR Data Science Exercise by Omar

## How to run the scripts

1. First, clone this repository and then open the terminal in the root directory to the run the following command: 
```
pip install -r requirements.txt
```
This will install the requirements for the excercise. It is up to the user if they want to create a new environment to run this exercise.


2. Launch 'spyder' and navigate to root directory of this repository.

This repository contains two python scripts.
```
src\exercise_functions.py
tests\exercise_functions_test.py
```

3. Navigate to 'tests' directory and run exercise_functions_test.py which uses the implemented functions to generate the clean files for all 4 months, and generates the visualisations for the 6th month. Following section provides a brief description of functions and how their input arguments in exercise_functions_test.py can be modified for various tasks.

## Brief description of functions

Script file exercise_functions.py has two functions for the users, one for cleaning and the other for visualisation.
```
def clean_csv_files(months = [6,7,8,9])
def visulize_data(months = [6], filter_size=5)
```
Function 'clean_csv_files' uses the csv files in database to generate clean csv file(s) for each month. The new csv files are generated in the root directory. By default, this function will process the files for all 4 months to generate the clean files with data from targeted timestamps. However, user can specify the desired month(s) to be cleaned as a list of month numbers. See the following example which will only generate clean file for the 9th month:
```
clean_csv_files([9])
```
Function 'visulize_data' generates visualizations for the specified month(s). By default, this function will generate the visualisation only for the 6th month. The user can specify the month(s) for which visualisations are desired. For example, following call will generate the visualisation for both 7th and 8th month.  
```
visulize_data(months = [7,8])
```
A total of 14 figures are generated for the visualisation of each month (explained later), so using multiple months will generate a significant number of figures and can cause confusion (and some RuntimeWarnings).  

## Brief explanation of visualisations

Two visualisation figures are generated for each type of feature i.e., a1, a2, b1, b2, hspec, dspec and sprspec, and for each month. All 100 sub-features (0-99) for each feature are included in these visualisations. 

First figure for each feature projects all the sub-features in a 2-D space using a different colour for each sub-feature. This allows to easily identify the days/times where all the sub-features show a similar trend.
Here is an example of hspec features (hspec_0 to hspec_99) for the 6th month when projected on a 2-D space.
![Alt](images/Figure_9.png)

Second figure for each feature generates two interactive surface subplots of all the sub-features (0 to 99) for a feature. This allows the user to observe the variation across days as well as across sub-features. The first subplot directly uses the data from csv files without any modifications, whereas the second subplot uses a 2-D averaging filter for smoothing the surface by reducing the high frequency noise. The default dimensions for the filter are 5x5, but the user can specify any desired dimension between 3 and 21. The example below uses a larger filter of 21x21 for visualizing the data of 6th month. 
```
visulize_data(months = [6],filter_size=21)
```

The use of larger filter generates smoother surfaces for visualisations but also filters the high frequency features from the data. Here is an example of hspec features for the 6th month when projected as a 3-D surface. Surface on the left uses the raw data, whereas the surface on the right uses the filtered data with filter size of 21x21.

Caution: Use of larger averaging filters is not appropriate if there are NaNs in the data. 

![Alt](images/Figure_10.png)


### Project structure
```
2023-01-data-science-exercise/

├── data
│   ├── 2022-06
│   ├── 2022-07
│   ├── 2022-08
│   └── 2022-09
├── images
│   ├── Figure_9.png
│   └── Figure_10.png
├── src
│   ├── __init__.py
│   └── exercise_functions.py
├── tests
│   ├── __init__.py
│   └── exercise_functions_test.py
├── README.md
└── requirements.txt
```

