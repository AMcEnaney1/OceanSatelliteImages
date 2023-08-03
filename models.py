## Aidan McEnaney
## July 12th, 2023
## Code for various models used to get parameters

## Start of imports

import satFunctions
import os

## End of imports

def model_routine(bbox, date_tuples, project_name, path, model, poly_dir, request_function, npy_save_to=None):
    if (npy_save_to == True):  # Default folder for npy files, this is so POLYMER doesnt get upset
        npy_save_to = project_name + '_' + 'npyFiles'

    download_directory = os.path.join(path, project_name)

    satFunctions.sentinelsat_routine(bbox, date_tuples, download_directory, request_function)

    satFunctions.run_polymer_on_folder(poly_dir)

    convert(download_directory, npy_save_to, model, polymer_root_name=polymer_root_name)

def convert(tmp_, npy_save_to, model_func, polymer_root_name):

    os.chdir(os.path.join(os.getcwd(), polymer_root_name)) # Change directory to that of polymer

    tmp_ = satFunctions.remove_overlap(os.getcwd(), tmp_)

    satFunctions.move_files_by_type(os.getcwd(), tmp_, '.nc') # Moves the outputs from POLYMER

    filevals = satFunctions.get_surface_level_folders(tmp_) # Gets a list of the downloaded folders

    paths = satFunctions.find_files_with_strings(tmp_, filevals) # Get nc files output by POLYMER to convert to npy

    for path in paths: # Creates npy files for all the parts of each nc file
        satFunctions.convert_nc_to_npy(path, save_to=npy_save_to)

    model_func(os.getcwd(), tmp_, npy_save_to) # Calls the specified model

def chlor(changeDir, tmp_, npy_save_to):
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