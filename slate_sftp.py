from base64 import decodebytes
from datetime import datetime
import pandas as pd
import paramiko
import re


def find_latest_files(file_list, type):
    # Get current date.
    dt = datetime.now()

    # Convert to MMDDYYYY format string.
    today_str = dt.strftime('%m%d%Y')

    # Generate search pattern.
    pattern = "^" + type + today_str + ".*"

    # Build regex.
    regx = re.compile(pattern)

    # Search for a match.
    matches = list(filter(regx.match, file_list))

    # Return a match if it exists, otherwise exit.
    if not matches:
        print("No matches found. Quitting...")
        exit()
    else:
        return matches[0]


def pull_latest():
    # Create a Slate SFTP instance.
    sftp = slate_sftp()
    
    # Navigate to /outgoing/distance_exports.
    sftp.chdir('outgoing/distance_exports')

    # Grab file listing.
    files = sftp.listdir()

    # Grab latest application export.
    latest_apps = find_latest_files(files, "applicants_funnel_report_")
    latest_prospects = find_latest_files(files, "prospects_funnel_report_")

    # https://stackoverflow.com/questions/58433996/reading-file-opened-with-python-paramiko-sftpclient-open-method-is-slow

    def pull_into_dataframe(filename):
        file_object = sftp.open(filename, bufsize=32768)
        file_object.prefetch()
        return pd.read_csv(file_object)

    return pull_into_dataframe(latest_apps), pull_into_dataframe(latest_prospects)


def slate_sftp():
    # Create a Paramiko SSH Client instance.
    ssh = paramiko.SSHClient()

    # SSH/SFTP Connection Info
    server = 'ft.technolutions.net'
    port = 22
    user = 'js2506=goto.msstate.edu'
    host_key = b"""AAAAB3NzaC1yc2EAAAADAQABAAABAQDV4xfHn4JFdttLAbX4fffewjouWNuFscZ4Z/b2UgRTFPAyBLcLOacHzRhm6F7AoVeQL/otGJfhT16zQ8nBlb+itRYk8YlJuTi69xTXlLiDKl3CAcNzutiEWw+gRKvFKgpneJuPEfKfgtF6iO8hfnfbcuA8k+cuUIQzWUqhITImK/+SG/aQg9mUgDMDD44uOiFII5hM6fGpygsLIhQlgjzTwF20H4t9OG1LZfE4vJ7ZaWoTRFomf3JGLSGyGFeZ571dzjbA0rdkCd1JO9F+WBUlRGcVbKfrwCWT5lW8djS2Izme/WNg9W7GTIRThbSZP0xVOs3+jr0MuAezEluwcO+R"""

    # Convert host_key into an RSAKey object.
    key = paramiko.RSAKey(data=decodebytes(host_key))

    # Add the RSAKey object to the list of known hosts rather than auto-accepting.
    ssh.get_host_keys().add(server, 'ssh-rsa', key) 

    # Make the connection using the private key file.
    ssh.connect(server, port, user, key_filename='id_rsa')

    # Open the SFTP instance.
    return ssh.open_sftp()


def main():
    """ Pull latest exports and display them. """

    # Pull the latest exports.
    apps_df, prospects_df = pull_latest()

    # Display them.
    print(apps_df.head())
    print(prospects_df.head())


if __name__ == "__main__":
    main()