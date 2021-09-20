import pandas as pd

def undergrad(debug=False):
    """ Define the Undergraduate bin DataFrame and return it. """

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
            "next": [],
            "type": "optional"
        },{
            "name": "Ready to Review-Freshmen",
            "category": "Review",
            "order": 20,
            "next": [
                "Awaiting Additional Materials",
                "Awaiting Materials"
            ],
            "set": "Ready to Review",
            "type": "set"
        },{
            "name": "Ready to Review-Transfers",
            "category": "Review",
            "order": 25,
            "next": [
                "Awaiting Additional Materials",
                "Awaiting Materials"
            ],
            "set": "Ready to Review",
            "type": "set"
        },{
            "name": "Awaiting Additional Materials",
            "category": "Review",
            "order": 28,
            "next": [
                "Ready to Review-Freshmen",
                "Ready to Review-Transfers"
            ],
            "type": "optional"
        },{
            "name": "ARNR Committee",
            "category": "Committee",
            "order": 30,
            "next": [],
            "type": "optional"
        },{
            "name": "ARNR Approved",
            "category": "Committee",
            "order": 32,
            "next": [],
            "type": "optional"
        },{
            "name": "ARNR Awaiting Materials",
            "category": "Committee",
            "order": 33,
            "next": [],
            "type": "optional"
        },{
            "name": "Transfer Reject Committee",
            "category": "Committee",
            "order": 40,
            "next": [],
            "type": "optional"
        },{
            "name": "Refer to Test",
            "category": "Decision",
            "order": 65,
            "next": [],
            "type": "optional"
        },{
            "name": "Ready to Admit",
            "category": "Decision",
            "order": 70,
            "next": [],
            "type": "set",
            "set": "Ready to Decision"
        },{
            "name": "Ready to Admit (Contingent)",
            "category": "Decision",
            "order": 72,
            "next": [],
            "type": "set",
            "set": "Ready to Decision"
        },{
            "name": "Ready to Deny",
            "category": "Decision",
            "order": 72,
            "next": [],
            "type": "set",
            "set": "Ready to Decision"
        },{
            "name": "Conduct Committee Reject",
            "category": "Decision",
            "order": 75,
            "next": [],
            "type": "optional"
        },{
            "name": "Awaiting Release",
            "category": "Post Decision",
            "order": 80,
            "next": [],
            "type": "required"
        },{
            "name": "Released Decision",
            "category": "Post Decision",
            "order": 82,
            "next": [],
            "type": "required"
        }
    ]

    # Print debugging information.
    if debug:
        print("Loading Undergraduate bins into Dataframe...")
    
    # Convert list of dictionaries into a Pandas DataFrame.
    undergrad_bin_df = pd.DataFrame(undergrad_bins)

    # Print the Undergraduate bin DataFrame if we're debugging.
    if debug:
        print(undergrad_bin_df)
    
    # Return the DataFrame.
    return undergrad_bin_df


