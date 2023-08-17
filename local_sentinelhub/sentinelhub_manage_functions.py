"""
File: sentinelhub_manage_functions.py
Author: Aidan McEnaney
Date: 2023-08-11

Description: This module contains the functions that manage the processes for the SentinelHub API.

Contents:
    - sentinelhub_main: Main function for interacting with the SentinelHub API.
    - sentinelhub_routine: Function to handle the core routine for SentinelHub API.

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

def sentinelhub_main(resolution,  # Spatial resolution for data retrieval.
         date_tuples,  # List of tuples, each containing start and end dates for data retrieval.
         sat_image_save_path,  # Directory where satellite images will be saved.
         operations_save_path,  # Directory where operation log file will be saved.
         preface,  # Prefix or list of prefixes for file names and paths.
         farm_coords_wgs84,  # Bounding box coordinates [min_lon, min_lat, max_lon, max_lat] in WGS84.
         figure_save_path,  # Directory where figures will be saved (if applicable).
         csvpath,  # File path or list of file paths for CSV data.
         operext,  # File extension for operation log and satellite images.
         project_name,  # Name of the project.
         request_function,  # Function used for making API requests.
         createImages=False,  # Optional flag to create images.
         as_nc=False  # Optional flag to save images as NetCDF files.
         ):
    """
    Main function for managing data retrieval, processing, and storage. For the SentinelHub API.

    Args:
        resolution (int): Spatial resolution for data retrieval.
        date_tuples (list): A list of tuples, each containing start and end dates for data retrieval.
        sat_image_save_path (str): Directory where satellite images will be saved.
        operations_save_path (str): Directory where the operation log file will be saved.
        preface (str or list): Prefix or list of prefixes for file names and paths.
        farm_coords_wgs84 (list): Bounding box coordinates [min_lon, min_lat, max_lon, max_lat] in WGS84.
        figure_save_path (str): Directory where figures will be saved (if applicable).
        csvpath (str or list): File path or list of file paths for CSV data.
        operext (str): File extension for operation log and satellite images.
        project_name (str): Name of the project associated with the bbox.
        request_function (function): Function used for making API requests.
        createImages (bool): Flag to create images (default is False).
        as_nc (bool): Flag to save images as NetCDF files (default is False).

    Returns:
        None
    """

    # Setting up resolution and stuff

    farm_bbox = BBox(bbox=farm_coords_wgs84, crs=CRS.WGS84)
    farm_size = bbox_to_dimensions(farm_bbox, resolution=resolution)

    # print(f"Image shape at {resolution} m resolution: {farm_size} pixels") # Troubleshooting code

    # I want to do a check here, so I don't waste api calls on data I already have
    # This will get a list of any expected files that may not be there

    # We also need to create our log file, if one doesn't already exist

    if (not os.path.exists(operations_save_path)): # Operation log file doesn't already exist
        mf.folder_creation_manage(operations_save_path) # Creates folders leading up to file

        io.create_blank_file(operations_save_path) # Create operation log file if it doesn't already exist

    if (not (type(preface) is list)):
        preface = [preface]
        csvpath = [csvpath]

    for i in range(len(preface)):

        # Creating csv
        if (not os.path.exists(csvpath[i])): # Checks if csv already exists
            mf.folder_creation_manage(csvpath[i])  # Creates folders leading up to file

        if (createImages):
            nonexisting = io.check_files_exist(date_tuples, operext, sat_image_save_path, preface[i])
        else:
            nonexisting = io.check_files_exist_in_text_file(date_tuples, operext, operations_save_path, preface[i], project_name)

        if (len(nonexisting) == len(date_tuples)):
            sentinelhub_routine(farm_bbox, farm_size, date_tuples, sat_image_save_path, operations_save_path, preface[i],
                                farm_coords_wgs84, figure_save_path, csvpath[i], operext, project_name,
                                request_function, createImages = createImages, i=i, as_nc = as_nc)
        elif (len(nonexisting) != 0):
            flots = []

            for file_name in nonexisting:
                date_strings = file_name.split("_")[0:2]
                start_date, end_date = date_strings
                flots.append((start_date, end_date))

            sentinelhub_routine(farm_bbox, farm_size, flots, sat_image_save_path, operations_save_path, preface[i],
                                farm_coords_wgs84, figure_save_path, csvpath[i], operext, project_name,
                                request_function, createImages = createImages, i=i, as_nc = as_nc)
        else:
            print("All of these files are already downloaded")


def sentinelhub_routine(farm_bbox,  # Bounding box of the farm area.
            farm_size,  # Size of the farm area.
            date_tuples,  # List of tuples, each containing start and end dates for data retrieval.
            sat_image_save_path,  # Directory where satellite images will be saved.
            operations_save_path,  # Directory where operation log file will be saved.
            preface,  # Prefix for file names.
            farm_coords_wgs84,  # Bounding box coordinates [min_lon, min_lat, max_lon, max_lat] in WGS84.
            figure_save_path,  # Directory where figures will be saved (if applicable).
            csvpath,  # File path for CSV data.
            operext,  # File extension for operation log and satellite images.
            project_name,  # Name of the project.
            request_function,  # Function used for making API requests.
            createImages=False,  # Optional flag to create images.
            i=0,  # Optional index for processing.
            as_nc=False  # Optional flag to save images as NetCDF files.
            ):
    """
    Core routine for downloading, processing, and saving satellite data. For the SentinelHub API.

    Args:
        farm_bbox (BBox): Bounding box of the farm area.
        farm_size (tuple): Size of the farm area.
        date_tuples (list): A list of tuples, each containing start and end dates for data retrieval.
        sat_image_save_path (str): Directory where satellite images will be saved.
        operations_save_path (str): Directory where the operation log file will be saved.
        preface (str): Prefix for file names.
        farm_coords_wgs84 (list): Bounding box coordinates [min_lon, min_lat, max_lon, max_lat] in WGS84.
        figure_save_path (str): Directory where figures will be saved (if applicable).
        csvpath (str): File path for CSV data.
        operext (str): File extension for operation log and satellite images.
        project_name (str): Name of the project.
        request_function (function): Function used for making API requests.
        createImages (bool): Flag to create images (default is False).
        i (int): Index for processing (default is 0).
        as_nc (bool): Flag to save images as NetCDF files (default is False).

    Returns:
        None
    """

    # create a list of requests
    list_of_requests = [request_function(slot, farm_bbox, farm_size, config) for slot in date_tuples]
    list_of_requests = [request.download_list[0] for request in list_of_requests]

    # download data with multiple threads
    data = SentinelHubDownloadClient(config=config).download(list_of_requests, max_threads=5)

    if (isinstance(data[0][0][0], np.ndarray)):
        data = ao.reshape_data(data, i)

    # We are going to download these now as pngs so we don't have to call the api every time,
                                        # only done if createImages variable is True, or as_nc is True
    if (createImages or as_nc):
        sff.save_ndarrays_as_npy(data, sat_image_save_path, preface, date_tuples=date_tuples, project_name = project_name)
        sff.save_ndarrays_as_png(data, sat_image_save_path, preface, date_tuples=date_tuples, project_name = project_name)

    if (as_nc):
        fcf.convert_all_npy_and_nc(sat_image_save_path, preface, date_tuples=date_tuples, project_name = project_name)

    # Now we create a text file with the data we have, so we don't waste api calls if we are just filling data
    sff.populate_text_file(date_tuples, operext, operations_save_path, preface, project_name)

    name = date_tuples[0][0] + "_" + date_tuples[len(date_tuples)-1][1] + preface + '.png'

    # plot the data nicely
    if (len(date_tuples) < 52): # Ideally this would change with allocated ram amount
        pf.plot_ndarrays(data, date_tuples, farm_coords_wgs84, save_path=figure_save_path + project_name + '_' + name)

    ## Writing thermal data to csv

    sff.write_data_to_csv(data, date_tuples, csvpath)
    io.sort_csv_by_date(csvpath) # We do this here instead of in the write so its more efficient and can be moved