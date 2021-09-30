"""
    File: funnel_report.py
"""

import argparse
import pandas as pd
import numpy as np
import xlsxwriter
from matplotlib import pyplot as plt


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


def program_match(row, programs):
    program = row.Program
    app_program = row['App Program']


    if programs[programs.app_program == app_program].prospect_program.empty:
        return None

    prospect_program = programs[programs.app_program == app_program].prospect_program

    if (prospect_program == program).bool():
        return 'Match'
    else:
        return 'No Match'


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
    
    # Rank/Sort applications by 'Application Status'.
    prospects_df['Furthest App'] = prospects_df.apply(lambda x: rank_apps(apps_df, x['Apps']), axis=1)

    # Make another column for Furthest app's Program and Entry Term, and Application Status
    prospects_df['App Entry Term'] = prospects_df.apply(lambda x: apps_df.iloc[int(x['Furthest App'])]['Entry Term']
                                     if pd.notna(x['Furthest App']) else None, axis=1)

    prospects_df['App Program'] = prospects_df.apply(lambda x: apps_df.iloc[int(x['Furthest App'])]['Program']
                                     if pd.notna(x['Furthest App']) else None, axis=1)

    # Fill Nan values in Furthest Application Status with "Prospect"
    prospects_df['Furthest App Status'] = prospects_df.apply(lambda x: apps_df.iloc[int(x['Furthest App'])]['Application Status']
                                     if pd.notna(x['Furthest App']) else None, axis=1)

    prospects_df['Furthest App Status'] = np.where(prospects_df['Furthest App Status'].isnull(), 'Prospect', prospects_df['Furthest App Status'])

    # For each prospect, compare furthest application term to prospect entry term. "Entry Term Match?"
    prospects_df['Entry Term Match'] = np.where(prospects_df['Term']==prospects_df['App Entry Term'], 'Match', 'Later')

    # Count prospects, application steps and outcomes by program.
    programs_df = pd.read_csv('programs.csv')

    # Compare prospect program and furtherest application program to see if they match or not. Could put result in new column "Program Match?"
    # for each, get row from programs_df where app_program == prospect->furthest app->Program, then pull prospect_program from programs_df, then compare that to prospect->Program
    prospects_df['Program Match'] = prospects_df.apply(lambda x: program_match(x, programs_df), axis=1)

    # Once we have the program mapping, it should be just general data cleanup (renaming columns, things like that), then calling pd.pivot()
    del prospects_df['Birthdate']
    del prospects_df['Email']
    del prospects_df['Campus']
    del prospects_df['Created']
    del prospects_df['Ref']
    del prospects_df['Prospect ID']
    del prospects_df['Apps']
    #del prospects_df['Furthest App']

    prospects_df.to_csv('prospects.csv')

    # 1: Pie chart of Entry Term Match column
    # Answers the question "Do people apply for the semester they initially inquire about?"
    
    # pie = prospects_df.plot.pie(y='Entry Term Match', figsize=(5,5))
    fig1 = prospects_df['Entry Term Match'].value_counts().plot(kind='pie').get_figure()
    fig1.savefig('entry_match.png')
    plt.clf()
    # 2: Pie chart of Program Match column
    # Answers the question "Do people apply for the program they initially inquire about?"
    fig2= prospects_df['Program Match'].value_counts().plot(kind='pie').get_figure()
    fig2.savefig('program_match.png')
    plt.clf()
    # 3: Count of prospects by Prospect Program
    prospect_program = pd.pivot_table(prospects_df, index='Program', columns='Furthest App Status', values= 'Name', aggfunc='count')
    # 4: Pivot table of Application Program converted into Prospect Program (drop if no match in programs.csv), columns: Furthest App Status value (except for Prospect).
    
    # 5: Combine 3 and 4 into one pivot table with program as rows, (Prospect count & Furthest App Status values) as columns.
    prospect_program.to_excel('report_funnel.xlsx', sheet_name='Prospects-Program Info', engine='xlsxwriter')
    

if __name__ == '__main__':
    # Parse CLI arguments.
    ARGS = arguments()

    # Call main function.
    main(ARGS.Applications, ARGS.Prospects)
