import pandas as pd

def undergrad():

    # Pandas options for debugging.
    pd.set_option('display.width', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)

    # Go through each bin, each application must have:
    # - all bins marked "required"
    # - one of each bin in a set, per set group (i.e.: one from set 1, one from set 2, ...)
    # Additionally, for each bin, the next one in the linked list must be in the list of its next bins.

    undergrad_bins = [
        {
            "name": "Awaiting Submission",
            "category": "Awaiting Review",
            "next": [
                "Conduct Committee Review",
                "Awaiting Payment"
                ],
            "order": 10,
            "type": "required"
        },
        {
            "name": "Conduct Committee Review",
            "category": "Awaiting Review",
            "next": ["Conduct Committee Approved"],
            "order": 12,
            "type": "optional"
        },
        {
            "name": "Conduct Committee Approved",
            "category": "Awaiting Review",
            "next": ["Awaiting Payment"],
            "order": 13,
            "type": "optional"
        },
        {
            "name": "Awaiting Payment",
            "category": "Awaiting Review",
            "next": ["Awaiting Materials"],
            "order": 14,
            "type": "required"
        },
        {
            "name": "Awaiting Materials",
            "category": "Awaiting Review",
            "next": [
                "Not a New Admission",
                "Ready to Review-Freshmen",
                "Ready to Review-Transfers"
            ],
            "order": 16,
            "type": "required"
        },
        {
            "name": "Not a New Admission",
            "category": "Awaiting Review",
            "order": 19,
            "type": "optional"
        },{
            "name": "Ready to Review-Freshmen",
            "category": "Review",
            "order": 20,
            "set": "Ready to Review",
            "type": "set"
        },{
            "name": "Ready to Review-Transfers",
            "category": "Review",
            "order": 25,
            "set": "Ready to Review",
            "type": "set"
        }
    ]

    print("Loading Undergraduate bins into Dataframe...")
    undergrad_bin_df = pd.DataFrame(undergrad_bins)
    print(undergrad_bin_df)
    return undergrad_bin_df


if __name__ == "__main__":
    undergrad()