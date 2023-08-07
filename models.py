## Aidan McEnaney
## July 12th, 2023
## Code for various models used to get parameters

## Start of imports

import satFunctions
import os

## End of imports

def model_routine(bbox, date_tuples, project_name, path, model, poly_dir, request_function, npy_save_to=None,
                  polymer_root_name='polymer-v4.16.1'):

    # This will probably take hundreds of gigabytes of available storage to run

    if (npy_save_to == True):  # Default folder for npy files, this is so POLYMER doesnt get upset
        npy_save_to = project_name + '_' + 'npyFiles'

    download_directory = os.path.join(path, project_name)

    satFunctions.sentinelsat_routine(bbox, date_tuples, download_directory, request_function)

    satFunctions.run_polymer_on_folder(poly_dir)

    convert(download_directory, npy_save_to, model, polymer_root_name=polymer_root_name)

def model_routine_space_eff(bbox, date_tuples, project_name, model, poly_dir, request_function, npy_save_to=None,
                  polymer_root_name='polymer-v4.16.1'):

    if (npy_save_to == None):  # Default folder for npy files, this is so POLYMER doesnt get upset
        npy_save_to = project_name + '_' + 'npyFiles'

    for i in range(len(date_tuples)):

        date_tuple = [(str(date_tuples[i][0]), str(date_tuples[i][1]))]

        poly_dir2 = satFunctions.remove_overlap(os.getcwd(), poly_dir)

        satFunctions.sentinelsat_routine(bbox, date_tuple, poly_dir2, request_function)

        filevals = satFunctions.get_surface_level_folders(poly_dir)  # Gets a list of the downloaded folders

        for i in range(len(filevals)):
            filevals[i] = os.path.join(poly_dir, filevals[i])

        folder = satFunctions.most_recent_folder(filevals)

        satFunctions.call_polymer(folder)

        convert_eff(poly_dir, npy_save_to, model, polymer_root_name=polymer_root_name)

        satFunctions.delete_folder_with_contents(folder) # deletes sentinel folder
        file = satFunctions.find_files_with_strings(poly_dir, folder)
        satFunctions.del_file(file[0])
        satFunctions.delete_folder_with_contents(os.path.join(poly_dir, npy_save_to))


def convert_eff(tmp_, npy_save_to, model_func, polymer_root_name):

    os.chdir(os.path.join(os.getcwd(), polymer_root_name)) # Change directory to that of polymer

    tmp_ = satFunctions.remove_overlap(os.getcwd(), tmp_)

    satFunctions.move_files_by_type(os.getcwd(), tmp_, '.nc') # Moves the outputs from POLYMER

    filevals = satFunctions.get_surface_level_folders(tmp_) # Gets a list of the downloaded folders

    paths = satFunctions.find_files_with_strings(tmp_, filevals) # Get nc files output by POLYMER to convert to npy

    for path in paths: # Creates npy files for all the parts of each nc file
        satFunctions.convert_nc_to_npy(path, save_to=npy_save_to)

    path = satFunctions.most_recent_folder(paths)

    satFunctions.convert_nc_to_npy(path, save_to=npy_save_to)

    name = satFunctions.remove_overlap(tmp_, paths[0])
    name = name.rsplit('.', 1)[0]

    model_func(os.getcwd(), tmp_, npy_save_to, name) # Calls the specified model

    os.chdir(os.path.dirname(os.getcwd())) # Move back one directory, like with cd ..

def convert(tmp_, npy_save_to, model_func, polymer_root_name):

    os.chdir(os.path.join(os.getcwd(), polymer_root_name)) # Change directory to that of polymer

    tmp_ = satFunctions.remove_overlap(os.getcwd(), tmp_)

    satFunctions.move_files_by_type(os.getcwd(), tmp_, '.nc') # Moves the outputs from POLYMER

    filevals = satFunctions.get_surface_level_folders(tmp_) # Gets a list of the downloaded folders

    paths = satFunctions.find_files_with_strings(tmp_, filevals) # Get nc files output by POLYMER to convert to npy

    for path in paths: # Creates npy files for all the parts of each nc file
        satFunctions.convert_nc_to_npy(path, save_to=npy_save_to)

    name = satFunctions.remove_overlap(tmp_, paths[0])
    name = name.rsplit('.', 1)[0]

    model_func(os.getcwd(), tmp_, npy_save_to, name) # Calls the specified model

    os.chdir(os.path.dirname(os.getcwd())) # Move back one directory, like with cd ..

def chlor(changeDir, tmp_, npy_save_to, name):
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

    satFunctions.calculate_and_save_result(paths, vals, name, saveLoc)