import pandas as pd

na_cleaner_modes = ["remove row", "mean", "mode"]
def clean_me(dataframe, 
            detect_binary=True, 
            numeric_dtype=True, 
            one_hot=True, 
            na_cleaner_mode="mean", 
            normalize=True, 
            datetime_columns=[], 
            remove_columns=[], 
            verbose=True):
    """
    clean_me function performs automatic dataset cleaning to Pandas DataFrame as per the settings parameters passed to this function
    
    :param dataframe: input Pandas DataFrame on which the cleaning will be performed 
    :param detect_binray: if True, any column that has two unique values, these values will be replaced with 0 and 1 (e.g.: ['looser', 'winner'] => [0,1])
    :param numeric_dtype: if True, columns will be converted to numeric dtypes when possible **see [1] in README.md**
    :param one_hot: if True, all non-numeric columns will be encoded to one-hot columns 
    :param na_cleaner_mode: what technique to use when dealing with None/NA/Empty values. Modes: 
        False       : do not consider cleaning na values 
        'remove row': removes rows with a cell that has NA value
        'mean'      : substitues empty NA cells with the mean of that column 
        'mode'      : substitues empty NA cells with the mode of that column
        '*'         : substiture empty NA cells with the value passed in 'na_cleaner_mode' param
    :param normalize: if True, all non-binray (columns with values 0 or 1 are excluded) columns will be normalized. 
    :param datetime_columns: a list of columns which contains date or time or datetime entries (important to be announced in this list, otherwise hot-encoding will mess up these columns)
    :param remove_columns: list of columns to remove, this is usually non-related featues such as the ID column 
    :param verbose: print progress in terminal/cmd
    :return: processed and clean Pandas DataFrame.
    """
    df = dataframe.copy()

    if verbose:
        print(" +++++++++++++++ AUTO DATA CLEANING STARTED ++++++++++++++++ ")
    
    # Validating user input to __init__ function 
    assert type(one_hot) == type(True), "Please ensure that one_hot param is bool (True/False)"
    # assert na_cleaner_mode in na_cleaner_modes, "Please choose proper value for naCleaner parameter. (Correct values are only: {})".format(self.__naCleanerOps)
    assert type(df) == type(pd.DataFrame()), "Parameter 'df' should be Pandas DataFrame"
    


    # casting datetime columns to datetime dtypes -----------------------------------------------------------------------
    if len(datetime_columns) > 0:
        if verbose: 
            print(" =  AutoDataCleaner: Casting datetime columns to datetime dtype... ")
        df = cols_to_datetime_dtype(df, datetime_columns, verbose)

    # removing unwanted columns (usually its the ID columns...) ---------------------------------------------------------
    if len(remove_columns) > 0: 
        if verbose: 
            print(" =  AutoDataCleaner: Performing removal of unwanted columns... ")
        df = remove_columns_df(df, remove_columns, verbose)


    # detecting binary columns ------------------------------------------------------------------------------------------
    if detect_binary: 
        if verbose: 
            print(" =  AutoDataCleaner: Performing One-Hot encoding... ")
        df = detect_binary_df(df, verbose)



    # checking if any columns can be converted to numeric dtypes  -------------------------------------------------------
    if numeric_dtype: 
        if verbose: 
            print(" = AutoDataCleaner: Converting columns to numeric dtypes when possible...")
        df = convert_numeric_df(df, exclude=datetime_columns, force=False, verbose=verbose)



    # converting non-numeric to one hot encoding ------------------------------------------------------------------------
    if one_hot: 
        if verbose: 
            print(" =  AutoDataCleaner: Performing One-Hot encoding... ")
        cols_num_before = df.shape[1]
        df = one_hot_df(df)
        if verbose: 
            print("  + one-hot encoding done, added {} new columns".format(df.shape[1] - cols_num_before))
    


    # clean None (na) values --------------------------------------------------------------------------------------------
    if na_cleaner_mode != False: 
        if verbose: 
            print(" =  AutoDataCleaner: Performing None/NA/Empty values cleaning... ")
        df = clean_na_df(df, na_cleaner_mode, verbose)
    


    # normalize all columns (binary 0,1 columns are excluded) -----------------------------------------------------------
    if normalize: 
        if verbose: 
            print(" =  AutoDataCleaner: Performing dataset normalization... ")
        df = normalize_df(df, exclude=datetime_columns, verbose=verbose)

    
    if verbose: 
        print(" +++++++++++++++ AUTO DATA CLEANING FINISHED +++++++++++++++ ")
    return df




""" ------------------------------------------------------------------------------------------------------------------------- """


import pandas as pd 

