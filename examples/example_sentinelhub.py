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
import os

# Local module imports
import local_sentinelhub.sentinelhub_manage_functions as shm
import utils.misc_functions as mf
import local_sentinelhub.requestFunctions as rf

def basic_download():

    # Setting variables
    resolution = 30  # Resolution for thermal images

    coordinates = (-69.9040, 43.8586, -69.8987, 43.8651)  # These will be turned into bounding boxes

    projectName = 'MaxFarm'  # These will be prefixes in the relevant files

    # These variables set the start and end dates for the data collection
    start_year = 2022
    end_year = 2023
    start_month = 4
    end_month = 4
    start_day = 1
    end_day = 30

    n_chunks = 15 # This is 1 more than the amount of data points you want to collect

    # Setting up start and end date as well as the amount of snapshots
    start = datetime(start_year, start_month, start_day)
    end = datetime(end_year, end_month, end_day)
    date_tuples = mf.get_timeslots(start, end, n_chunks)

    createImages = False  # If True, .npy and .png images will be created when making calls with SentinelHub

    # This the name of the folder in which will serve as the root for downloaded data from SentinelHub
    outputs_folder = 'out'
    image_folder_name = 'images'
    sat_image_folder_name = 'satData'
    sat_image_save_path = os.path.join(outputs_folder, sat_image_folder_name, image_folder_name, '')

    operations_txt_suffix = '_oper'
    operations_txt_filename = projectName + operations_txt_suffix + '.txt'
    sat_image_folder_name = 'satData'
    log_file_folder_name = sat_image_folder_name
    log_folder_name = 'logs'
    operations_save_path = os.path.join(outputs_folder, log_file_folder_name, log_folder_name, '') + operations_txt_filename
    thermalPreface = 'Thermal'
    figure_path_folder_name = 'figures'
    figure_save_path = os.path.join(outputs_folder, figure_path_folder_name, '')

    csv_path_folder_name = 'data'
    csv_path_folder_suffix = '_compData'
    csv_path_thermal_suffix = '_Thermal'
    csvpath_base = os.path.join(outputs_folder, csv_path_folder_name, '') + projectName + csv_path_folder_suffix
    csvpath_thermal = csvpath_base + projectName + csv_path_thermal_suffix + '.csv'

    operext = '.npy'

    shm.sentinelhub_main(resolution, date_tuples, sat_image_save_path, operations_save_path, thermalPreface,
                         coordinates, figure_save_path, csvpath_thermal, operext, projectName,
                         request_function=rf.get_thermal_request, createImages=createImages)

if __name__ == "__main__":
    basic_download()