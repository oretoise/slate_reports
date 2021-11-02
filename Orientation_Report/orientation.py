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

def eliminate_columns(df):

    df = df[[not elem for elem in df.index.str.contains("Day", na=False)]]
        
    list = ['MSU', 'digit', 'Digit', 'Date', 'Admit', 'Final', 'Term', 'term', '#', 'ID', 'Total', 'First', 'Last', 'Name', 'Student','student', 'Id', 'Totat', 'Semester', 'Username', 'Date']
    boolean_list = []
    flag = False

    # print(df.index)

    for element in df.index:
        for thing in list:
            if thing in str(element):
                boolean_list.append(True)
                flag = True
                break
        if flag:
            flag = False
            continue
        boolean_list.append(False)

    df = df[boolean_list]

    list = ['Final Score', 'Assignments Unposted Final Score', 'Unposted Final Score', 'Assignments Final Points', 'Imported Assignments Final Score','Imported Assignments Final Points', 'Imported Assignments Unposted Final Score', 'ID', 'Assignments Final Score']
    
    return df.drop(labels=list, axis=0).transpose().drop(index=0)

def combine_admit(df):
    return df[(df.index.str.contains('admit', case=False)) | (df.index.str.contains('term', case=False) | (df.index.str.contains('semester', case=False)))].transpose()


def combine_netID(df):
    return df[(df.index.str.contains('Net')) | (df.index.str.contains('SIS Login') | (df.index.str.contains('Username')))].transpose()


def combine_9_digit(df):
    return df[(df.index.str.contains('9')) | (df.index.str.contains('MSU') | (df.index.str.contains('0') | (df.index.str.contains('SIS User') | (df.index.str.contains('Student ID')))))].transpose()

def combine_scores(df):
    return df[(df.index.str.contains('Fina')) | (df.index.str.contains('Tota'))].transpose()

def construct_result(df):
    list = []
    list.append(combine_scores(df.transpose()))
    list.append(combine_9_digit(df.transpose()))
    list.append(combine_netID(df.transpose()))
    list.append(combine_admit(df.transpose()))

    # TODO: since concattenating data is being separated fix this later
    return pd.concat(list)

def main():

    # aggregate the data into a big dataframe
    df = data_to_df(pathlib.Path(os.getcwd()) / "data")    

    # eliminate unwanted columns
    df = eliminate_columns(df.transpose())

    # condense into 4 columns
    final_df = construct_result(df)

    
    ''' for debugging '''
    # final_df.to_excel("final_df.xlsx")
    # df.to_excel("df.xlsx")
    print(final_df.shape)
    

if __name__ == "__main__":
    # Parse CLI arguments.
    # ARGS = arguments()

    # Call main function.
    main()