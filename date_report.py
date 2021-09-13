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


def to_linked_list(list, key):
    LList = List(key)

    for i in range(len(list)):
        node = Node()
        node.bin_name = list[i]
        if (i+1 != len(list)):
            node.list_data.append(list[i+1])

        LList.append(node)     

    return LList


def fill_gaps(history_link, good_link):
    history_node = history_link.head
    good_node = good_link.head
    
    while history_node is not None and good_node is not None:
        if history_node.bin_name == good_node.bin_name:
            history_node = history_node.next
            good_node = good_node.next
        else:
            node = Node()
            node.bin_name = good_node.bin_name
            node.date_completed = history_node.date_completed

            history_link.insert_before(node, history_node)
            good_node = good_node.next

    return history_link

def main(query):
    """ Create report from query export. """
    
    #Bin Order Listing
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
        'Released Decision']
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
        'Matric']
    ra_bin_order = [
        'Conduct Committee Review',
        'Review (Spring)',
        'Review (Summer and Fall)',
        'Further Review',
        'Readmit',
        'Not a Readmit',
        'Conduct Review Reject']
    
    '''
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
    '''
    # Step 1: Build linked lists for bin history data.
    ug_link = to_linked_list(ug_bin_order, "UG")
    ga_link = to_linked_list(ga_bin_order, "GR")
    ra_link = to_linked_list(ra_bin_order, "RA")

    good_link_dict = {
        'UG': ug_link,
        'GR': ga_link,
        'RA': ra_link
    }
    # Pandas options for debugging.
    pd.set_option('display.width', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)

    
    
    # Read input file into Pandas dataframe.
    query_df = pd.read_csv(query)

    # Create new column containing python list of each application's bin history.
    query_df['Bin History List'] = query_df['Bin History'].apply(split_history)

    # Include only applications that have at least two bin history items.
    query_df['History Length'] = query_df['Bin History List'].apply(lambda x: 0 if [] else len(x))
    query_df = query_df[query_df['History Length'] > 1]

    # Create a linked list of bin history items and their data, including round key, bin names, and bin dates.
    query_df['Bin History List'] = query_df.apply(lambda x: split_history_items(x['Bin History List'], x['Round Key']), axis=1)

    # Reset the index after filtering for easy indexing.
    query_df = query_df.reset_index(drop=True)

    # Display a sample linked list object.
    print(query_df['Bin History List'].loc[0].display())
    # Step 2: Compare linked lists to known good ones and fill in the gaps.
    query_df['Bin History List'] = query_df.apply(lambda x: fill_gaps(x['Bin History List'], good_link_dict[x['Round Key']]), axis=1)

    print(query_df['Bin History List'].loc[0].display())
    # Step 3: Calculate date diff for each step in the path.

    # Step 4: Run basic statistics for date differences per bin movement using the pandas describe() function.

if __name__ == '__main__':
    # Parse CLI arguments.
    ARGS = arguments()

    # Call main function.
    main(ARGS.Input)