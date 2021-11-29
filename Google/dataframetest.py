import pygsheets
import pandas as pd

def main():

    # Initialize Google Sheets Connector.
    gc = pygsheets.authorize(service_account_file='credentials.json')

    # Create a new DataFrame.
    df = pd.DataFrame()

    # Add the name column.
    df['name'] = ['John', 'Steve', 'Sarah']

    # Add the score column.
    df['score'] = [29, 50, 73]

    for id in gc.spreadsheet_ids():

        # Display spreadsheet ID.
        print("Opening Spreadsheet with ID", id)

        # Open the spreadsheet.
        sh = gc.open_by_key(id)

        # Grab the first worksheet.
        wks = sh[0]

        # Set the worksheet contents to the DataFrame.
        wks.set_dataframe(df,(1,1))

        # Share it with Jordan.
        #sh.share("jordan.d.scruggs@gmail.com", role='writer')

    print(gc.spreadsheet_ids())

if __name__ == "__main__":
    main()