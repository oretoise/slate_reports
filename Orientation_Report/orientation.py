"""
File: orientation.py
"""

import argparse
import numpy as np
import pandas as pd

import os 
import pathlib
import openpyxl

import time
import datetime

pd.set_option('display.width', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_colwidth', None)

# def arguments():
#     """ Parse CLI arguments. """
#     description = "Create a year-to-date report of application data."
#     parser = argparse.ArgumentParser(description=description)
#     parser.add_argument("-i", "--Input", action="store", help="Application Data File", required=True)
#     return parser.parse_args()

def data_to_df(data_path):
    ''' 
    walk the directory converting files to df 
    and then returning one combined dataframe
    '''

    
    dfs = []
    df = pd.DataFrame()

    for subdir, dirs, files in os.walk(data_path):
        for filename in files:
            if filename.endswith('.xlsx'):
                dfs.append(pd.read_excel(data_path / subdir / filename, engine = 'openpyxl'))
            elif filename.endswith('.csv'):
                dfs.append(pd.read_csv(data_path / subdir / filename))
    
    df = pd.concat(dfs)
    return df

def main():

    # aggregate the data into a big dataframe
    df = data_to_df(pathlib.Path(os.getcwd()) / "data")

    print(df.shape)

    # df.transpose()

    # print(df.index)
    # df.index.dropna(inplace=True)

    # print(df.index)
    # for col in df.columns:
    #     print(col)
        

            

if __name__ == "__main__":
    # Parse CLI arguments.
    # ARGS = arguments()

    # Call main function.
    main()