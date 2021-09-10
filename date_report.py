"""
    File: date_report.py
"""

import argparse
import pandas as pd

from datetime import date, timedelta

from classes import Node, List

def arguments():
    """ Parse arguments. """
    description = "Create report of what bins applications spend the most time in based on bin history."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-i", "--Input", action="store", help="Query File", required=True)
    return parser.parse_args()


def split_history(bin_history):
    """ Splits the provided bin history list. """

    # If there is no bin history, return nothing.
    if pd.isna(bin_history):
        return []

    # Otherwise do some processing.
    else:

        # Build up list of bins.
        bin_list = []

        # If there is more than one, split them into a list.
        if ',' in bin_history:
            bin_list = bin_history.split(',')
        
        # Otherwise, use a one-item list.
        else:
            bin_list = [bin_history]
        
        return bin_list

def split_history_items(bin_history):
    bin_link = List()

    for item in bin_history:
        node = Node()
        node.set_data_split(item)
        
        tmp = bin_link.head
        while (tmp != None):
            if node.date_completed > tmp.date_completed:
                tmp = tmp.next
                continue
            break
        bin_link.insert_before(node, tmp)
    
    return bin_link






def main(query):
    """ Create report from query export. """

    # Pandas options for debugging.
    pd.set_option('display.width', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)

    # Bin Order Listing
    bin_order = [
        'Awaiting Submission',
        'Awaiting Payment'
    ]

    # UG bin order
        # Awaiting Submission -> Awaiting Payment -> Awaiting Materials -> either Ready to Review or Awaiting Materials 
    # GR bin order
    # RA bin order

    # "07/13/2021 - Awaiting Materials, 07/13/2021 - Awaiting Submission"
    # ["07/13/2021 - Awaiting Materials", "07/13/2021 - Awaiting Submission"]
    # [Object: {date -> 07/13/2021, bin -> "Awaiting Submission", next_bin -> "Awaiting Materials"}, Object : {}]
    
    # Read input file into Pandas dataframe.
    query_df = pd.read_csv(query)

    

    # Create new column containing python list of each application's bin history.
    query_df['Bin History List'] = query_df['Bin History'].apply(split_history)
    query_df['History Length'] = query_df['Bin History List'].apply(lambda x: 0 if [] else len(x))
    # Only process if length of bin history list > 1.
    query_df = query_df[query_df['History Length'] > 1]

    # Filter out records where bin history is none.
    #query_df = query_df[query_df['Bin History List'] != 'none']

    # Split each (date - bin) pair into a list containing the date and bin name as separate objects.
    #query_df['Bin History List'] = query_df['Bin History List'].apply(split_history_items)
    query_df['Bin History List'] = query_df['Bin History List'].apply(split_history_items)
    # Sort BH list by date, oldest to latest, then by status list.
    #query_df['Bin History List'] = query_df['Bin History List'].apply(lambda x: x.sort('date'))

    # List of statuses by progress (Awaiting Submission -> Payment -> Materials -> Ready to Review -> Awaiting Decision -> Released Decision, everything in between.)

    # Build bin history path df, assume logical order (see ^) for same day movement. If a record goes back, make new movement row for the same ref.
    # For skips, what should I assume? Perhaps moved on the date of the next step?
    # Include program on movement_df

    # Calculate date diff for each step in the path.
    # Third DF: status_movement_df
    # Calculate total days for each application status step (Submission, Payment, Materials, Review, Dept Review, Decision, Decision Release, Post-release (enroll, matric))
    # Pivot table that by program (coalesce program based on round key)

    print(query_df['Bin History List'].head(5))

if __name__ == '__main__':
    # Parse CLI arguments.
    ARGS = arguments()

    # Call main function.
    main(ARGS.Input)