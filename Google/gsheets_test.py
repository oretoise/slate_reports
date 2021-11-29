import gsheets
import os
import pandas as pd
import random


def main():
    """ Create a test DataFrame and set it. """

    # Create a client instance.
    client = gsheets.authorize()

    print("Filename:", os.path.basename(__file__))
    print("Authorized.")

    # Create a sample DataFrame.
    df = pd.DataFrame()

    # Add the name column.
    df['name'] = ['John', 'Steve', 'Sarah']

    # Add the score column.
    df['score'] = random.sample(range(0,100),3)

    print("Made sample dataframe:")
    print(df)

    # Open "Test" worksheet.
    gsheets.set_dataframe(client, df, "Test")

    print("Pushed to Google Sheet")

    print("Requesting worksheet as dataframe...")

    # Request what we pushed back as a second DataFrame.
    df2 = gsheets.get_sheet_as_dataframe(client, "Test")

    print("Got dataframe:", df2)
    print("Checking for equality...")
    #pd.testing.assert_frame_equal(df, df2)

if __name__ == "__main__":
    main()