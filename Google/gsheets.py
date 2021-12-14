import pygsheets


def authorize():
    ''' Authorize as service account and return a client instance. '''

    # Initialize Google Sheets Connector.
    return pygsheets.authorize(service_account_file='Google\credentials.json')


def set_dataframe(client, df, worksheet):
    ''' Set worksheet to contents of df using client. '''

    # Get GSheets document using client.
    gdoc = client.open("Jordan's File")
    try:
        # Get specified worksheet.
        sheet = gdoc.worksheet('title', worksheet)
       
    except pygsheets.exceptions.WorksheetNotFound:
        # Create new worksheet and then get specified worksheet
        gdoc.add_worksheet(worksheet)
        sheet = gdoc.worksheet('title', worksheet)

    # Set the sheet contents to the provided dataframe.
    sheet.set_dataframe(df,(1,1), copy_index=True)
    # Sync it.
    sheet.sync()


def get_sheet_as_dataframe(client, worksheet):
    ''' Get worksheet contents as dataframe. '''

    # Get GSheets document using client.
    gdoc = client.open("Jordan's File")

    # Get specified worksheet.
    sheet = gdoc.worksheet('title', worksheet)

    return sheet.get_as_df()