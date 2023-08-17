"""
File: example_for_script.py
Author: Aidan McEnaney
Date: 2023-08-17

Description: This is an example python file to be run by a script, such as 'scripts/run.sh'.

Contents:
    - main: Function containing calls to functions in other example files, to be called by a script, or in python.

Notes:
    - This code is distributed under the MIT License. See LICENSE.txt for more details.
"""

# Local module imports
import examples.example_plotting as example_plotting
import examples.example_sentinelhub as example_sentinelhub

def main():
    """
    Function that calls functions from other example files
    Intended to be called from 'scripts/run.sh' to demonstrate executing code from this project in bash
    """

    example_plotting.temperature_plots() # Downloads temperature data from the SentinelHub API then plots it
    example_sentinelhub.basic_download_multi() # Downloads multiple bands of data from the SentinelHub API


if __name__ == "__main__":
    main()