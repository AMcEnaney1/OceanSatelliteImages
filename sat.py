## Aidan McEnaney
## June 30th, 2023
## Code for satellite image analysis


## Imports

import satFunctions
import evalscripts
import requestFunctions
import keys
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
    # Setting up config
    config = SHConfig()
    config.sh_client_id = keys.client_id
    config.sh_client_secret = keys.client_secret

    if not config.sh_client_id or not config.sh_client_secret:
        print("Warning! To use Process API, please provide the credentials (OAuth client ID and client secret).")

    # Setting up farm coordinates
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


    ## Actually doing stuff for thermal data ##

    # create a list of requests
    list_of_requests = [requestFunctions.get_thermal_request(slot, farm_bbox, farm_size, config) for slot in slots]
    list_of_requests = [request.download_list[0] for request in list_of_requests]

    # download data with multiple threads
    data = SentinelHubDownloadClient(config=config).download(list_of_requests, max_threads=5)

    # plot the data nicely
    satFunctions.plot_ndarrays(data, slots, farm_coords_wgs84)

    ## End of stuff for thermal data ##

if __name__ == "__main__":
    main()