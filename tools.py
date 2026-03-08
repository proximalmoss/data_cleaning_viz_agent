import pandas as pd
import numpy as np

def check_nulls(df: pd.DataFrame) -> str:
    """check for null values in each column"""
    null_counts=df.isnull().sum()
    null_percent=(df.isnull().sum()/len(df)) * 100
    result=pd.DataFrame({
        'null count':null_counts,
        'null percent':null_percent.round(2)
    })
    return result.to_string()

def fill_null(df: pd.DataFrame) -> str:
    """fill numerical with median and categorical with mode"""
    filled_columns=[]
    
    for column in df.columns:
        if df[column].isnull().sum()>0:
            if df[column].dtype in ['float64', 'int64']:
                median_val=df[column].median()
                df[column].fillna(median_val, inplace=True)
                filled_columns.append(f"{column}: filled with median ({median_val:.2f})")
            else:
                mode_val=df[column].mode()[0]
                df[column].fillna(mode_val, inplace=True)
                filled_columns.append(f"{column}: filled with mode ({mode_val})")
    if filled_columns:
        return "Filled nulls: \n" + "\n".join(filled_columns)
    else:
        return "No null values found"

def check_duplicates(df: pd.DataFrame) -> str:
    """check for duplicate values in each column"""
    duplicate_count=df.duplicated().sum()
    duplicate_percent=(df.duplicated().sum()/len(df)) * 100
    return f"Found {duplicate_count} duplicate rows ({duplicate_percent:.2f}% of total data)"

def remove_duplicates(df: pd.DataFrame) -> str:
    """removing duplicates if they are less ran 30% of total data"""
    duplicate_percent=(df.duplicated().sum()/len(df)) * 100
    if (duplicate_percent<30):
        df.drop_duplicates(inplace=True)
    else:
        return f"Warning: {duplicate_percent:.2f}% of data is duplicates. Too high to auto-remove, please review manually."
    return "Duplicates removed"

def fix_datatypes(df: pd.DataFrame) -> str:
    """fixing datatypes of columns"""
    fixed_columns=[]
    for column in df.columns:
        if df[column].dtype=='object':
            try:
                df[column]=pd.to_numeric(df[column])
                fixed_columns.appned(f"{column}: converted to numeric")
            except:
                pass
    if fixed_columns:
        return "Fixed datatypes:\n" + "\n".join(fixed_columns)
    else:
        return "All datatypes are correct"

def detect_outliers(df: pd.DataFrame) -> str:
    """Detect outliers in numerical columns using IQR method"""
    outliers=[]
    for column in df.columns:
        Q1=df[column].quantile(0.25)
        Q3=df[column].quantile(0.75)
        IQR=Q3-Q1
        outlier_count=df[(df[column]<Q1-1.5*IQR) | (df[column]>Q3+1.5*IQR)].shape[0]
        if outlier_count>0:
            outliers.append(f"{column}: {outlier_count} outliers detected")
    if outliers:
        return "Outliers found:\n" + "\n".join(outliers)
    else:
        return "No outliers found"

def get_summary(df: pd.DataFrame):
    """Get a summary of the dataframe"""
    summary=[]
    summary.append(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns")
    summary.append(f"\nColumn Datatypes:\n{df.dtypes.to_string()}")
    summary.append(f"\nBasic Statistics: \n{df.describe().to_string()}")
    return "\n".join(summary)