"""
File: example_models.py
Author: Aidan McEnaney
Date: 2023-08-11

Description: Python file for examples in basic functionality of the SentinelHub API with the project.

Contents:
    - basic_download_single: Example function for how to download a singular band of data.
    - basic_download_multi: Example function for how to download multiple bands of data.
    - multiple_locations: Example function for how to download from multiple locations in one function.

Notes:
    - This code is distributed under the MIT License. See LICENSE.txt for more details.
"""

# Standard library imports
import os

# Local module imports
import local_sentinelhub.sentinelhub_manage_functions as shm
import utils.misc_functions as mf
import local_sentinelhub.requestFunctions as rf
import utils.polymer_functions as pf

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