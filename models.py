## Aidan McEnaney
## July 12th, 2023
## Code for various models used to get parameters

## Imports

from configg import *
from datetime import datetime, timedelta
from collections import OrderedDict
import satFunctions
import os

## End of Imports

def chlor(bbox, date_tuples, project_name, path, npy_save_to = None):

    if (npy_save_to == True): # Default folder for npy files, this is so POLYMER doesnt get upset
        npy_save_to = project_name + 'npyFiles'

    tmp_ = os.path.join(path, project_name)
    tmp = tmp_.split('/')
    tmp = satFunctions.move_elements_down_one(tmp)

    for i in range(len(tmp)-1):
        satFunctions.create_folder(tmp[i], tmp[i+1])

    wkt_bbox = satFunctions.bbox_to_WKT(bbox)

    for i in range(len(date_tuples)):
        start_date = datetime.strptime(date_tuples[i][0], '%Y-%m-%d')
        end_date = datetime.strptime(date_tuples[i][1], '%Y-%m-%d')

        # Initialize an empty OrderedDict to store the products
        products = OrderedDict()

        # Query for products on the earliest date within the date range
        current_date = start_date
        while current_date <= end_date:
            query_kwargs = {
                'platformname': 'Sentinel-3',
                'instrumentshortname': 'OLCI',
                'date': (current_date, current_date + timedelta(days=1)),  # Query for a single day
                'area': wkt_bbox  # Use the WKT representation for the bounding box
            }
            pp = api.query(**query_kwargs)

            if pp:
                # If products are found on the current date, add them to the products OrderedDict and break the loop
                products.update(pp)
                break

            # Move to the next date
            current_date += timedelta(days=1)

        # Set your desired download directory here
        download_directory = os.path.join(path, project_name)

        # Use the download_path parameter to specify the download directory
        api.download_all(products, directory_path=download_directory)

    satFunctions.unzip_all_zip_files(tmp_) # Unzips all the folders, so we have folders of .nc files
    satFunctions.delete_all_zip_files(tmp_)  # Deletes all of the zip folders
    #satFunctions.process_directory(tmp_, npy_save_to) # Converts all of these .nc files into .npy files


def RemoteReflectance():
    # Atmospheric Correction algorithm
    # Calculates water reflectance, used to get chlorophyll-a. This is the POLYMER algorithm.
    # This algorithm came from here: https://opg.optica.org/oe/fulltext.cfm?uri=oe-19-10-9783&id=213648
    # And was used to get chlorophyll-a in this paper: https://www.sciencedirect.com/science/article/pii/S1569843223000456#b0190



    return 0

def chlorophyll(arr):
    # Algorithm to get chlorophyll-a, from this paper:
    # https://www.sciencedirect.com/science/article/pii/S1569843223000456#b0040

    # Defining regression coefficients
    B0 = 0.761
    B1 = 0.3495
    B2 = -1.512
    B3 = 1.925
    B4 = -9.0585
    B5 = 8.4015


    ### Needs to be finished

    # Defining reflectance values
    R1 = RemoteReflectance()
    R2 = RemoteReflectance()
    R3 = RemoteReflectance()
    R4 = RemoteReflectance()
    R5 = RemoteReflectance()

    val = B0 + (B1 * R1) + (B2 * R2) + (B3 * R3) + (B4 * R4) + (B5 * R5)

    return val