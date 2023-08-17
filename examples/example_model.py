"""
File: example_model.py
Author: Aidan McEnaney
Date: 2023-08-11

Description: Python file for examples in basic functionality of the SentinelHub API with the project.

Contents:
    - download_and_apply_model: Example function for calling linear model.

Notes:
    - This code is distributed under the MIT License. See LICENSE.txt for more details.
"""

# Standard library imports
import os
from datetime import datetime

# Local module imports
import utils.misc_functions as mf
import local_sentinelsat.request_functions as rf
import utils.model_application_functions as maf
import models.model_functions as mmf
from config import *

def download_and_apply_model():
    """
    Example of applying a parameter model to a snapshat from the sentinelsat API.
    This code to download the data is from 'example_sentinelsat.py'.
    """

    # Settings
    coordinates = (-69.9040, 43.8586, -69.8987, 43.8651)
    start_year, end_year = 2023, 2023
    start_month, end_month = 2, 7
    start_day, end_day = 1, 30
    n_chunks = 3

    project_name = 'example_model'
    npy_save_to = project_name + '_' + 'poly_files'

    # Date calculation
    start = datetime(start_year, start_month, start_day)
    end = datetime(end_year, end_month, end_day)
    date_tuples = mf.get_timeslots(start, end, n_chunks)

    # File path
    # THIS PATH MUST BE DEEPER THAN THE POLYMER DIRECTORY
    file_paths_dict = {
        'poly_dir': os.path.join(polymer_path, 'chlorPoly', project_name) + '/'
    }

    # /Users/aidan/Documents/secondGit/copy_prior_branch_OceanSatelliteImages/polymer-v4.16.1/chlorPoly/MaxFarm
    # MaxFarm_poly_files

    maf.model_routine_space_eff(coordinates, date_tuples, project_name, mmf.chlor,
                                file_paths_dict['poly_dir'], request_function=rf.get_olci_singular,
                                npy_save_to=npy_save_to)

if __name__ == "__main__":
    download_and_apply_model()