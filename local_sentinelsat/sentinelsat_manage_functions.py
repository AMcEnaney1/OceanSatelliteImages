"""
File: sentinelsat_manage_functions.py
Author: Aidan McEnaney
Date: 2023-08-11

Description: This module contains the functions that manage the processes for the SentinelHub API.

Contents:
    - sentinelsat_routine: Function to handle the core routine for Sentinelsat API.

Notes:
    - This code is distributed under the MIT License. See LICENSE.txt for more details.
"""

# Standard library imports
import os

# Third-party library imports
from sentinelhub import (
    CRS,
    BBox,
    SentinelHubDownloadClient,
    bbox_to_dimensions,
)
import numpy as np

# Local module imports
from conf.config import *
import utils.io_functions as io
import utils.file_conversion_functions as fcf
import utils.plot_functions as pf
import utils.save_file_functions as sff
import utils.array_operations as ao
import utils.misc_functions as mf


def sentinelsat_routine(bbox,  # Bounding box coordinates [min_lon, min_lat, max_lon, max_lat].
                        date_tuples,  # List of tuples, each containing start and end dates for data retrieval.
                        download_directory,  # Directory where downloaded zip files will be saved.
                        request_function  # Function used for making API requests and downloading zips.
                        ):
    """
    Routine for using SentinelSat API to download and process Sentinel data.

    Args:
        bbox (tuple): Bounding box coordinates [min_lon, min_lat, max_lon, max_lat].
        date_tuples (list): A list of tuples, each containing start and end dates for data retrieval.
        download_directory (str): Directory where downloaded zip files will be saved.
        request_function (function): Function used for making API requests and downloading zip files.

    Returns:
        None
    """

    if (download_directory.split('/')[0] == ''):
        io.create_batch_folders(download_directory)
    else:
        tmp = download_directory.split('/')
        tmp = ao.move_elements_down_one(tmp)

        for i in range(len(tmp) - 1): # Creates folders
            io.create_folder(tmp[i], tmp[i + 1])

    request_function(date_tuples, bbox, download_directory)  # Downloads zips

    io.unzip_all_zip_files(download_directory)  # Unzips all the folders, so we have folders of .nc files, also deletes zips