"""
    File: date_report.py
"""

import argparse
import pandas as pd

from classes import Node, List

def arguments():
    """ Parse arguments. """
    description = "Create report of what bins applications spend the most time in based on bin history."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-i", "--Input", action="store", help="Query File", required=True)
    return parser.parse_args()


def split_history(bin_history):
    """ Splits the provided bin history list. """

    # If there is no bin history, return an empty list.
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


def split_history_items(bin_history, key):
    '''
    # Bin Order Listing
    ug_bin_order = [
        'Awaiting Submission',
        'Conduct Committee Review',
        'Conduct Committee Approved',
        'Awaiting Payment',
        'Awaiting Materials',
        'Not a New Admission',
        'Ready to Review-Freshmen',
        'Ready to Review-Transfers',
        'Awaiting Additional Materials',
        'ARNR Committee',
        'ARNR Approved',
        'ARNR Awaiting Materials',
        'Transfer Reject Committee',
        'Refer to Test',
        'Ready to Admit',
        'Ready to Admit (Contingent)',
        'Ready to Deny',
        'Conduct Committee Reject',
        'Cancel',
        'Awaiting Release',
        'Released Decision'
    ]

    re_bin_order = [
        'Conduct Committee Review',
        'Review (Spring)',
        'Review (Summer and Fall)',
        'Further Review',
        'Readmit',
        'Not a Readmit',
        'Conduct Review Reject',
    ]

    ga_bin_order = [
        'Awaiting Submission',
        'Awaiting Payment',
        'Conduct Committee Review',
        'Conduct Committee Approved',
        'Fee Waiver Review',
        'Awaiting Materials',
        'Admissions Review', 
        'Awaiting Additional Materials',
        'Unaccredited',
        'Unclassified', 
        'Departmental Preview', 
        'Department Review',
        'Department Final Review',
        'College Dean Review', 
        'Dean of Grad School Review', 
        'Export Control',
        'Ready to Admit',
        'Ready to Admit (Contingent)',
        'Ready to Admit (Provisional)',
        'Ready to Deny',
        'Cancel',
        'Conduct Committee Reject',
        'Awaiting Release',
        'Released Decision', 
        'Official Await',
        'Matric'
    ]
    '''

    # Create a new linked list object.
    bin_link = List(key)

    # For each item in the bin history:
    for item in bin_history:

        # Make a new node object.
        node = Node()

        # Set the bin_name and date_completed members.
        node.set_data_split(item)
        

        tmp = bin_link.head
        while (tmp != None):
            if node.date_completed > tmp.date_completed:
                tmp = tmp.next
                continue
            break
        bin_link.insert_before(node, tmp)
        '''
        while (tmp1 != None):
            if node.bin_name < tmp.bin_name:
                tmp = tmp.next
                continue
            break
        bin_link.insert_before(node, tmp1)
        '''

    return bin_link


def to_linked_list(list):
    LList = List()

    for i in range(len(list)):
        node = Node()
        node.bin_name = list[i]
        if (i+1 != len(list)):
            node.list_data.append(list[i+1])

        LList.append(node)     

    return LList


def main(query):
    """ Create report from query export. """

    # Pandas options for debugging.
    pd.set_option('display.width', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)

    #Bin Order Listing
    ug_bin_order = {
        'Awaiting Submission': 1,
        'Conduct Committee Review':2,
        'Conduct Committee Approved':3,
        'Awaiting Payment':4,
        'Awaiting Materials':5,
        'Not a New Admission':6,
        'Ready to Review-Freshmen':7,
        'Ready to Review-Transfers':8,
        'Awaiting Additional Materials':9,
        'ARNR Committee':10,
        'ARNR Approved':11,
        'ARNR Awaiting Materials':12,
        'Transfer Reject Committee':13,
        'Refer to Test':14,
        'Ready to Admit':15,
        'Ready to Admit (Contingent)':16,
        'Ready to Deny':17,
        'Conduct Committee Reject':18,
        'Cancel':19,
        'Awaiting Release':20,
        'Released Decision':21
    }

    re_bin_order = {
        'Conduct Committee Review':1,
        'Review (Spring)':2,
        'Review (Summer and Fall)':3,
        'Further Review':4,
        'Readmit':5,
        'Not a Readmit':6,
        'Conduct Review Reject':7,
    }

    ga_bin_order = {
        'Awaiting Submission':1,
        'Awaiting Payment':2,
        'Conduct Committee Review':3,
        'Conduct Committee Approved':4,
        'Fee Waiver Review':5,
        'Awaiting Materials':6,
        'Admissions Review':7, 
        'Awaiting Additional Materials':8,
        'Unaccredited':9,
        'Unclassified':10, 
        'Departmental Preview':11, 
        'Department Review':12,
        'Department Final Review':13,
        'College Dean Review':14, 
        'Dean of Grad School Review':15, 
        'Export Control':16,
        'Ready to Admit':17,
        'Ready to Admit (Contingent)':18,
        'Ready to Admit (Provisional)':19,
        'Ready to Deny':20,
        'Cancel':21,
        'Conduct Committee Reject':22,
        'Awaiting Release':23,
        'Released Decision':24, 
        'Official Await':25,
        'Matric':26
    }


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

    # Include only applications that have at least two bin history items.
    query_df['History Length'] = query_df['Bin History List'].apply(lambda x: 0 if [] else len(x))
    query_df = query_df[query_df['History Length'] > 1]

    # Split each (date - bin) pair into a list containing the date and bin name as separate objects.
    query_df['Bin History List'] = query_df.apply(lambda x: split_history_items(x['Bin History List'], x['Round Key']), axis=1)

    # Reset the index after filtering for easy indexing.
    query_df = query_df.reset_index(drop=True)

    # Display a sample linked list object.
    print(query_df['Bin History List'].loc[0].display())

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

    #print(query_df['Bin History List'].loc[4].head.next.bin_name)

if __name__ == '__main__':
    # Parse CLI arguments.
    ARGS = arguments()

    # Call main function.
    main(ARGS.Input)