def datetime_dtype_series(series, verbose=True):
    """
    datetime_dtype_series function casts date columns to datetime dtype 

    :param df: input Pandas Series
    :returns: processed Pandas Series
    """
    try: 
        series = pd.to_datetime(series)
        if verbose: 
            print("  + converted column {} to datetime dtype".format(series.name))
        return series
    except Exception as e:
        print(" ERROR {}".format(e))


def cols_to_datetime_dtype(df, cols, verbose=True):
    """
    cols_to_datetime_dtype function casts given columns in dataframe to datetime dtype 

    :param df: input Pandas DataFrame
    :returns: processed Pandas DataFrame
    """
    for c in cols: 
        df[c] = datetime_dtype_series(df[c], verbose)
    return df


def remove_columns_df(df, remove_columns, verbose=True): 
    """
    remove_columns_df function removes columns in 'remove_columns' param list and returns df 
    
    :param df: input Pandas DataFrame 
    :param remove_columns: list of columns to be removed from the dataframe 
    :param verbose: print progress in terminal/cmd
    :returns: processed Pandas DataFrame 
    """
    stat = 0
    for col in remove_columns: 
        assert col in df.columns.to_list(), "{} is marked to be removed, but it does not exist in the dataset/dataframe".format(col)
        
        df.drop(columns=col, inplace=True)
        stat += 1
    if verbose: 
        print("  + removed {} columns successfully.".format(stat))
    return df

def detect_binary_df(df, verbose=True): 
    """
    detect_binray function detects columns that has two unique values (e.g.: yes/no OR true/false etc...)
    and converts it to a boolean column containing 0 or 1 values only 

    :param df: input Pandas DataFrame 
    :param verbose: print progress in terminal/cmd
    :returns: processed Pandas DataFrame 
    """
    stat_cols = 0
    stat_cols_names = [] 
    stat_rows = 0
    for col in df.columns.to_list(): 
        # check if column has two unique values 
        if len(df[col].unique().tolist()) == 2: 
            unique_values = df[col].unique().tolist()
            unique_values.sort() # to ensure consistency during training and predicting
            df[col] = df[col].replace(unique_values[0], 0)
            df[col] = df[col].replace(unique_values[1], 1)
            stat_cols += 1
            stat_cols_names.append(col)
            stat_rows += df.shape[0]
    if verbose: 
        print("  + detected {} binary columns [{}], cells cleaned: {} cells".format(stat_cols, stat_cols_names, stat_rows))
    return df

def convert_numeric_series(series, force=False, verbose=True): 
    """
    convert_numeric_series function converts columns of dataframe to numeric dtypes when possible safely 
    if the values that cannot be converted to numeric dtype are minority in the series (< %25), then
    these minority values will be converted to NaN and the series will be forced to numeric dtype 

    :param series: input Pandas Series
    :param force: if True, values which cannot be casted to numeric dtype will be replaced with NaN 'see pandas.to_numeric() docs' (be careful with force=True)
    :param verbose: print progress in terminal/cmd
    :returns: Pandas series
    """
    stats = 0
    if force: 
        stats += series.shape[0]
        return pd.to_numeric(series, errors='coerce'), stats
    else: 
        # checking if values that cannot be converted to numeric are < 25% of entries in this series
        non_numeric_count = pd.to_numeric(series, errors='coerce').isna().sum()
        if non_numeric_count/series.shape[0] < 0.25: 
            # values that cannot be numeric are minority; hence, we set this as NaN and force that column to be
            # casted to numeric dtype, the 'clean_na_series' function will handle these NaN values laters 
            stats += series.shape[0]
            if verbose and non_numeric_count != 0: 
                print("  + {} minority (minority means < %25 of '{}' entries) values that cannot be converted to numeric dtype in column '{}' have been set to NaN, nan cleaner function will deal with them".format(non_numeric_count, series.name, series.name))
            return pd.to_numeric(series, errors='coerce'), stats
        else: 
            # this series probably cannot be converted to numeric dtype, we will just leave it as is
            return series, stats


