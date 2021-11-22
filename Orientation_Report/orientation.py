"""
File: orientation.py
"""

import numpy as np
import pandas as pd

import os 
import pathlib
import openpyxl

import time
from datetime import datetime as dt


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
            dfs[-1]['Start Orientation Date'] = filename
            dfs[-1]['Orientation Year'] = subdir
    df = pd.concat(dfs)
    return df

def eliminate_columns(df):

    df = df[[not elem for elem in df.index.str.contains("Day", na=False)]]
        
    list = ['MSU', 'digit', 'Digit', 'Date', 'Admit', 'Final', 'Term', 'term', '#', 'ID', 'Total', 'First', 'Last', 'Name', 'Student','student', 'Id', 'Totat', 'Semester', 'Username', 'Date', 'Filename', 'Orientation Year']
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

    # list = ['Final Score', 'Assignments Unposted Final Score', 'Unposted Final Score', 'Assignments Final Points', 'Imported Assignments Final Score','Imported Assignments Final Points', 'Imported Assignments Unposted Final Score', 'ID', 'Assignments Final Score']
    
    # return df.drop(labels=list, axis=0).transpose().drop(index=0)
    return df.transpose().drop(index=0)

def combine_admit(df):
    df = df[(df.index.str.contains('admit', case=False)) | (df.index.str.contains('term', case=False) | (df.index.str.contains('semester', case=False)))].transpose()

    flag = True
    for col in df.columns:
        if flag:
            df['0-Admitted Students'] = df[str(col)]
            flag=False

        df['0-Admitted Students'] = np.where(df[str(col)].isnull(), df['0-Admitted Students'], df[str(col)])

    return df['0-Admitted Students']

def combine_netID(df):
    df = df[(df.index.str.contains('Net')) | (df.index.str.contains('SIS Login') | (df.index.str.contains('Username')))].transpose()

    flag = True
    for col in df.columns:
        if flag:
            df['0-NetID'] = df[str(col)]
            flag=False

        df['0-NetID'] = np.where(df[str(col)].isnull(), df['0-NetID'], df[str(col)])

    return df['0-NetID']

def combine_9_digit(df):
    df = df[(df.index.str.contains('9')) | (df.index.str.contains('MSU') | (df.index.str.contains('0') | (df.index.str.contains('SIS User') | (df.index.str.contains('Student ID')))))].transpose()

    flag = True
    for col in df.columns:
        if flag:
            df['0-MSU-9-digit'] = df[str(col)]
            flag=False

        df['0-MSU-9-digit'] = np.where(df[str(col)].isnull(), df['0-MSU-9-digit'], df[str(col)])

    return df['0-MSU-9-digit']

def combine_scores(df):
    df = df[(df.index.str.contains('Fina')) | (df.index.str.contains('Tota'))].transpose()

    flag = True
    for col in df.columns:
        if flag:
            df['0-Final Scores'] = df[col]
            flag=False

        df['0-Final Scores'] = np.where(df[str(col)].isnull(), df['0-Final Scores'], df[str(col)])

    return df['0-Final Scores']

def construct_result(df):
    combined_frame = pd.DataFrame()
    combined_frame['NetID'] = combine_netID(df.transpose())
    combined_frame['MSU 9-Digit'] = combine_9_digit(df.transpose())
    combined_frame['Final Scores'] = combine_scores(df.transpose())
    combined_frame['Admit Term'] = combine_admit(df.transpose())

    combined_frame['Start Orientation Date'] = df['Start Orientation Date']
    combined_frame['Orientation Year'] = df['Orientation Year']

    return combined_frame.reset_index(drop=True).dropna(thresh=4)

def to_datetime(x):

    start_dates = {
        "Spring 2008": "January 9",
        "Summer 2008": "May 12",
        "Fall 2008": "August 18",
        # Note: Spring 2009's calendar is missing...
        "Summer 2009": "May 11",
        "Fall 2009": "August 17",
        "Spring 2010": "January 6",
        "Summer 2010": "May 10",
        "Fall 2010": "August 18",
        "Spring 2011": "January 5",
        "Summer 2011": "May 9",
        "Fall 2011": "August 17",
        "Spring 2012": "January 9",
        "Summer 2012": "May 9",
        "Fall 2012": "August 20",
        "Spring 2013": "January 7",
        "Summer 2013": "May 13",
        "Fall 2013": "August 19",
        "Spring 2014": "January 13",
        "Summer 2014": "May 12",
        "Fall 2014": "August 18",
        "Spring 2015": "January 12",
        "Summer 2015": "May 11",
        "Fall 2015": "August 17",
        # Spring 2016 calendar also missing...
        "Summer 2016": "May 9",
        "Fall 2016": "August 16",
        "Spring 2017": "January 9",
        "Summer 2017": "May 8",
        "Fall 2017": "August 16",
        "Spring 2018": "January 7",
        "Summer 2018": "May 7",
        "Fall 2018": "August 22",
        "Spring 2019": "January 7",
        "Summer 2019": "May 8",
        "Fall 2019": "August 21",
        "Spring 2020": "January 6",
        "Summer 2020": "May 6",
        "Fall 2020": "August 17",
        "Spring 2021": "January 11",
        "Summer 2021": "May 10",
        "Fall 2021": "August 18",
        "Spring 2022": "January 18",
        "Summer 2022": "May 16",
        "Fall 2022": "August 17"
    }

    season_dict = {
        "Fall": 'August 1',
        "Summer": "May 15", 
        "Spring": "January 1"
    }

    if str(x) == 'Readmit' or str(x) == np.nan:
        return x
    try:
        year = str(x).split(' ')
        y = dt.strptime(start_dates[x] + ' ' + year[1], "%B %d %Y")
        return y
    except KeyError:
        try:
            z = str(x).split(' ')
            z = dt.strptime(season_dict[z[0]] + ' ' + z[1], "%B %d %Y")
            return z
        except:
            return x

def time_difference(x):
    y = dt.strptime(' '.join(x['Start Orientation Date']), "%Y %B %d")
    z = to_datetime(x['Admit Term'])

    try:
        return z - y
    except:
        return np.NaN

def main():

    # aggregate the data into a big dataframe
    df = data_to_df(pathlib.Path(os.getcwd()) / "data")    

    # eliminate unwanted columns
    df = eliminate_columns(df.transpose())

    # condense into 4 columns
    final_df = construct_result(df)

    # format filename and folder values
    final_df['Start Orientation Date'] = final_df['Start Orientation Date'].apply(lambda x: x.split("_Orientation")[0].split("_"))
    final_df['Orientation Year'] = final_df['Orientation Year'].apply(lambda x: x.split("\\")[-1].split("_"))
    final_df['Orientation Year'] = final_df['Orientation Year'].apply(lambda x: ' '.join(x))    

    # calculate time difference and format filename
    final_df['Admit Term - Orientation Start'] = final_df.apply(time_difference, axis=1)
    final_df['Start Orientation Date'] = final_df['Start Orientation Date'].apply(lambda x: ' '.join(x))

    # output results
    final_df.to_excel("final_df.xlsx")
    
if __name__ == "__main__":

    # Call main function.
    main()