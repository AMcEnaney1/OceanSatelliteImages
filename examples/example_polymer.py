"""
File: example_polymer.py
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
import utils.polymer_functions as pf
from config import *

def download_and_apply():
    """
    Example of applying POLYMER to a snapshot downloaded using the sentinelsat API.
    This code to download the data is from 'example_sentinelsat.py'.
    """

    coordinates = (-69.9040, 43.8586, -69.8987, 43.8651)

    # File path
    file_paths_dict = {
        'download_dir': 'out/'
    }
    mf.make_absolute_paths_dict(file_paths_dict)

    date_tuples = [('2023-03-01', '2023-03-14')]

    shm.sentinelsat_routine(
        coordinates, date_tuples, file_paths_dict['download_dir'], request_function=rf.get_olci_singular
    )

    filevals = mf.get_surface_level_folders(file_paths_dict['download_dir'])  # Gets a list of the downloaded folder(s)
    filevals = [os.path.join(file_paths_dict['download_dir'], file_path) for file_path in filevals]

    folder = mf.most_recent_folder(filevals) # Getting the newest folder, this should be the one we just downloaded

    pf.call_polymer(folder) # Now we call the polymer script


def download_and_apply_bulk():
    """
    Example of applying POLYMER to multiple snapshopts downloaded using the sentinelsat API.
    This code to download the data is from 'example_sentinelsat.py'.
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

    filevals = mf.get_surface_level_folders(file_paths_dict['download_dir'])  # Gets a list of the downloaded folder(s)
    filevals = [os.path.join(file_paths_dict['download_dir'], file_path) for file_path in filevals]

    pf.call_polymer(filevals)  # Now we call the polymer script


if __name__ == "__main__":
    download_and_apply()