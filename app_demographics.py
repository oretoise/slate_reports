"""
    File: app_demographics.py
"""

import argparse
import pandas as pd
import numpy as np
import Google.gsheets as gsheets


def arguments():
    """ Parse arguments. """
    description = "Prepare application data export, push to Google Sheets for Demographics dashboard."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-a", "--Applications", action="store",
                        help="Applications File", required=True)
    return parser.parse_args()


def main(apps):
    """ Clean up application data and push to Google Sheets """

    # Load application data into DataFrames.
    apps_df = pd.read_csv(apps)

    apps_df['Race'] = np.where((apps_df['Hispanic'] == 'Yes') & (apps_df['Race'].notnull()), apps_df['Race'] + ", Hispanic", apps_df['Race'])

    # Clean up apps_df by setting "Program" and "Entry Term" columns based on "Round Key".
    apps_df['Program'] = np.where(apps_df["GR Academic Interest (App)"].isnull(), apps_df["UG Academic Interest (App)"], apps_df["GR Academic Interest (App)"])
    apps_df['Entry Term'] = np.where(apps_df["UG Entry Term (App)"].isnull(), apps_df["GR Entry Term (App)"], apps_df["UG Entry Term (App)"])

    # List of columns to remove.
    cols = [
        "GR Academic Interest (App)",
        "UG Academic Interest (App)",
        "GR Entry Term (App)",
        "UG Entry Term (App)",
        "Prospect ID",
        "Created",
        "Decision Confirmed Name",
        "Campus (App)",
        "Round Key",
        "Ready for Release",
    ]

    # Delete unneeded columns.
    for column in cols:
        del apps_df[column]

    # Push to Gsheets
    client = gsheets.authorize()
    gsheets.set_dataframe(client, apps_df, "App-Demographics")


if __name__ == '__main__':
    # Parse CLI arguments.
    ARGS = arguments()

    # Call main function.
    main(ARGS.Applications)