def convert_numeric_df(df, exclude=[], force=False, verbose=True):
    """
    convert_numeric_df function converts dataframe columns to numeric dtypes when possible safely 
    if the values in a particular columns that cannot be converted to numeric dtype are minority in that column (< %25), then
    these minority values will be converted to NaN and the column will be forced to numeric dtype 

    :param df: input Pandas DataFrame
    :param exclude: list of columns to be excluded whice converting dataframe columns to numeric dtype (usually datetime columns)
    :param force: if True, values which cannot be casted to numeric dtype will be replaced with NaN 'see pandas.to_numeric() docs' (be careful with force=True)
    :param verbose: print progress in terminal/cmd
    :returns: Pandas DataFrame
    """
    stats = 0
    for col in df.columns.to_list(): 
        if col in exclude:
            continue
        df[col], stats_temp = convert_numeric_series(df[col], force, verbose)
    stats += stats_temp
    if verbose: 
        print("  + converted {} cells to numeric dtypes".format(stats))
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
    if na_cleaner_mode == 'remove row': 
        return series.dropna()
    elif na_cleaner_mode == 'mean':
        mean = series.mean()
        return series.fillna(mean)
    elif na_cleaner_mode == 'mode':
        mode = series.mode()[0]
        return series.fillna(mode)
    elif na_cleaner_mode == False: 
        return series
    else: 
        return series.fillna(na_cleaner_mode)


def clean_na_df(df, na_cleaner_mode, verbose=True): 
    """
    clean_na_df function cleans all columns in DataFrame as per given na_cleaner_mode
    
    :param df: input DataFrame
    :param na_cleaner_mode: what technique to apply to clean na values 
    :param verbose: print progress in terminal/cmd
    :returns: cleaned Pandas DataFrame 
    """
    stats = {}
    for col in df.columns.to_list(): 
        if df[col].isna().sum() > 0: 
            stats[col + " NaN Values"] = df[col].isna().sum()
            try:
                df[col] = clean_na_series(df[col], na_cleaner_mode)
            except: 
                pass
                # print("  + could not find mean for column {}, will use mode instead to fill NaN values".format(col))
                # df[col] = clean_na_series(df[col], 'mode')
    if verbose: 
        print("  + cleaned the following NaN values: {}".format(stats))
    return df

def normalize_df(df, exclude=[], verbose=True): 
    """
    normalize_df function performs normalization to all columns of dataframe excluding binary (1/0) columns 
    
    :param df: input Pandas DataFrame
    :param exclude: list of columns to be excluded when performing normalization (usually datetime columns)
    :param verbose: print progress in terminal/cmd
    :returns: normalized Pandas DataFrame 
    """
    stats = 0
    for col in df.columns.to_list(): 
        if col in exclude: 
            continue
        # check if column is binray
        col_unique = df[col].unique().tolist()
        if len(col_unique) == 2 and 0 in col_unique and 1 in col_unique: 
            continue
        else: 
            df[col] = (df[col]-df[col].mean())/df[col].std()
            stats += df.shape[0]
    if verbose: 
        print("  + normalized {} cells".format(stats))
    return df



def help(): 
    help_text = """
    ++++++++++++++++++ AUTO DATA CLEANER HELP +++++++++++++++++++++++
    FUNCTION CALL:
    AutoDataCleaner.clean_me(df, one_hot=True, na_cleaner_mode="mean", normalize=True, remove_columns=[], verbose=True)

    FUNCTION PARAMETERS:
    df: input Pandas DataFrame on which the cleaning will be performed 
    one_hot: if True, all non-numeric columns will be encoded to one-hot columns 
    na_cleaner_mode: what technique to use when dealing with None/NA/Empty values. Modes: 
        False: do not consider cleaning na values 
        'remove row': removes rows with a cell that has NA value
        'mean': substitues empty NA cells with the mean of that column  
        'mode': substitues empty NA cells with the mode of that column
        '*': any other value will substitute empty NA cells with that particular value passed here 
    normalize: if True, all non-binray (columns with values 0 or 1 are excluded) columns will be normalized. 
    remove_columns: list of columns to remove, this is usually non-related featues such as the ID column 
    verbose: print progress in terminal/cmd
    returns: processed and clean Pandas DataFrame 
    ++++++++++++++++++ AUTO DATA CLEANER HELP +++++++++++++++++++++++
    """
    print(help_text)

if __name__=="__main__": 
    import pandas as pd
    import AutoDataCleaner.AutoDataCleaner as adc
    df = pd.DataFrame([
        [1, "Male", "white", 3, "2018/11/20"], 
        [2, "Female", "blue", "4", "2014/01/12"],
        [3, "Male", "white", 15, "2020/09/02"], 
        [4, "Male", "blue", "5", "2020/09/02"], 
        [5, "Male", "green", None, "2020/12/30"]
        ], columns=['id', 'gender', 'color', 'weight', 'created_on'])

    adc.clean_me(df, 
        detect_binary=True, 
        numeric_dtype=True, 
        one_hot=True, 
        na_cleaner_mode="mode", 
        normalize=True, 
        datetime_columns=["created_on"], 
        remove_columns=["id"], 
        verbose=True)