"""
File: example_sentinelsat.py
Author: Aidan McEnaney
Date: 2023-08-11

Description: Python file for examples in basic functionality of the Sentinelsat API with the project.

Contents:
    - basic_download_single: Example function for how to download a singular snapshot of data.
    - basic_download_multi: Example function for how to download multiple snapshots of data.

Notes:
    - This code is distributed under the MIT License. See LICENSE.txt for more details.
"""

# Standard library imports
from datetime import datetime
import os

# Local module imports
import local_sentinelsat.sentinelsat_manage_functions as shm
import utils.misc_functions as mf
import local_sentinelsat.request_functions as rf

def basic_download_single():
    """
    Example of how to download a single snapshot given a date range using the sentinelsat API.
    """

    # Settings
    coordinates = (-69.9040, 43.8586, -69.8987, 43.8651)

    # File path
    file_paths_dict = {
        'download_dir': 'out/'
    }
    mf.make_absolute_paths_dict(file_paths_dict)

    date_tuples = [('2023-03-01', '2023-03-25')]

    shm.sentinelsat_routine(
        coordinates, date_tuples, file_paths_dict['download_dir'], request_function=rf.get_olci_singular
    )


def basic_download_multi():
    """
        Example of how to download multiple snapshots of data over a date range using the sentinelsat API.
        """

    # Settings
    coordinates = (-69.9040, 43.8586, -69.8987, 43.8651)
    start_year, end_year = 2022, 2023
    start_month, end_month = 1, 4
    start_day, end_day = 1, 30
    n_chunks = 11

    # File path
    file_paths_dict = {
        'download_dir': 'out/'
    }
    mf.make_absolute_paths_dict(file_paths_dict)

    # Date calculation
    start = datetime(start_year, start_month, start_day)
    end = datetime(end_year, end_month, end_day)
    date_tuples = mf.get_timeslots(start, end, n_chunks)

    shm.sentinelsat_routine(
        coordinates, date_tuples, file_paths_dict['download_dir'], request_function=rf.get_olci
    )


if __name__ == "__main__":
    basic_download_single()
    basic_download_multi()