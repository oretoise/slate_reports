"""
File: ytd_report.py
"""

import argparse
import numpy as np
import pandas as pd

import time
import datetime

def arguments():
    """ Parse CLI arguments. """
    description = "Create a year-to-date report of application data."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-i", "--Input", action="store", help="Application Data File", required=True)
    parser.add_argument("-d", "--Date", action="store", help="Cutoff date, in YYYY-MM-DD format", required=True)
    return parser.parse_args()


def bin_history_filter(bh_list_str, cutoff):
    """ Mark data for deletion in th bin history column. """

    # Ignore any application with no bin history.
    if pd.isna(bh_list_str):
        return
    
    # Split bin history string by comma.
    bh_list = str(bh_list_str).split(",")

    # List to return
    ret_list = list()

    # Walk through each one, splitting by dash, comparing the data
    for bin_status in bh_list:
        bin_status_tuple = bin_status.split("-")
        bin_date = bin_status_tuple[0].strip()
        bin_dt_object = datetime.datetime.strptime(bin_date, "%m/%d/%Y")

        if bin_dt_object < cutoff:
            ret_list.append(bin_status)
    
    return ret_list


def convert_to_datetime(timestamp):

    # Ignore pd.NaT values.
    if pd.isnull(timestamp):
        return "None"

    # Strip the decimal after the seconds.
    new_timestamp = str(timestamp).split('.')[0]

    # Convert to datetime object.
    dt_object = datetime.datetime.strptime(new_timestamp, "%Y-%m-%d %H:%M:%S")

    return dt_object


def date_filter(timestamp, cutoff):
    """ Mark data for deletion if it occurs after the provided cutoff date. """

    # Convert timestamp to datetime object.
    dt_object = convert_to_datetime(timestamp)

    if dt_object == "None":
        return dt_object
    else:
        # Compare against cutoff date.
        if dt_object > cutoff:
            return "Future"
        else:
            return dt_object


def strip_time(timestamp):
    """ Remove HH:MM:SS.YYYY from Slate-provided timestamp. """

    dt_object = convert_to_datetime(timestamp)

    if dt_object == "None":
        return None
    else:
        # Return just the date.
        return dt_object.date()


def status(bin_history):
    """ Grab the application status based on the bin history. """
    # First item in the bin history list is the latest, so grab just that one.
    
    # Ignore any applications where there is no bin history.
    if not bin_history:
        return "Awaiting Submission"

    # Split bin history string by comma.
    #bh_list = str(bin_history).split(",")

    # Grab just the first entry.
    status_date = str(bin_history[0])
    #print(status_date)

    # Split that one by the dash (-)
    if "-" in status_date:
        status_date_list = status_date.split("-")
    else:
        return "Awaiting Submission"
    
    # Clear any whitespace.
    status = status_date_list[1].strip()

    return status


def current_status(bin_history):
    """ Grab the application status based on the bin history. """
    # First item in the bin history list is the latest, so grab just that one.
    
    # Ignore any applications where there is no bin history.
    if pd.isna(bin_history):
        return "Awaiting Submission"

    # Split bin history string by comma.
    bh_list = str(bin_history).split(",")

    # Grab just the first entry.
    status_date = str(bh_list[0]).strip()
    #print(status_date)

    # Split that one by the dash (-)
    if "-" in status_date:
        status_date_list = status_date.split("-")
    else:
        return "Awaiting Submission"
    
    # Clear any whitespace.
    status = status_date_list[1].strip()

    return status


def main(applications, cutoff):
    """ Generate YTD report """

    # Read in the provided file.
    apps_df = pd.read_excel(applications, engine="openpyxl")

    # Coalesce program fields into main one.
    apps_df['Entry Term'] = np.where(apps_df["UG Entry Term (App)"].isnull() == True, apps_df["GR Entry Term (App)"], apps_df["UG Entry Term (App)"])

    # Remove separate program fields.
    del apps_df["UG Entry Term (App)"]
    del apps_df["GR Entry Term (App)"]

    # Copy dataframe into new one.
    current_df = apps_df.copy()

    


    # Filter any date values from apps_df.
    # Convert the cutoff date into a datetime object.
    cutoff_date = datetime.datetime.strptime(cutoff, "%Y-%m-%d")

    # Go through each column containing datetime data, and mark any elements newer than the cutoff date.
    date_columns = "App Submitted", "Created", "Decision Confirmed Date" # as well as bin history, but it's special

    for column in date_columns:
        apps_df[column] = apps_df[column].apply(lambda x: date_filter(x, cutoff_date))
    
    # Filter out bin history column as well.
    apps_df['Bin History'] = apps_df['Bin History'].apply(lambda x: bin_history_filter(x, cutoff_date))
    
    # Filter any rows with Created date equal to "Future"
    apps_df = apps_df[apps_df.Created != "Future"]

    # Set any "Future" values in "App Submitted" and "Decision Confirmed Date" to "None".
    apps_df.loc[apps_df["App Submitted"] == "Future", "App Submitted"] = "None"
    apps_df.loc[apps_df["Decision Confirmed Date"] == "Future", "Decision Confirmed Date"] = "None"

    # Generate application status column.
    apps_df["Status"] = apps_df['Bin History'].apply(status)
    apps_df["Status"] = np.where(apps_df["Decision Released Name"].isnull() == False, apps_df["Decision Released Name"], apps_df["Status"])
    apps_df["Status"] = np.where(apps_df["Enrolled Flag"] == 1.0, "Enrolled", apps_df["Status"])

    current_df["Status"] = current_df['Bin History'].apply(current_status)
    current_df["Status"] = np.where(current_df["Decision Released Name"].isnull() == False, current_df["Decision Released Name"], current_df["Status"])
    current_df["Status"] = np.where(current_df["Enrolled Flag"] == 1.0, "Enrolled", current_df["Status"])

    # Clean up current_df a bit.
    columns_to_convert = "App Submitted", "Created", "Decision Confirmed Date"
    for column in columns_to_convert:
        current_df[column] = current_df[column].apply(strip_time)


    # Make two new dataframes of just the program and application status.
    old_df = apps_df[['Entry Term', 'Status']]
    new_df = current_df[['Entry Term', 'Status']]


    # Print dataframe for now.
    #print(apps_df)
    #print(current_df)

    #print(old_df)
    #print(new_df)

    # Make pivot table for both.
    old_table = old_df.pivot_table(index="Entry Term", columns="Status", aggfunc='size')
    new_table = new_df.pivot_table(index="Entry Term", columns="Status", aggfunc='size')

    # Rename columns to "- old"
    old_table = old_table.rename(columns = lambda x: x + " - Old")

    # Merge both.
    merge = pd.concat([old_table, new_table], axis=1)

    # Reorder columns alphabetically.
    columns = merge.columns.tolist()
    columns.sort()
    merge_sorted = merge[columns]


    merge_sorted.to_csv('merge.csv')


if __name__ == "__main__":
    # Parse CLI arguments.
    ARGS = arguments()

    # Call main function.
    main(ARGS.Input, ARGS.Date)