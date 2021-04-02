<p align="center">
	<a href="https://www.python.org/downloads/">
		<img src="https://img.shields.io/badge/Python-3.*.*-success" />
	</a>
	<a href="https://pypi.org/project/AutoDataCleaner/">
		<img src="https://img.shields.io/badge/PypiBuild-Stable-blue" />
	</a>
	<a href="https://pypi.org/project/AutoDataCleaner/">
		<img src="https://img.shields.io/badge/Version-1.0.3-lightgrey" />
	</a>
</p>
# AutoDataCleaner
Simple and automatic data cleaning in one line of code! It performs **One Hot Encoding**, **Cleans Dirty/Empty Values**, **Normalizes values** and **Removes unwanted columns** all in one line of code.
Get your data ready for model training and fitting quickly.
# Features 
0. **Uses Pandas DataFrames [So, no need to learn new syntax]**
1. **One-hot encoding**: encodes non-numeric values to one-hot encoding columns 
2. **Normalization**: performs normalization to columns (excludes binary [1/0] columns)
3. **Cleans Dirty/None/NA/Empty values**: replace None values with mean or mode of a column, delete row that has None cell or substitute None values with pre-defined value
4. **Delete Unwanted Columns**: drop and remove unwanted columns (usually this will be the 'id' column)
# Installation 
#### Using pip
`pip install AutoDataCleaner`
#### Cloning repo: 
Clone repository and run `pip uninstall -e .` inside the repository directory
####
Install from repository directly using `pip install git+git://github.com/sinkingtitanic/AutoDataCleaner.git#egg=AutoDataCleaner`
# Quick One-line Usage: 
```
    AutoDataCleaner.clean_me(df, 
                            one_hot=True, 
                            na_cleaner_mode="mean", 
                            normalize=True, 
                            remove_columns=[], 
                            verbose=True)
```
# Example 
```
import pandas as pd
import AutoDataCleaner

df = pd.DataFrame([
                    [1, "Green", 3], 
                    [2, "Blue", 4],
                    [3, "Green", 5], 
                    [4, "Green", None]
                ], columns=['id', 'color', 'weight'])

AutoDataCleaner.clean_me(df, remove_columns=['id']) # see 'Usage' section for more parameters
```
Example output:
```
 +++++++++++++++ DATA CLEANING STARTED ++++++++++++++++ 
 = DataCleaner: Performing One-Hot encoding... 
 = DataCleaner: Performing None/NA/Empty values cleaning... 
 = DataCleaner: Performing dataset normalization... 
 = DataCleaner: Performing removal of unwanted columns... 
 +++++++++++++++ DATA CLEANING FINISHED +++++++++++++++ 
	weight 	color_Blue 	color_Green
0 	-0.855528 	0 	1
1 	-0.475293 	1 	0
2 	-0.095059 	0 	1
3 	1.425880 	0 	0
```
# Explaining Parameters 

`AutoDataCleaner.clean_me(df, one_hot=True, na_cleaner_mode="mean", normalize=True, remove_columns=[], verbose=True)`

Parameters & what do they mean:
* `df`: input Pandas DataFrame on which the cleaning will be performed <br />
* `one_hot`: if True, all non-numeric columns will be encoded to one-hot columns <br />
* `na_cleaner_mode`: what technique to use when dealing with None/NA/Empty values. Modes: <br />
    * `False`: do not consider cleaning na values <br />
    * `'remove row'`: removes rows with a cell that has NA value<br />
    * `'mean'`: substitues empty NA cells with the mean of that column <br /> 
    * `'mode'`: substitues empty NA cells with the mode of that column<br />
    * `'*'`: any other value will substitute empty NA cells with that particular value passed here <br />
* `normalize`: if True, all non-binray (columns with values 0 or 1 are excluded) columns will be normalized. <br />
* `remove_columns`: list of columns to remove, this is usually non-related featues such as the ID column <br />
* `verbose`: print progress in terminal/cmd<br />
* `returns`: processed and clean Pandas DataFrame <br />

# Prediction 
In prediction phase, put the examples to be predicted in Pandas DataFrame and run them through `AutoDataCleaner.clean_me` function **with the same parameters you
used during training**.
# Contribution 
Please feel free to send me feedback on "ofcourse7878@gmail.com", submit an issue or make a pull request! 
