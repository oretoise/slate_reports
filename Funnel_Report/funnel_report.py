"""
    File: funnel_report.py
"""

import argparse
import pandas as pd
import numpy as np


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

        # Get applications for the prospect.
        relevant_apps = apps[apps['Ref'].isin(app_refs)]
        relevant_apps = relevant_apps[pd.notna(relevant_apps['Application Status'])]

        if relevant_apps.empty:
            return
        else:
            
            # Sort the DataFrame using status_ranking as a key.
            relevant_apps = relevant_apps.sort_values(by='Application Status', key=lambda x: x.apply(lambda y: status_ranking[str(y)]), ascending=False).reset_index()

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

def sep_prog(df, programs):
    tmp = []
    for index, row in df.iterrows():
        if ';' in str(row.Program):
            split = row.Program.split(';')
            if str(row['Furthest App Status']) == 'Prospect':
                for i in range(len(split)):
                    # Make a deep copy of the row.
                    row_copy = row.copy(deep=True)

                    # Set the program.
                    row_copy.Program = split[i]
                    row_copy['Prospect ID'] = row_copy['Prospect ID'] + "-" + str(i)

                    # Append modified copy to tmp.  
                    tmp.append(row_copy)
            else:
                row['App Program'] = programs[programs.app_program == row['App Program']].prospect_program
                row.Program = row['App Program'].values[0]

                tmp.append(row)
            df.drop(labels=index, axis=0, inplace=True)
    
    tmp = pd.DataFrame(tmp, columns=df.columns)
    df = df.append(tmp, ignore_index=True)
    return df

def college_col(x,college_df):
    try:
        if pd.notna(x['Program']) & (not college_df[college_df.prospect_program == x['Program']].empty): 
                y = str(college_df[college_df.prospect_program == str(x['Program'])].college.values[0])
                return y
        else:
            return None
    except:
        print(college_df[college_df.prospect_program == x['Program']]['college'])
        print(x)
        quit()


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

    # Determine outcomes for each application.
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
    prospects_df['Entry Term Match'] = np.where((pd.notna(prospects_df['Term'])) & (pd.notna(prospects_df['App Entry Term'])), prospects_df['Entry Term Match'], None)
    




    # Count prospects, application steps and outcomes by program.
    try:
        programs_df = pd.read_csv('programs.csv')
    except FileNotFoundError:
        print("Cannot find programs.csv. Is it in the same folder as this script?")
        raise SystemExit

    # Compare prospect program and furtherest application program to see if they match or not
    prospects_df['Program Match'] = prospects_df.apply(lambda x: program_match(x, programs_df), axis=1)

    # For prospects with multiple programs, keep either further app, or if prospect, split into multiple records (one for each program) as prospects for each program.
    prospects_df = sep_prog(prospects_df, programs_df)





    # Add college column based on primary program.
    college_df = pd.read_csv("colleges.csv")
    
    prospects_df['College'] = prospects_df.apply(lambda x: college_col(x,college_df), axis=1)
    



    # Data Cleanup Section
    del prospects_df['Apps']
    
    # Pivot tables for Application status by Program and college
    prospect_program = pd.pivot_table(prospects_df, index='Program', columns='Furthest App Status', values='Prospect ID', aggfunc='count')
    college_pivot = pd.pivot_table(prospects_df, index='College', columns='Furthest App Status', values='Prospect ID', aggfunc='count')
    
    prospect_program = prospect_program.fillna(0)
    college_pivot = college_pivot.fillna(0)

    # Combine Cancelled and GR Cancelled into one column.
    prospect_program['Cancelled'] = prospect_program['Cancelled'] + prospect_program['GR Cancelled']
    college_pivot['Cancelled'] = college_pivot['Cancelled'] + college_pivot['GR Cancelled']
    
    del prospect_program['GR Cancelled']
    del college_pivot['GR Cancelled']
    
    # Combine All GR Rejects and Reject
    prospect_program['Reject'] = prospect_program['Reject'] + prospect_program['GR Reject - Academic Deficiency'] + prospect_program['GR Reject - Other']
    college_pivot['Reject'] = college_pivot['Reject'] + college_pivot['GR Reject - Academic Deficiency'] + college_pivot['GR Reject - Other']

    del prospect_program['GR Reject - Academic Deficiency']
    del prospect_program['GR Reject - Other']
    del college_pivot['GR Reject - Academic Deficiency']
    del college_pivot['GR Reject - Other']

    # Reorder into chronological steps.
    column_order = ['Prospect', 'Awaiting Submission', 'Awaiting Payment', 'Awaiting Materials', 'Awaiting Conduct', 'Awaiting Decision', 'Awaiting Confirmation', 
    'Reject','Admit','Decided', 'Cancelled']

    prospect_program = prospect_program.reindex(column_order, axis=1)
    college_pivot = college_pivot.reindex(column_order, axis=1)

    # Export Pivot tables to excel
    with pd.ExcelWriter('report_funnel.xlsx') as writer:
        prospect_program.to_excel(writer, sheet_name='Prospects-Program Info')
        college_pivot.to_excel(writer, sheet_name='Prospects-College Info')

    

if __name__ == '__main__':
    # Parse CLI arguments.
    ARGS = arguments()

    # Call main function.
    main(ARGS.Applications, ARGS.Prospects)
