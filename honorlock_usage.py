import argparse
import pandas as pd
import pyautogui
import pyperclip

pyautogui.PAUSE = 3

def arguments():
    """ Parse arguments. """
    description = "Create report of what bins applications spend the most time in based on bin history."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-p", "--Honorlock", action="store",
                        help="Honorlock Usage File (CSV)", required=True)
    return parser.parse_args()


def get_dept(email):

    bad_emails = [
        "katie@poultry.msstate.edu",
        "JLarson@ads.msstate.edu"
    ]

    if "msstate.edu" in email and email not in bad_emails:

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


def main(honorlock_csv):
    honorlock = pd.read_csv(honorlock_csv)

    # Sort professors based on session_count.
    sorted_profs = honorlock.groupby(['instructor_name', 'instructor_email']).apply(lambda x: x.groupby('CRN').session_count.first().sum()).reset_index(name="total").sort_values(by='total', ascending=False)

    # Hit windows key + 1
    pyautogui.hotkey('win', '1')

    # For each professor, grab their department info from Banner using PyAutoGUI, ignoring any non-msstate.edu email addresses.
    sorted_profs['Department'] = sorted_profs['instructor_email'].apply(get_dept)
    print(sorted_profs.head())


if __name__ == '__main__':
    # Parse CLI arguments.
    ARGS = arguments()

    # Call main function.
    main(ARGS.Honorlock)
