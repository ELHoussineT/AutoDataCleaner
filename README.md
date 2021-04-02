# AutoDataCleaner
Simple and automatic data cleaning in one line of code! 
Get your data ready for model training and fitting quickly.
# Features 
0. Uses Pandas DataFrames [So, no need to learn new syntax]
1. One-hot encoding: encodes non-numeric values to one-hot encoding columns 
2. Normalization: performs normalization to columns (excludes binary [1/0] columns)
3. Cleans Dirty/None/NA/Empty values: replace None values with mean or mode of a column, delete substitute with pre-defined value
4. Delete Unwanted Columns: drop and remove unwanted columns (usually this will be the 'id' column)
# Installation 
## Using pip: 
`pip install AutoDataCleaner`
# Example 
Import statements: 
`import pandas as pd
import AutoDataCleaner`
Example Pandas DataFrame to be cleaned: 
`df = pd.DataFrame([
                    [1, "Green", 3], 
                    [2, "Blue", 4],
                    [3, "Green", 5], 
                    [4, "Green", None]
                ], columns=['id', 'color', 'weight'])`
Call the `AutoDataCleaner.clean_me` to clean _dirty_ DataFrames:
`AutoDataCleaner.clean_me(df, remove_columns=['id']) # see 'Usage' section for more parameters`

Example output:
` +++++++++++++++ DATA CLEANING STARTED ++++++++++++++++ 
 = AutoDataCleaner: Performing One-Hot encoding... 
 = AutoDataCleaner: Performing None/NA/Empty values cleaning... 
 = AutoDataCleaner: Performing dataset normalization... 
 = AutoDataCleaner: Performing removal of unwanted columns... 
 +++++++++++++++ DATA CLEANING FINISHED +++++++++++++++ 

	weight 	color_Blue 	color_Green
0 	-1.224745 	0 	1
1 	0.000000 	1 	0
2 	1.224745 	0 	1
3 	0.000000 	0 	1`
# Usage
`AutoDataCleaner.clean_me(df, one_hot=True, na_cleaner_mode="mean", normalize=True, remove_columns=[], verbose=True):
    """
    clean_me function performs automatic dataset cleaning to Pandas DataFrame as per the settings parameters passed to this function
    
    :param df: input Pandas DataFrame on which the cleaning will be performed 
    :param one_hot: if True, all non-numeric columns will be encoded to one-hot columns 
    :param na_cleaner_mode: what technique to use when dealing with None/NA/Empty values. Modes: 
                            False       : do not consider cleaning na values 
                            'remove row': removes rows with a cell that has NA value
                            'mean'      : substitues empty NA cells with the mean of that column 
                            'mode'      : substitues empty NA cells with the mode of that column
                            '*'         : substiture empty NA cells with the value passed in 'na_cleaner_mode' param
    :param normalize: if True, all non-binray (columns with values 0 or 1 are excluded) columns will be normalized. 
    :param remove_columns: list of columns to remove, this is usually non-related featues such as the ID column 
    :param verbose: print progress in terminal/cmd
    :return: processed and clean Pandas DataFrame 
    """`
# Contribution 
Please feel free to send me feedback on "ofcourse7878@gmail.com", submit an issue or make a pull request! 
