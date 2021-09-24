"""
    File: funnel_report.py
"""

import argparse
import pandas as pd
import numpy as np
import re


def arguments():
    """ Parse arguments. """
    description = "Create report of what bins applications spend the most time in based on bin history."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-a", "--Applications", action="store",
                        help="Applications File", required=True)
    parser.add_argument("-p", "--Prospects", action="store",
                        help="Prospects File", required=True)
    return parser.parse_args()


def get_apps(apps, prospect_id):
    """ Get application IDs from apps_df based on given prospect ID. """

    results = apps[apps['Prospect ID'] == prospect_id]['Ref']
    return results.tolist()


def rank_apps(apps, app_refs):
    """ Determine higest ranking application for a prospect, if it exists. """

    if len(app_refs) > 0:

        status_ranking = {
            'Admit': 100,
            'Awaiting Conduct': 50,
            'Awaiting Confirmation': 70,
            'Awaiting Decision': 80,
            'Awaiting Materials': 10,
            'Awaiting Payment': 5,
            'Awaiting Submission': 0,
            'Cancelled': 0,
            'Decided': 90,
            'GR Cancelled': 0,
            'GR Reject - Academic Deficiency': 95,
            'GR Reject - Other': 95,
            'Reject': 95,
            'UG ACCESS Cancelled': 0
        }
        
        # print(app_refs)

        # Get applications for the prospect.
        relevant_apps = apps[apps['Ref'].isin(app_refs)]
        relevant_apps = relevant_apps[pd.notna(relevant_apps['Application Status'])]

        if relevant_apps.empty:
            return
        else:

            #print(relevant_apps['Application Status'])
            
            # Sort the DataFrame using status_ranking as a key.
            relevant_apps = relevant_apps.sort_values(by='Application Status', key=lambda x: x.apply(lambda y: status_ranking[str(y)]), ascending=False).reset_index()
            # print(relevant_apps)
            # quit()
            #print(relevant_apps)

            # Return highest-ranking Application Status.
            return int(relevant_apps.iloc[0]['index'])
    else:
        return


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
    apps_df['Program'] = np.where(apps_df["GR Academic Interest (App)"].isnull(), apps_df["UG Academic Interest (App)"], apps_df["GR Academic Interest (App)"])
    apps_df['Entry Term'] = np.where(apps_df["UG Entry Term (App)"].isnull(), apps_df["GR Entry Term (App)"], apps_df["UG Entry Term (App)"])

    del apps_df['GR Academic Interest (App)']
    del apps_df['UG Academic Interest (App)']
    del apps_df['GR Entry Term (App)']
    del apps_df['UG Entry Term (App)']
    
    # Match up applications to prospect records.
    prospects_df['Apps'] = prospects_df.apply(lambda x: get_apps(apps_df, x['Prospect ID']), axis=1)

    # Testing relation.
    # print(prospects_df.iloc[10000])
    # print(apps_df[apps_df['Ref'].isin(prospects_df.iloc[10000]['Apps'])])

    # Determine outcomes for each application.
    # If App status is "Decided", pull "Decision Confirmed Name", else use value from App status.
    # May need to normalize decisions (all "Admit _____" or "GR Admit ______" can just be "Admit")
    apps_df['Decision Confirmed Name'] = np.where(apps_df['Decision Confirmed Name'].isnull(), '',apps_df['Decision Confirmed Name'])
    apps_df['Decision Confirmed Name'] = np.where(apps_df['Decision Confirmed Name'].str.contains(pat='Admit'), 'Admit',apps_df['Decision Confirmed Name'])
    apps_df['Application Status'] = np.where(apps_df['Application Status'] == 'Decided', apps_df['Decision Confirmed Name'], apps_df['Application Status'])
    apps_df['Application Status'] = np.where(apps_df['Application Status'] == '', 'Decided', apps_df['Application Status'])

    del apps_df['Decision Confirmed Name']

    # print(apps_df.head())
    # print(prospects_df.head())
    
    # Rank/Sort applications by 'Application Status'.
    prospects_df['Furthest App'] = prospects_df.apply(lambda x: rank_apps(apps_df, x['Apps']), axis=1)

    # Make another column for Furthest app's Program and Entry Term, and Application Status
    # Fill Nan values in Furthest Application Status with "Prospect"

    print(prospects_df['Furthest App'].head(30))
    print(apps_df.iloc[int(prospects_df.iloc[10]['Furthest App'])])
    #prospects_df['Furthest App'] = np.where(prospects_df['Furthest App'].isnull(), 'Prospect', prospects_df['Furthest App'])
    #prospects_df['App Entry Term'] = np.where(pd.notna(prospects_df['Furthest App']), apps_df.iloc[int(prospects_df['Furthest App'])]['Entry Term'], None) 

    # For each prospect, compare furthest application term to prospect entry term. "Entry Term Match?"
    # If they match, "match", if one lataer, "later", etc.


    # Count prospects, application steps and outcomes by program.
    programs_df = pd.read_csv('programs.csv')

    # Compare prospect program and furtherest application program to see if they match or not. Could put result in new column "Program Match?"
    # for each, get row from programs_df where app_program == prospect->furthest app->Program, then pull prospect_program from programs_df, then compare that to prospect->Program

    # Once we have the program mapping, it should be just general data cleanup (renaming columns, things like that), then calling pd.pivot()


if __name__ == '__main__':
    # Parse CLI arguments.
    ARGS = arguments()

    # Call main function.
    main(ARGS.Applications, ARGS.Prospects)
