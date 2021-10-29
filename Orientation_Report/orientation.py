"""
File: ytd_report.py
"""

import argparse
import numpy as np
import pandas as pd

import time
import datetime

def arguments():
    """ Parse CLI arguments. """
    description = "Create a year-to-date report of application data."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("-i", "--Input", action="store", help="Application Data File", required=True)
    parser.add_argument("-d", "--Date", action="store", help="Cutoff date, in YYYY-MM-DD format", required=True)
    return parser.parse_args()

def main(input, date):
    pass


if __name__ == "__main__":
    # Parse CLI arguments.
    ARGS = arguments()

    # Call main function.
    main(ARGS.Input, ARGS.Date)