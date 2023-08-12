"""
File: example_sentinelhub.py
Author: Aidan McEnaney
Date: 2023-08-11

Description: Python file for examples in basic functionality of the SentinelHub API with the project.

Contents:
    - basic_download: Example function for how to download a singular band of data.

Notes:
    - This code is distributed under the MIT License. See LICENSE.txt for more details.
"""

# Standard library imports
from datetime import datetime

# Local module imports
import local_sentinelhub.sentinelhub_manage_functions as shm
import utils.misc_functions as mf
import local_sentinelhub.requestFunctions as rf

def basic_download():
    # Settings
    resolution = 30
    coordinates = (-69.9040, 43.8586, -69.8987, 43.8651)
    projectName = 'MaxFarm'
    start_year, end_year = 2022, 2023
    start_month, end_month = 4, 4
    start_day, end_day = 1, 30
    n_chunks = 15
    createImages = True

    # File paths
    file_paths_dict = {
        'sat_image_save_path': 'out/satData/images/',
        'operations_save_path': 'out/satData/logs/MaxFarm_oper.txt',
        'figure_save_path': 'out/figures/',
        'csvpath_thermal': 'out/data/MaxFarm_compDataMaxFarm_Thermal.csv'
    }
    mf.make_absolute_paths_dict(file_paths_dict)

    # Date calculation
    start = datetime(start_year, start_month, start_day)
    end = datetime(end_year, end_month, end_day)
    date_tuples = mf.get_timeslots(start, end, n_chunks)

    # SentinelHub processing
    thermalPreface = 'Thermal'
    operext = '.npy'

    shm.sentinelhub_main(
        resolution, date_tuples, file_paths_dict['sat_image_save_path'],
        file_paths_dict['operations_save_path'], thermalPreface, coordinates,
        file_paths_dict['figure_save_path'], file_paths_dict['csvpath_thermal'],
        operext, projectName, request_function=rf.get_thermal_request,
        createImages=createImages
    )

if __name__ == "__main__":
    basic_download()