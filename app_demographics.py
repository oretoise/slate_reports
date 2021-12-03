"""
    File: app_demographics.py
"""

import pandas as pd
import numpy as np
import Google.gsheets as gsheets
import slate_sftp

def main():
    """ Clean up application data and push to Google Sheets """

    # Pull latest application export into Pandas DataFrame.
    apps_df, prospects_df = slate_sftp.pull_latest()

    # Combine Race and Hispanic columns.
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
    main()