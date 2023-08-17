"""
File: example_sentinelhub.py
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
from datetime import datetime

# Local module imports
import local_sentinelhub.sentinelhub_manage_functions as shm
import utils.misc_functions as mf
import local_sentinelhub.requestFunctions as rf

def basic_download_single():
    """
    Example of how to download a single band of data from a satellite using the SentinelHub API.
    """

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


def basic_download_multi():
    """
    Example of how to download multiple bands of data from a satellite using the SentinelHub API.
    In order to do this you must make the csvpath into a list with the length equal to the bands of the request.
    The preface must be made into a list as well, one with the same length.
    """

    # Settings
    resolution = 20
    coordinates = (-69.9040, 43.8586, -69.8987, 43.8651)
    projectName = 'MaxFarm'
    start_year, end_year = 2022, 2023
    start_month, end_month = 4, 4
    start_day, end_day = 1, 30
    n_chunks = 15
    createImages = True

    preface = []

    # File paths
    file_paths_dict = {
        'sat_image_save_path': 'out/satData/images/',
        'operations_save_path': 'out/satData/logs/MaxFarm_oper.txt',
        'figure_save_path': 'out/figures/',
        'csvpath': []
    }

    for j in range(12): # We have 12 bands in the request
        file_paths_dict['csvpath'].append('out/data/MaxFarm_compDataMaxFarm_alls2l2a' + '_' + str(j) +  '.csv')
        preface.append('Alls2l2a' + str(j))

    mf.make_absolute_paths_dict(file_paths_dict)

    # Date calculation
    start = datetime(start_year, start_month, start_day)
    end = datetime(end_year, end_month, end_day)
    date_tuples = mf.get_timeslots(start, end, n_chunks)

    operext = '.npy'

    shm.sentinelhub_main(
        resolution, date_tuples, file_paths_dict['sat_image_save_path'],
        file_paths_dict['operations_save_path'], preface, coordinates,
        file_paths_dict['figure_save_path'], file_paths_dict['csvpath'],
        operext, projectName, request_function=rf.get_all_s2l2a_request,
        createImages=createImages
    )


def multiple_locations():
    """
    Example of how to download a single band of data from a satellite using the SentinelHub API.
    """

    # Settings
    projectName = ['firstLocation', 'secondLocation']
    coordinates = [(-69.9040, 43.8586, -69.8987, 43.8651), (-69.9040, 43.8586, -69.8987, 43.8751)]
    prefaces = ['Thermal', []]
    start_year, end_year = 2022, 2023
    start_month, end_month = 4, 4
    start_day, end_day = 1, 30
    n_chunks = 30
    createImages = True
    operext = '.npy'

    # File paths
    file_paths_dicts = [{
        'sat_image_save_path': 'out/satData/images/',
        'operations_save_path': 'out/satData/logs/MaxFarm_oper.txt',
        'figure_save_path': 'out/figures/',
        'csvpath': 'out/data/MaxFarm_compDataMaxFarm_Thermal.csv'
        },
        {
        'sat_image_save_path': 'out/satData/images/',
        'operations_save_path': 'out/satData/logs/MaxFarm_oper.txt',
        'figure_save_path': 'out/figures/',
        'csvpath': []
        }
    ]

    for j in range(5): # We have 5 bands in the request
        file_paths_dicts[1]['csvpath'].append('out/data/MaxFarm_compDataMaxFarm_ChlorAlgo' + '_' + str(j) + '.csv')
        prefaces[1].append('chlorAlgo' + str(j))

    # Date calculation
    start = datetime(start_year, start_month, start_day)
    end = datetime(end_year, end_month, end_day)
    date_tuples = mf.get_timeslots(start, end, n_chunks)

    for i in range(len(projectName)):

        #file_paths_dict = file_paths_dicts[i]
        #mf.make_absolute_paths_dict(file_paths_dict)
        #print(file_paths_dict)

        mf.make_absolute_paths_list(file_paths_dicts)

        resolution = 100
        shm.sentinelhub_main(
            resolution, date_tuples, file_paths_dicts[0]['sat_image_save_path'],
            file_paths_dicts[0]['operations_save_path'], prefaces[0], coordinates[i],
            file_paths_dicts[0]['figure_save_path'], file_paths_dicts[0]['csvpath'],
            operext, projectName[i], request_function=rf.get_sediment_request,
            createImages=createImages
        )

        resolution = 100
        shm.sentinelhub_main(
            resolution, date_tuples, file_paths_dicts[1]['sat_image_save_path'],
            file_paths_dicts[1]['operations_save_path'], prefaces[1], coordinates[i],
            file_paths_dicts[1]['figure_save_path'], file_paths_dicts[1]['csvpath'],
            operext, projectName[i], request_function=rf.get_chlor_algo_request,
            createImages=createImages
        )


if __name__ == "__main__":
    basic_download_single()
    basic_download_multi()
    multiple_locations()