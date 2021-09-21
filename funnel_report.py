"""
    File: funnel_report.py
"""

import argparse
import pandas as pd


def arguments():
    """ Parse arguments. """
    description = "Create report of what bins applications spend the most time in based on bin history."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-a", "--Applications", action="store", help="Applications File", required=True)
    parser.add_argument("-p", "--Prospects", action="store", help="Prospects File", required=True)
    return parser.parse_args()


def main(apps, prospects):
    """ Build funnel report based on prospects and applications data. """

    # Pandas options for debugging.
    pd.set_option('display.width', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)

    # Load apps and prospects files into DataFrames.
    apps_df = pd.read_csv(apps)
    prospects_df = pd.read_csv(prospects)

    # Clean up apps_df by setting "Program" and "Entry Term" columns based on "Round Key".

    #print(apps_df.head())
    

    # Match up applications to prospect records.
    #print(prospects_df.apply(lambda x: apps[apps['Prospect ID'] == x['Prospect ID']], axis=1))
    first = prospects_df.loc[0]['Prospect ID']

    print(first)
    print(apps_df[apps_df['Prospect ID'] == first]['Ref'])

    prospects_df['Apps'] = prospects_df.apply(lambda x: apps_df[apps_df['Prospect ID'] == x['Prospect ID']]['Ref'], axis=1)

    # Determine outcomes for each application.

    # For each prospect, compare application outcomes to initial entry term.

    # Count prospects, application steps and outcomes by program. (Need mapping for prospect program -> app program.)


if __name__ == '__main__':
    # Parse CLI arguments.
    ARGS = arguments()

    # Call main function.
    main(ARGS.Applications, ARGS.Prospects)