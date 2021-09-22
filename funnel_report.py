"""
    File: funnel_report.py
"""

import argparse
import pandas as pd
import time


def arguments():
    """ Parse arguments. """
    description = "Create report of what bins applications spend the most time in based on bin history."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-a", "--Applications", action="store", help="Applications File", required=True)
    parser.add_argument("-p", "--Prospects", action="store", help="Prospects File", required=True)
    return parser.parse_args()


def get_apps(apps, prospect_id):
    """ Get application IDs from apps_df based on given prospect ID. """
    #print("Looking for", prospect_id)
    #print(apps.head())

    results = apps[apps['Prospect ID'] == prospect_id]['Ref']
    #return results
    if results.empty:
        return []
    else:
        # print("Found Refs", results)
        return results.tolist()


def main(apps, prospects):
    """ Build funnel report based on prospects and applications data. """

    # Pandas options for debugging.
    pd.set_option('display.width', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)

    # Load apps and prospects files into DataFrames.
    apps_df = pd.read_csv(apps)
    prospects_df = pd.read_csv(prospects)

    # TODO: Clean up apps_df by setting "Program" and "Entry Term" columns based on "Round Key".
    # Ex: If round key is UG, set Program to UG Academic Interest, and set Entry Term to UG Entry Term (App)
    #print(apps_df.head())

    # Match up applications to prospect records.
    prospects_df['Apps'] = prospects_df.apply(lambda x: get_apps(apps_df, x['Prospect ID']), axis=1)

    # Determine outcomes for each application.
    # If App status is "Decided", pull "Decision Confirmed Name", else use value from App status.
    # May need to normalize decisions (all "Admit _____" or "GR Admit ______" can just be "Admit")

    # Determine general outcome for prospect overall.
    # Ranking of app status, use application outcome for furthest along.

    # For each prospect, compare application outcomes to initial entry term.
    # If they match, "match", if one lataer, "later", etc.

    # Count prospects, application steps and outcomes by program. (Need mapping for prospect program -> app program.)
    programs_df = pd.read_csv('programs.csv')
    # Once we have the program mapping, it should be just general data cleanup (renaming columns, things like that), then calling pd.pivot()


if __name__ == '__main__':
    # Parse CLI arguments.
    ARGS = arguments()

    # Call main function.
    main(ARGS.Applications, ARGS.Prospects)