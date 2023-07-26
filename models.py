## Aidan McEnaney
## July 12th, 2023
## Code for various models used to get parameters

## Imports

from configg import *
from datetime import datetime, timedelta
from collections import OrderedDict
import satFunctions
import os
import subprocess

## End of Imports

def model_routine(bbox, date_tuples, project_name, path, model, npy_save_to=None, polymer_root_name = 'polymer-v4.16.1'):

    if (npy_save_to == True): # Default folder for npy files, this is so POLYMER doesnt get upset
        npy_save_to = project_name + '_' + 'npyFiles'

    tmp_ = os.path.join(path, project_name)
    tmp = tmp_.split('/')
    tmp = satFunctions.move_elements_down_one(tmp)

    for i in range(len(tmp)-1):
        satFunctions.create_folder(tmp[i], tmp[i+1])

    func = model(bbox, date_tuples, project_name, path)

    satFunctions.unzip_all_zip_files(tmp_)  # Unzips all the folders, so we have folders of .nc files, also deletes zips

    print(subprocess.run('./run_polymer.sh'))

    convert(tmp_, npy_save_to, func, polymer_root_name=polymer_root_name)

def chlor(bbox, date_tuples, project_name, path):

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

        return chlorophyll


def convert(tmp_, npy_save_to, model_func, polymer_root_name):

    os.chdir(os.path.join(os.getcwd(), polymer_root_name)) # Change directory to that of polymer

    tmp_ = satFunctions.remove_overlap(os.getcwd(), tmp_)

    satFunctions.move_files_by_type(os.getcwd(), tmp_, '.nc') # Moves the outputs from POLYMER

    filevals = satFunctions.get_surface_level_folders(tmp_) # Gets a list of the downloaded folders

    paths = satFunctions.find_files_with_strings(tmp_, filevals) # Get nc files output by POLYMER to convert to npy

    for path in paths: # Creates npy files for all the parts of each nc file
        satFunctions.convert_nc_to_npy(path, save_to=npy_save_to)

    model_func(os.getcwd(), tmp_, npy_save_to) # Calls the specified model

def chlorophyll(changeDir, tmp_, npy_save_to):
    # Algorithm to get chlorophyll-a, from this paper:
    # https://www.sciencedirect.com/science/article/pii/S1569843223000456#b0040

    os.chdir(changeDir)  # Change directory to that of polymer, just in case
    chlor_alg = 'algOut'  # Folder name for chlorophyll algorithm output files
    path2 = os.path.join(tmp_, npy_save_to)

    # Defining regression coefficients
    vals = []
    vals.append(0.761)
    vals.append(0.3495)
    vals.append(-1.512)
    vals.append(1.925)
    vals.append(-9.0585)
    vals.append(8.4015)

    filevals = ['Rw443', 'Rw490', 'Rw560', 'Rw674', 'Rw681'] # Defining the bands we care about

    paths = satFunctions.find_files_with_strings(path2, filevals) # Getting file paths for npy files

    saveLoc = os.path.join(os.getcwd(), tmp_)
    satFunctions.create_folder(saveLoc, chlor_alg)
    saveLoc = os.path.join(saveLoc, chlor_alg)

    satFunctions.calculate_and_save_result(paths, vals, chlor_alg, saveLoc)