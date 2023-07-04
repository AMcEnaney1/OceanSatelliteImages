## Aidan McEnaney
## June 30th, 2023
## Code for satellite image analysis


## Imports

import satFunctions
import evalscripts
import requestFunctions
import keys
from configg import *
import numpy as np
import matplotlib.pyplot as plt
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from PIL import Image
import io
import datetime
import os
from sentinelhub import (
    CRS,
    BBox,
    DataCollection,
    DownloadRequest,
    MimeType,
    MosaickingOrder,
    SentinelHubDownloadClient,
    SentinelHubRequest,
    bbox_to_dimensions,
    SHConfig,
)
from utils import plot_image
import math

## End of Imports

def main():

    ## Setting variables ##

    createImages = False # Set to True in order to create .npy and .png files of downloaded images.
                                        # Double check that it actually passed to the routine funcion if set to True

    operext = '.npy'
    operations_txt_filename = 'oper.txt'
    csvpath_base = 'out/data/compData'
    csvpath_thermal =  csvpath_base + '_Thermal.csv'
    csvpath_chlorophyll = csvpath_base + '_Chlor.csv'
    figure_save_path = 'out/figures/'
    sat_image_save_path = 'out/satData/images/'
    operations_save_path = 'out/satData/logs/' + operations_txt_filename

    thermalPreface = 'Thermal'
    chlorophyllPreface = 'Chlor'

    ## End of setting variables ##

    if not config.sh_client_id or not config.sh_client_secret:
        print("Warning! To use Process API, please provide the credentials (OAuth client ID and client secret).")

    ## Setting up farm coordinates
    farm_coords_wgs84 = (-69.9040, 43.8586, -69.8987, 43.8651) # Coordinates for the farm

    # Setting up start and end date as well as the amount of snapshots
    start = datetime.datetime(2021, 1, 1)
    end = datetime.datetime(2021, 12, 31)
    n_chunks = 13
    slots = satFunctions.get_timeslots(start, end, n_chunks)

    # Creating operation logging text file

    satFunctions.create_blank_file(operations_save_path)

    ## Actually doing stuff for thermal data ##

    # Setting up resolution and stuff

    resolution = 30  # Resolution for thermal images
    farm_bbox = BBox(bbox=farm_coords_wgs84, crs=CRS.WGS84)
    farm_size = bbox_to_dimensions(farm_bbox, resolution=resolution)

    # print(f"Image shape at {resolution} m resolution: {farm_size} pixels") # Troubleshooting code

    # Creating csv

    satFunctions.create_blank_file(csvpath_thermal)

    # I want to do a check here so I don't waste api calls on data I already have
    # This will get a list of any expected files that may not be there

    if createImages:
        nonexisting = satFunctions.check_files_exist(slots, operext, sat_image_save_path, thermalPreface)
    else:
        nonexisting = satFunctions.check_files_exist_in_text_file(slots, operext, operations_save_path, thermalPreface)

    if(len(nonexisting) == len(slots)):
        satFunctions.routine(farm_bbox, farm_size, slots, sat_image_save_path, operations_save_path, thermalPreface, farm_coords_wgs84,
                             figure_save_path, csvpath_thermal, operext, request_function=requestFunctions.get_thermal_request)
    elif(len(nonexisting) != 0):
        flots = []

        for file_name in nonexisting:
            date_strings = file_name.split("_")[0:2]
            start_date, end_date = date_strings
            flots.append((start_date, end_date))

        satFunctions.routine(farm_bbox, farm_size, flots, sat_image_save_path, operations_save_path, thermalPreface, farm_coords_wgs84,
                             figure_save_path, csvpath_thermal, operext, request_function=requestFunctions.get_thermal_request)
    else:
        print("All of these files are already downloaded")

    ## End of stuff for thermal data ##


    ## Start of stuff for Chlorophyll

    # Setting up resolution and stuff

    resolution = 100  # Resolution for chlorophyll images, actual res is 300,
                                    # but we can't assume our bbox line up exactl, especially with such a small area
    farm_bbox = BBox(bbox=farm_coords_wgs84, crs=CRS.WGS84)
    farm_size = bbox_to_dimensions(farm_bbox, resolution=resolution)

        # print(f"Image shape at {resolution} m resolution: {farm_size} pixels") # Troubleshooting code

    # Creating csv

    satFunctions.create_blank_file(csvpath_chlorophyll)

    # I want to do a check here so I don't waste api calls on data I already have
    # This will get a list of any expected files that may not be there

    nonexisting = satFunctions.check_files_exist(slots, '.npy', sat_image_save_path, chlorophyllPreface)

    if(len(nonexisting) == len(slots)):
        satFunctions.routine(farm_bbox, farm_size, slots, sat_image_save_path, operations_save_path, chlorophyllPreface, farm_coords_wgs84,
                             figure_save_path, csvpath_chlorophyll, operext, request_function=requestFunctions.get_chlorophyll_request)
    elif(len(nonexisting) != 0):
        flots = []

        for file_name in nonexisting:
            date_strings = file_name.split("_")[0:2]
            start_date, end_date = date_strings
            flots.append((start_date, end_date))

        satFunctions.routine(farm_bbox, farm_size, flots, sat_image_save_path, operations_save_path, chlorophyllPreface, farm_coords_wgs84,
                             figure_save_path, csvpath_chlorophyll, operext, request_function=requestFunctions.get_chlorophyll_request)
    else:
        print("All of these files are already downloaded")

    ## End of stuff for chlorophyll data ##


if __name__ == "__main__":
    main()