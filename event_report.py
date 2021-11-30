"""
File: event_report.py
"""

import argparse
import numpy as np
import pandas as pd
import Google.gsheets as gsheets


def arguments():
    """ Parse CLI arguments. """
    description = "Generate report on event registrations in Slate."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-i", "--Input", action="store", help="Event Registration Data File", required=True)
    return parser.parse_args()


def process_application_history(app_history):
    """ Return list of decision codes from comma-separated application history, if they exist. """

    ranking = {
        'Admit Contingent': 25,
        'Admit': 50,
        'Cancelled': 0,
        'GR Admit Contingent': 80,
        'GR Admit Provisional': 80,
        'GR Admit Regular': 100,
        'GR Cancelled': 5,
        'GR Reject - Academic Deficiency': 5,
        'GR Reject - Other': 5,
        'No Decision': 0
    }

    # If there is no application history, return nothing.
    if pd.isna(app_history):
        return

    # Otherwise do some processing.
    else:

        # Build up list of decisions for the applicant.
        decisions = []

        # If there is more than one, split them into a list.
        if ',' in app_history:
            decisions = app_history.split(',')
        
        # Otherwise, use a one-item list.
        else:
            decisions = [app_history]
        
        # List to store decision codes for the applicant.
        codes = []
        
        # For each decision, whether one or multiple, grab just the decision code.
        for decision in decisions:
            codes.append(decision.split(':')[1].strip())
        
        # Return highest ranking decision.
        return sorted(codes, key = lambda x: ranking[x], reverse=True)[0]
        

def process_events(events_list):
    """ Generate list of events attended. """
    if pd.isna(events_list):
        return
    else:
        events = []

        if ',' in events_list:
            events = events_list.split(',')
        else:
            events = [events_list]
        
        event_names = []
        for event in events:
            event_names.append(event.split(':')[-1].strip())
        
        return event_names


def status(row):
    """ Generate prospect status based on Status, Decision, and Enrolled columns. """
    if row['Status'] == 'Inquiry':
        return 'Inquiry'
    elif row['Status'] == 'Applicant':
        if row['Enrolled'] == 1:
            return 'Enrolled'
        elif 'Admit' in row['Decision']:
            return 'Admit'
        else:
            return 'Applicant'


def main(input_file):
    """ 
        Generate event report.

        Request:
            the number of events that were held online and the number of attendees?
            Is it possible to find out how many students who attended those events got admitted?
            Were they all held with community colleges or were there others? - would have to check the cc fairs folder in slate or have mindy determine
    """

    # Read input file into pandas.
    event_df = pd.read_csv(input_file, encoding = 'unicode_escape')

    # Remove some unneeded columns.
    to_remove = [
        "Distance - Academic Program",
        "Event - Most Recent Registration Event Date/Time",
        "Event - Most Recent Registration Summary",
        "Event - First Registration Summary",
        "Event - First Registration Event Date/Time"]
    
    for column in to_remove:
        del event_df[column]
    
    # Coalesce enrolled flag fields into one.
    event_df['Enrolled'] = np.where(event_df["Enrolled Flag"].isnull() == True, event_df["GR Enrolled Flag"], event_df["Enrolled Flag"])
    del event_df['Enrolled Flag']
    del event_df['GR Enrolled Flag']

    # If there is a decision, grab the most important one.
    event_df['Decision'] = event_df['Application History (comma)'].apply(process_application_history)

    # Remove the Application History column.
    del event_df['Application History (comma)']

    # Generate a list of event(s) attended.
    event_df['Events'] = event_df['Events - Comma Separated'].apply(process_events)

    # Remove the Application History column.
    del event_df['Events - Comma Separated']

    # Generate overall prospect status based on Status, Decision, and Enrolled columns.
    event_df['Status'] = event_df.apply(status, axis=1)

    # Remove Enrolled and Decision columns.
    del event_df['Enrolled']
    del event_df['Decision']

    # Explode the Events column.
    explosion = event_df.explode('Events')

    # Filter out any events with a date between 8/1/2020 and 5/31/2021.
    explosion['Event Date'] = explosion['Events'].apply(lambda x: x.split('-')[-1].strip())
    explosion['Event Date'] = explosion['Event Date'].apply(lambda x: pd.to_datetime(x, format="%m/%d/%Y"))
    explosion = explosion[(explosion['Event Date'] > "2020-07-31") & (explosion['Event Date'] < "2021-06-01")]

    # Generate pivot table of events attended by application status.
    event_pivot = pd.pivot_table(explosion, values='Name', index='Events', columns='Status', aggfunc='count', fill_value=0, margins=True)

    # Output pivot table to a CSV.
    # event_pivot.to_csv('pivot.csv')

    # Push to Gsheets
    client = gsheets.authorize()
    gsheets.set_dataframe(client, event_pivot, "Event Pivot")
    
if __name__ == "__main__":
    # Parse CLI arguments.
    ARGS = arguments()

    # Call main function.
    main(ARGS.Input)