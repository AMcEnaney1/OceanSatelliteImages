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

    csvpath = 'out/data/compData.csv'
    figure_save_path = 'out/figures/'
    sat_image_save_path = 'out/satData/images/'

    thermalPreface = 'Thermal'

    ## End of setting variables ##

    if not config.sh_client_id or not config.sh_client_secret:
        print("Warning! To use Process API, please provide the credentials (OAuth client ID and client secret).")

    ## Setting up farm coordinates
    farm_coords_wgs84 = (-69.9040, 43.8586, -69.8987, 43.8651) # Coordinates for the farm
    resolution = 30 # Resolution for thermal images
    farm_bbox = BBox(bbox=farm_coords_wgs84, crs=CRS.WGS84)
    farm_size = bbox_to_dimensions(farm_bbox, resolution=resolution)

    #print(f"Image shape at {resolution} m resolution: {farm_size} pixels") # Troubleshooting code

    # Setting up start and end date as well as the amount of snapshots
    start = datetime.datetime(2021, 1, 1)
    end = datetime.datetime(2021, 12, 31)
    n_chunks = 13
    slots = satFunctions.get_timeslots(start, end, n_chunks)

    ## Creating csv

    satFunctions.create_blank_csv(csvpath)


    ## Actually doing stuff for thermal data ##


    # I want to do a check here so I don't waste api calls on data I already have
    # This will get a list of any expected files that may not be there

    nonexisting = satFunctions.check_files_exist(slots, '.npy', sat_image_save_path, thermalPreface)

    if(len(nonexisting) == len(slots)):
        satFunctions.routine(farm_bbox, farm_size, slots, sat_image_save_path, thermalPreface, farm_coords_wgs84,
                             figure_save_path, csvpath)
    elif(len(nonexisting) != 0):
        slots = []

        for file_name in nonexisting:
            date_strings = file_name.split("_")[0:2]
            start_date, end_date = date_strings
            slots.append((start_date, end_date))

        satFunctions.routine(farm_bbox, farm_size, slots, sat_image_save_path, thermalPreface, farm_coords_wgs84,
                             figure_save_path, csvpath)

    # create a list of requests
    list_of_requests = [requestFunctions.get_thermal_request(slot, farm_bbox, farm_size, config) for slot in slots]
    list_of_requests = [request.download_list[0] for request in list_of_requests]

    # download data with multiple threads
    data = SentinelHubDownloadClient(config=config).download(list_of_requests, max_threads=5)

    # We are going to download these now as pngs so we don't have to call the api every time
    satFunctions.save_ndarrays_as_npy(data, sat_image_save_path, preface = thermalPreface, date_tuples= slots)
    satFunctions.save_ndarrays_as_pngs(data, sat_image_save_path, preface=thermalPreface, date_tuples=slots)

    # plot the data nicely
    satFunctions.plot_ndarrays(data, slots, farm_coords_wgs84, save_path=figure_save_path + 'thermalFigure.png')

    ## Writing thermal data to csv

    satFunctions.write_data_to_csv(data, slots, csvpath)

    ## End of stuff for thermal data ##

if __name__ == "__main__":
    main()