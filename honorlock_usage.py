import argparse
import Google.gsheets as gsheets
import pandas as pd
import pyautogui
import pyperclip

pyautogui.PAUSE = 3

def arguments():
    """ Parse arguments. """
    description = "Create report of what bins applications spend the most time in based on bin history."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-i", "--Input", action="store",
                        help="Honorlock Usage File (CSV)", required=True)
    parser.add_argument("-l", "--Lookup", action="store_true", default=False,
                        help="Directory lookup", required=False)
    return parser.parse_args()


def campus(crn):
    """ Figure out campus based on course number. """

    if crn.startswith('-'):
        if crn.startswith('-XL-'):
            return "Crosslisted"
        elif crn.startswith('-EXT-'):
            return "External"
    else:
        if '-' in crn:
            crn_split = crn.split('-')

            if len(crn_split) > 2:
                section = crn_split[2]

                if section.startswith('H') or section.startswith('E') or section.startswith('C'):
                    section = section[1:]
                
                if len(section) == 2:
                    return "Campus 1"
                else:
                    return "Campus " + section[0]
            else:
                return "Other"
        else:
            return "Other"


def get_dept(email):

    if "msstate.edu" in email:

        # Press the end key.
        pyautogui.press('end')

        # Click on email field
        pyautogui.click(1468, 956)

        # Typewrite email
        pyautogui.hotkey('ctrl', 'a')
        pyautogui.typewrite(email)

        # Click search
        pyautogui.click(1774, 1124)

        # Triple click department
        pyautogui.click(723, 1220, clicks=3)

        # Copy to clipboard
        pyautogui.hotkey('ctrl', 'c')

        # Return department name.
        dept = pyperclip.paste()
        return dept
    else:
        return


def pull_dept(professors, x):
    #print(x)
    return professors[professors['instructor_name'] == x]['department'].values[0]

def main(honorlock_csv, lookup):
    honorlock = pd.read_csv(honorlock_csv)

    professors = pd.read_csv('./sheets/prof_dept.csv')

    # Determine campus.
    honorlock['campus'] = honorlock['CRN'].apply(campus)

    # Sort professors based on session_count.
    sorted_profs = honorlock.groupby(['instructor_name', 'instructor_email', 'campus']).apply(lambda x: x.groupby(['campus', 'CRN']).session_count.first().sum()).reset_index(name="total").sort_values(by='total', ascending=False)

    # sorted_profs['Campus'] = sorted_profs['CRN'].apply(campus)
    sorted_profs['Department'] = sorted_profs['instructor_name'].apply(lambda x: pull_dept(professors, x))

    if lookup:

        # Hit windows key + 1
        pyautogui.hotkey('win', '1')

        # For each professor, grab their department info from Banner using PyAutoGUI, ignoring any non-msstate.edu email addresses.
        sorted_profs['Department'] = sorted_profs['instructor_email'].apply(get_dept)
    
    # Display results.
    print(sorted_profs.head())

    # Output to CSV file.
    sorted_profs.to_csv('sorted_prof.csv', index=False)

    # Push to Gsheets
    client = gsheets.authorize()
    gsheets.set_dataframe(client, sorted_profs, "Honorlock")


if __name__ == '__main__':
    # Parse CLI arguments.
    ARGS = arguments()

    # Call main function.
    main(ARGS.Input, ARGS.Lookup)