def graduate(debug=False):
    """ Define the Graduate bin DataFrame and return it. """

    graduate_bins = [
        {
            "name": "Awaiting Submission",
            "category": "Awaiting Review",
            "next": [],
            "order": 10,
            "type": "required"
        },{
            "name": "Awaiting Payment",
            "category": "Awaiting Review",
            "next": [],
            "order": 14,
            "type": "required"
        },{
            "name": "Conduct Committee Review",
            "category": "Awaiting Review",
            "next": [],
            "order": 15,
            "type": "optional"
        },{
            "name": "Conduct Committee Approved",
            "category": "Awaiting Review",
            "next": [],
            "order": 16,
            "type": "optional"
        },{
            "name": "Fee Waiver Review",
            "category": "Awaiting Review",
            "next": [],
            "order": 17,
            "type": "optional"
        },{
            "name": "Awaiting Materials",
            "category": "Awaiting Review",
            "next": [],
            "order": 18,
            "type": "optional"
        },{
            "name": "Admissions Review",
            "category": "Admissions Review",
            "next": [],
            "order": 20,
            "type": "required"
        },{
            "name": "Awaiting Additional Materials",
            "category": "Admissions Review",
            "next": [],
            "order": 30,
            "type": "optional"
        },{
            "name": "Unaccredited",
            "category": "Admissions Review",
            "next": [],
            "order": 33,
            "type": "optional"
        },{
            "name": "Unclassified",
            "category": "Admissions Review",
            "next": [],
            "order": 35,
            "type": "optional"
        },{
            "name": "Departmental Preview",
            "category": "Departmental Review",
            "next": [],
            "order": 39,
            "type": "optional"
        },{
            "name": "Departmental Review",
            "category": "Departmental Review",
            "next": [],
            "order": 40,
            "type": "required"
        },{
            "name": "Departmental Final Review",
            "category": "Departmental Review",
            "next": [],
            "order": 42,
            "type": "required"
        },{
            "name": "College Dean Review",
            "category": "Departmental Review",
            "next": [],
            "order": 45,
            "type": "required"
        },{
            "name": "Dean of Grad School Review",
            "category": "Departmental Review",
            "next": [],
            "order": 46,
            "type": "required"
        },{
            "name": "Grad School Final Review",
            "category": "Grad School Final Review",
            "next": [],
            "order": 75,
            "type": "required"
        },{
            "name": "Security Review",
            "category": "Grad School Final Review",
            "next": [],
            "order": 75,
            "type": "optional"
        },{
            "name": "Ready to Admit",
            "category": "Decision",
            "next": [],
            "order": 80,
            "set": "Decision",
            "type": "set"
        },{
            "name": "Ready to Admit (Contingent)",
            "category": "Decision",
            "next": [],
            "order": 82,
            "set": "Decision",
            "type": "set"
        },{
            "name": "Ready to Admit (Provisional)",
            "category": "Decision",
            "next": [],
            "order": 83,
            "set": "Decision",
            "type": "set"
        },{
            "name": "Ready to Deny",
            "category": "Decision",
            "next": [],
            "order": 85,
            "set": "Decision",
            "type": "set"
        },{
            "name": "Conduct Committee Reject",
            "category": "Decision",
            "next": [],
            "order": 89,
            "type": "optional"
        },{
            "name": "Awaiting Release",
            "category": "Post Decision",
            "next": [],
            "order": 105,
            "type": "required"
        },{
            "name": "Released Decision",
            "category": "Post Decision",
            "next": [],
            "order": 107,
            "type": "required"
        },{
            "name": "Official Await",
            "category": "Post Decision",
            "next": [],
            "order": 110,
            "type": "optional"
        },{
            "name": "Matric",
            "category": "Post Decision",
            "next": [],
            "order": 120,
            "type": "optional"
        }
    ]
    
    # Print debugging information.
    if debug:
        print("Loading Graduate bins into Dataframe...")
    
    # Convert list of dictionaries into a Pandas DataFrame.
    grad_bin_df = pd.DataFrame(graduate_bins)

    # Print the Undergraduate bin DataFrame if we're debugging.
    if debug:
        print(grad_bin_df)
    
    # Return the DataFrame.
    return grad_bin_df
    

def readmit(debug=False):
    """ Define the Readmission bin DataFrame and return it. """
    readmit_bins = [
        {
            "name": "Conduct Committee Review",
            "category": "Conduct",
            "next": [],
            "order": 2,
            "type": "required"
        },{
            "name": "Review (Spring)",
            "category": "Review",
            "next": [],
            "order": 10,
            "set": "Review Semester",
            "type": "set"
        },{
            "name": "Review (Summer and Fall)",
            "category": "Review",
            "next": [],
            "order": 12,
            "set": "Review Semester",
            "type": "set"
        },{
            "name": "Further Review",
            "category": "Review",
            "next": [],
            "order": 15,
            "type": "optional"
        },{
            "name": "Readmit",
            "category": "Decision",
            "next": [],
            "order": 20,
            "set": "Decision",
            "type": "set"
        },{
            "name": "Not a Readmit",
            "category": "Decision",
            "next": [],
            "order": 30,
            "set": "Decision",
            "type": "set"
        },{
            "name": "Conduct Review Reject",
            "category": "Decision",
            "next": [],
            "order": 40,
            "type": "optional"
        }
    ]

    # Print debugging information.
    if debug:
        print("Loading Graduate bins into Dataframe...")
    
    # Convert list of dictionaries into a Pandas DataFrame.
    readmit_bin_df = pd.DataFrame(readmit_bins)

    # Print the Undergraduate bin DataFrame if we're debugging.
    if debug:
        print(readmit_bin_df)
    
    # Return the DataFrame.
    return readmit_bin_df


if __name__ == "__main__":

    # Pandas options for debugging.
    pd.set_option('display.width', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_colwidth', None)

    # Build the Undergraduate bin DataFrame.
    undergrad(debug=True)

    # Build the Graduate bin DataFrame.
    graduate(debug=True)

    # Build the Readmit bin DataFrame.
    readmit(debug=True)