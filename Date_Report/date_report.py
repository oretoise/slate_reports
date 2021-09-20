"""
    File: date_report.py
"""

import argparse
import pandas as pd

from classes import Node, List
import bins

def arguments():
    """ Parse arguments. """
    description = "Create report of what bins applications spend the most time in based on bin history."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-i", "--Input", action="store", help="Query File", required=True)
    return parser.parse_args()


def split_history(bin_history):
    """ Splits the provided bin history list into a consistent format. """

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
    ''' Create the linked list for a given bin history list. '''

    # Create a new linked list object.
    bin_link = List(key)

    # For each item in the bin history:
    for item in bin_history:

        # Make a new node object.
        node = Node()

        # Set the bin_name and date_completed members.
        node.set_data_split(item)
        
        # Append each bin history item in chronological order.
        tmp = bin_link.head
        while (tmp != None):
            if node.date_completed > tmp.date_completed:
                tmp = tmp.next
                continue
            break
        bin_link.insert_before(node, tmp)

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


def validate(history_linked_list, bin_df):
    """ Validate given Bin History list against the bin movement rules in bin_df. """

    # Skip for now.
    if bin_df is None:
        return history_linked_list
    else:
        # Validate
        print("List is", history_linked_list.display())
        
        # Walk through the nodes.
        node = history_linked_list.head
        possibilities = ["Awaiting Submission"]

        # At any time, an application can be cancelled and move to the Cancel bin, except for Readmission applications.
        
        while node != None:

            # Is it what we expect?
            print("\nLooking for", node.bin_name, "in", possibilities)

            if node.bin_name in possibilities:
                # Node is what we expect.
                print("This is what we expected.")
                print("Getting possibilities for next appropriate node.")

                # Filter the bin DataFrame to just the one we need.
                bin = bin_df[bin_df['name'] == node.bin_name].reset_index(drop=True)

                # Get the possibile next bins from it.
                possibilities = bin['next'].loc[0]
                print("Possibilities are:", possibilities)

                # Move on to the next node.
                node = node.next
            else:
                print("Current node not in possibilities of prior node. Correction needed.\n")
                
                
                # Finds node_bin name in item possibilities
                '''
                for item in possibilities:
                    
                    possible = bin_df[bin_df['name'] == item].reset_index(drop=True)['next'].loc[0]

                    print("Looking for", node.bin_name, "in", item, possible)

                    if node.bin_name in possible:
                        print(node.bin_name, "found in", possible)
                        print("Inserting", item, "before", node.bin_name)

                        fill_node = Node()
                        fill_node.bin_name = item
                        history_linked_list.insert_before(fill_node, node)
                        break
                        
                node = node.next    
                '''

                # TODO: Determine which node(s) to insert and insert them using insert_before().

                # Traverse the list of possibilites searching for current node in each item's next
                # if we cannot find it insert first required item
                # Keep track of set and required possibilites
                    #[  for item in possibilites 
                    # if current node in items['next']

                    # else if item type == required
                    #]
                
                
                quit()

            # If optional: go through each bin in the sequence.

            # If set, do we have at least one item from the set, in the appropriate order?

            #print(node)
            #index = index + 1
            #node = node.next

        return


def main(query):
    """ Create report from query export. """
    
    #Bin Order Listing
    ug_bin_order = [
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
    
    
    # Step 1: Build linked lists for bin history data.
    good_link_dict = {
        'UG': to_linked_list(ug_bin_order, "UG"),
        'GR': to_linked_list(ga_bin_order, "GR"),
        'RA': to_linked_list(ra_bin_order, "RA")
    }

    # Import bin structures from bins.py
    undergrad_bin_df = bins.undergrad()

    bin_dataframes = {
        "UG": undergrad_bin_df,
        "GR": None,
        "RA": None
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
    #print("Sample bin history before adjustment:")
    #print(query_df['Bin History List'].loc[0].display())

    # Run each application's bin history through the validation function, filling in gaps as necessary. 
    query_df['Validation'] = query_df.apply(lambda x: validate(x['Bin History List'], bin_dataframes[x['Round Key']]), axis=1)

    print(query_df[query_df['Round Key'] == 'UG'].reset_index(drop=True).loc[0])

    # Step 2: Compare linked lists to known good ones and fill in the gaps.
    query_df['Bin History List'] = query_df.apply(lambda x: fill_gaps(x['Bin History List'], good_link_dict[x['Round Key']]), axis=1)

    #print("Sample bin history after adjustment:")
    #print(query_df['Bin History List'].loc[0].display())

    # Step 3: Calculate date diff for each step in the path.

    # Step 4: Run basic statistics for date differences per bin movement using the pandas describe() function.

if __name__ == '__main__':
    # Parse CLI arguments.
    ARGS = arguments()

    # Call main function.
    main(ARGS.Input)