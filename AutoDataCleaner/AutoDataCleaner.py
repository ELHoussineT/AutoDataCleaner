import pandas as pd

na_cleaner_modes = ["remove row", "mean", "mode"]

def clean_me(df, one_hot=True, na_cleaner_mode="mean", normalize=True, remove_columns=[], verbose=True):
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
    :return: processed and clean Pandas DataFrame.
    """
    if verbose:
        print(" +++++++++++++++ DATA CLEANING STARTED ++++++++++++++++ ")
    
    # Validating user input to __init__ function 
    assert type(one_hot) == type(True), "Please ensure that one_hot param is bool (True/False)"
    # assert na_cleaner_mode in na_cleaner_modes, "Please choose proper value for naCleaner parameter. (Correct values are only: {})".format(self.__naCleanerOps)
    assert type(df) == type(pd.DataFrame()), "Parameter 'df' should be Pandas DataFrame"
    
    # converting non-numeric to one hot encoding 
    if one_hot: 
        if verbose: 
            print(" = DataCleaner: Performing One-Hot encoding... ")
        df = one_hot_df(df)
    
    # clean None (na) values 
    if na_cleaner_mode != False: 
        if verbose: 
            print(" = DataCleaner: Performing None/NA/Empty values cleaning... ")
        df = clean_na_df(df, na_cleaner_mode)
    
    # normalize all columns (binary 0,1 columns are excluded)
    if normalize: 
        if verbose: 
            print(" = DataCleaner: Performing dataset normalization... ")
        df = normalize_df(df)

    # removing unwanted columns (usually its the ID columns...)
    if len(remove_columns) > 0: 
        if verbose: 
            print(" = DataCleaner: Performing removal of unwanted columns... ")
        df = remove_columns_df(df, remove_columns)

    if verbose: 
        print(" +++++++++++++++ DATA CLEANING FINISHED +++++++++++++++ ")
    return df

def one_hot_df(df): 
    """ 
    one_hot_df returns one-hot encoding of non-numeric columns in all the columns of the passed Pandas DataFrame
    
    :param df: input Pandas DataFrame
    :returns: Pandas DataFrame
    """
    return pd.get_dummies(df)

def clean_na_series(series, na_cleaner_mode): 
    """ 
    clean_nones function manipulates None/NA values in a given panda series according to cleaner_mode parameter
        
    :param series: the Panda Series in which the cleaning will be performed 
    :param na_cleaner_mode: what cleaning technique to apply, 'na_cleaner_modes' for a list of all possibilities 
    :returns: cleaned version of the passed Series
    """
    if na_cleaner_mode == "remove row": 
        return series.dropna()
    elif na_cleaner_mode == 'mean':
        mean = series.mean()
        return series.fillna(mean)
    elif na_cleaner_mode == 'mode':
        mode = series.mode()
        return series.fillna(mode)
    else: 
        return series.fillna(na_cleaner_mode)


def clean_na_df(df, na_cleaner_mode): 
    """
    clean_na_df function cleans all columns in DataFrame as per given na_cleaner_mode
    
    :param df: input DataFrame
    :param na_cleaner_mode: what technique to apply to clean na values 
    :returns: cleaned Pandas DataFrame 
    """
    for col in df.columns.to_list(): 
        df[col] = clean_na_series(df[col], na_cleaner_mode)
    return df

def normalize_df(df): 
    """
    normalize_df function performs normalization to all columns of dataframe excluding binary (1/0) columns 
    
    :param df: input Pandas DataFrame
    :returns: normalized Pandas DataFrame 
    """
    for col in df.columns.to_list(): 
        # check if column is binray
        col_unique = df[col].unique().tolist()
        if len(col_unique) == 2 and 0 in col_unique and 1 in col_unique: 
            continue
        else: 
            df[col] = (df[col]-df[col].mean())/df[col].std()
    return df

def remove_columns_df(df, remove_columns): 
    """
    remove_columns_df function removes columns in 'remove_columns' param list and returns df 
    
    :param df: input Pandas DataFrame 
    :param remove_columns: list of columns to be removed from the dataframe 
    :returns: processed Pandas DataFrame 
    """
    for col in remove_columns: 
        assert col in df.columns.to_list(), "{} is marked to be removed, but it does not exist in the dataset/dataframe".format(col)
        
        df.drop(columns=col, inplace=True)
    return df

