## Aidan McEnaney
## June 30th, 2023
## Functions used in the satellite image analysis code


## Imports

import plotFunctions
from configg import *
import sentinelsatRequests
import shutil
import numpy as np
from PIL import Image
import os
import csv
from sentinelhub import (
    CRS,
    BBox,
    SentinelHubDownloadClient,
    bbox_to_dimensions,
)
import netCDF4 as nc
from netCDF4 import Dataset
from sentinelsat import geojson_to_wkt
from datetime import datetime
import zipfile
import glob
import subprocess

## End of Imports

def run_polymer_on_folder(poly_dir, satellite_type=0, filetype=True, sline=None, eline=None, scol=None, ecol=None,
                          blocksize=None, resolution=None, ancillary=0, landmask=None, altitude=None, add_noise=None,
                          srf_file=None, use_srf=None, filename=None, ext=None, tmpdir=None, outdir=None, overwrite=None,
                          datasets=None, compress=None, format=None, multiprocessing=None, dir_base=None, calib=None,
                          normalize=None):
    """
    Calls the POLYMER algorithm on an entire folder of snapshots by calling a bash script in a subprocess that
    then calls a python script, which parses arguments before finally passing them to POLYMER.

    Args:
        poly_dir (str): Directory containing folders with snapshots for POLYMER processing.
        satellite_type (int): Select the satellite that the data came from:
                - 0: OLCI
                - 1: MSI
            Default is 0.
        filetype (bool): If True, output is .nc file; if False, .hdf file. Default is True.
        sline (int): Start line for data processing. Default is None.
        eline (int): End line for data processing. Default is None.
        scol (int): Start column for data processing. Default is None.
        ecol (int): End column for data processing. Default is None.
        blocksize (int): Block size for processing. Default is None.
        resolution (str): Resolution of data, either '60', '20' or '10' (in m). Default is None.
        ancillary (int): Ancillary data option. If 0, use NASA data; if None, no ancillary data. Default is 0.
        landmask (Union[str, None, GSW object]): Landmask information. Can be a string, None, or a GSW object.
            Default is None.
        altitude (Union[float, DEM object]): Altitude parameter. Can be a float, or a DEM object.
            Default is None.
        add_noise (bool):
            Whether to add simulated noise to the radiance data. When set to True,
            random noise is added to the radiance values to simulate measurement
            uncertainty or sensor noise.
            Default is None.
        srf_file (str): Spectral response function. By default, it will use:
            auxdata/msi/S2-SRF_COPE-GSEG-EOPG-TN-15-0007_3.0_S2A.csv for S2A
            auxdata/msi/S2-SRF_COPE-GSEG-EOPG-TN-15-0007_3.0_S2B.csv for S2B
        use_srf (bool): Whether to calculate the bands central wavelengths from the SRF or to use fixed ones.
            Default is None.
        filename (str):
            Output filename. If None, determine filename from level1 by using output directory.
            Default is None.
        ext (str): Output file extension, such as '.nc'. Default is None.
        tmpdir (str): Path of temporary directory. Default is None.
        outdir (str): Output directory. Default is None.
        overwrite (bool): Overwrite existing file. Default is None.
        datasets (list): List of datasets to include in level 2. Default is None.
        compress (bool): Activate compression. Default is None.
        format (str):
            Underlying file format as specified in netcdf's Dataset:
                one of 'NETCDF4', 'NETCDF4_CLASSIC', 'NETCDF3_CLASSIC' or 'NETCDF3_64BIT'
            Default is None.
        multiprocessing (int):
            Number of threads to use for processing
                - 0: Single thread (multiprocessing disactivated)
                - 1 or greater: Use as many threads as there are CPUs on local machine
            Default is None.
        dir_base (str): Location of base directory to locate auxiliary data. Default is None, will use
            'ANCILLARY/METEO'.
        calib (dict):
            A dictionary for applying calibration coefficients.
            Default is None.
        normalize (int):
            Select water reflectance normalization:
                - 0: No geometry nor wavelength normalization
                - 1: Apply normalization of the water reflectance at nadir-nadir
                - 2: Apply wavelength normalization for MERIS and OLCI
                - 3: Apply both geometry and wavelength normalization
            Default is None.

    Returns:
        None
    """

    for folder in os.listdir(poly_dir):
        folder_path = os.path.join(poly_dir, folder)
        if os.path.isdir(folder_path):
            folder_name = os.path.basename(folder_path)
            folder_name = os.path.join(poly_dir, folder_name)

            call_polymer(folder_name, filetype=filetype, sline=sline, eline=eline, scol=scol, ecol=ecol, blocksize=blocksize,
                            ancillary=ancillary, landmask=landmask, altitude=altitude, add_noise=add_noise, filename=filename,
                            ext=ext, tmpdir=tmpdir, outdir=outdir, overwrite=overwrite, datasets=datasets, compress=compress,
                            format=format, multiprocessing=multiprocessing, dir_base=dir_base, calib=calib, normalize=normalize)

def call_polymer(dirname, satellite_type=0, filetype=True, sline=None, eline=None, scol=None, ecol=None,
                          blocksize=None, resolution=None, ancillary=0, landmask=None, altitude=None, add_noise=None,
                          srf_file=None, use_srf=None, filename=None, ext=None, tmpdir=None, outdir=None, overwrite=None,
                          datasets=None, compress=None, format=None, multiprocessing=None, dir_base=None, calib=None,
                          normalize=None):
    """
    Calls the POLYMER algorithm on a single snapshot using subprocess.

    Args:
        dirname (str): Directory name containing input data for POLYMER.
        satellite_type (int): Select the satellite that the data came from:
                - 0: OLCI
                - 1: MSI
            Default is 0.
        filetype (bool): If True, output is .nc file; if False, .hdf file. Default is True.
        sline (int): Start line for data processing. Default is None.
        eline (int): End line for data processing. Default is None.
        scol (int): Start column for data processing. Default is None.
        ecol (int): End column for data processing. Default is None.
        blocksize (int): Block size for processing. Default is None.
        resolution (str): Resolution of data, either '60', '20' or '10' (in m). Default is None.
        ancillary (int): Ancillary data option. If 0, use NASA data; if None, no ancillary data. Default is 0.
        landmask (Union[str, None, GSW object]): Landmask information. Can be a string, None, or a GSW object.
            Default is None.
        altitude (Union[float, DEM object]): Altitude parameter. Can be a float, or a DEM object.
            Default is None.
        add_noise (bool):
            Whether to add simulated noise to the radiance data. When set to True,
            random noise is added to the radiance values to simulate measurement
            uncertainty or sensor noise.
            Default is None.
        srf_file (str): Spectral response function. By default, it will use:
            auxdata/msi/S2-SRF_COPE-GSEG-EOPG-TN-15-0007_3.0_S2A.csv for S2A
            auxdata/msi/S2-SRF_COPE-GSEG-EOPG-TN-15-0007_3.0_S2B.csv for S2B
        use_srf (bool): Whether to calculate the bands central wavelengths from the SRF or to use fixed ones.
            Default is None.
        filename (str):
            Output filename. If None, determine filename from level1 by using output directory.
            Default is None.
        ext (str): Output file extension, such as '.nc'. Default is None.
        tmpdir (str): Path of temporary directory. Default is None.
        outdir (str): Output directory. Default is None.
        overwrite (bool): Overwrite existing file. Default is None.
        datasets (list): List of datasets to include in level 2. Default is None.
        compress (bool): Activate compression. Default is None.
        format (str):
            Underlying file format as specified in netcdf's Dataset:
                one of 'NETCDF4', 'NETCDF4_CLASSIC', 'NETCDF3_CLASSIC' or 'NETCDF3_64BIT'
            Default is None.
        multiprocessing (int):
            Number of threads to use for processing
                - 0: Single thread (multiprocessing disactivated)
                - 1 or greater: Use as many threads as there are CPUs on local machine
            Default is None.
        dir_base (str): Location of base directory to locate auxiliary data. Default is None, will use
            'ANCILLARY/METEO'.
        calib (dict):
            A dictionary for applying calibration coefficients.
            Default is None.
        normalize (int):
            Select water reflectance normalization:
                - 0: No geometry nor wavelength normalization
                - 1: Apply normalization of the water reflectance at nadir-nadir
                - 2: Apply wavelength normalization for MERIS and OLCI
                - 3: Apply both geometry and wavelength normalization
            Default is None.

    Returns:
        None
    """
    if (satellite_type == 0):
        args = ["./run_polymer.sh", "run_polymer", dirname] # Initialize with required arguments
    elif (satellite_type == 1):
        args = ["./run_polymer_msi.sh", "run_polymer", dirname]  # Initialize with required arguments

    # Append optional arguments only if they are not None
    if filetype is not None:
        args.extend(["--filetype", str(filetype)])
    if sline is not None:
        args.extend(["--sline", str(sline)])
    if eline is not None:
        args.extend(["--eline", str(eline)])
    if scol is not None:
        args.extend(["--scol", str(scol)])
    if ecol is not None:
        args.extend(["--ecol", str(ecol)])
    if blocksize is not None:
        args.extend(["--blocksize", str(blocksize)])
    if resolution is not None:
        args.extend(["--resolution", str(resolution)])
    if ancillary is not None:
        args.extend(["--ancillary", str(ancillary)])
    if landmask is not None:
        args.extend(["--landmask", landmask])
    if altitude is not None:
        args.extend(["--altitude", str(altitude)])
    if add_noise is not None:
        args.extend(["--add_noise", str(add_noise)])
    if srf_file is not None:
        args.extend(["--srf_file", str(srf_file)])
    if use_srf is not None:
        args.extend(["--use_srf", str(use_srf)])
    if filename is not None:
        args.extend(["--filename", filename])
    if ext is not None:
        args.extend(["--ext", ext])
    if tmpdir is not None:
        args.extend(["--tmpdir", tmpdir])
    if outdir is not None:
        args.extend(["--outdir", outdir])
    if overwrite is not None:
        args.extend(["--overwrite", str(overwrite)])
    if datasets is not None:
        args.extend(["--datasets", datasets])
    if compress is not None:
        args.extend(["--compress", str(compress)])
    if format is not None:
        args.extend(["--format", format])
    if multiprocessing is not None:
        args.extend(["--multiprocessing", str(multiprocessing)])
    if dir_base is not None:
        args.extend(["--dir_base", dir_base])
    if calib is not None:
        args.extend(["--calib", calib])
    if normalize is not None:
        args.extend(["--normalize", str(normalize)])

    try:
        subprocess.run(args, check=True) # Calls script
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def most_recent_folder(folder_paths):
    """
    Fetches the most recently created folder and returns the absolute path.

    Args:
        folder_paths (list): List of folder paths to search for the most recent one.

    Returns:
        str: Absolute path of the most recently created folder.
    """

    most_recent_time = 0
    most_recent_folder = None

    for i in range(len(folder_paths)):
        if (folder_paths[i].endswith('.DS_Store')):
            folder_paths.pop(i)

    for folder_path in folder_paths:
        if os.path.isdir(folder_path):
            creation_time = os.path.getctime(folder_path)
            if creation_time > most_recent_time:
                most_recent_time = creation_time
                most_recent_folder = folder_path

    return most_recent_folder

def delete_folder_with_contents(folder_name):
    """
    Deletes a folder along with all of its contents.

    Args:
        folder_name (str): Path of the folder to be deleted.

    Returns:
        None
    """

    try:
        shutil.rmtree(folder_name)
        print(f"Folder '{folder_name}' and its contents have been deleted successfully.")
    except Exception as e:
        print(f"An error occurred while deleting '{folder_name}': {e}")

def get_folder_name(path):
    """
    Gets the name of a subfolder within the given folder.

    Args:
        path (str): Path of the folder to search for subfolders.

    Returns:
        str: Name of the subfolder.
    """

    items = os.listdir(path)

    # Filter out only the subfolders
    subfolders = [item for item in items if os.path.isdir(os.path.join(path, item))]

    # Assuming there's only one subfolder, get its name
    if len(subfolders) == 1:
        singular_folder_name = subfolders[0]
    else:
        print("No singular folder found or multiple subfolders present.")

    return singular_folder_name

def create_batch_folders(save_path):
    """
    Create a series of nested folders based on the provided file path.

    Args:
        save_path (str): Path to the file, including the filename at the end.

    Returns:
        None
    """

    folders = save_path.split('/')  # Gets names of required folders

    for i in range(len(folders) - 1):
        tmp_path = os.path.join(*list(folders[:i + 1]))
        if (i > 0):
            tmp_path2 = os.path.join(*list(folders[:i]))
        else:
            tmp_path2 = ''
        if (not os.path.exists(tmp_path)):
            create_folder(tmp_path2, folders[i])

def sort_list_b_based_on_list_a(a, b):
    """
    Sort the elements in list 'b' based on their order in list 'a'.

    Args:
        a (list): The reference list with desired order.
        b (list): The list to be sorted based on the order of list 'a'.

    Returns:
        list: The sorted list 'b' based on the order of list 'a'.
    """

    # Create a dictionary to store the indices of elements in list 'a'
    index_dict = {value: index for index, value in enumerate(a)}

    # Sort list 'b' based on the indices in list 'a'
    sorted_b = sorted(b, key=lambda x: index_dict[x])

    return sorted_b

def del_file(file_path):
    """
    Delete a file at the specified file path.

    Args:
        file_path (str): Path to the file to be deleted.

    Returns:
        None
    """

    try:
        os.remove(file_path)
    except OSError as e:
        print(f"Error: {e}")

def get_surface_level_folders(folder_path):
    """
    Get a list of subfolder names in the specified folder (surface level only).

    Args:
        folder_path (str): Path to the folder where subfolders will be retrieved.

    Returns:
        list: List of subfolder names in the specified folder.
    """

    try:
        # Get a list of all items (files and subfolders) in the specified folder
        all_items = os.listdir(folder_path)

        # Filter out only the directories (subfolders) from the list
        subfolders = [item for item in all_items if os.path.isdir(os.path.join(folder_path, item))]

        return subfolders
    except OSError as e:
        print(f"Error: {e}")
        return []

def remove_overlap(current_working_directory, deeper_file_path):
    """
    Remove the overlapping portion of two file paths and return the new file path.

    Args:
        current_working_directory (str): Path to the current working directory.
        deeper_file_path (str): Full file path to a location deeper within the directory structure.

    Returns:
        str: New file path with the overlapping portion removed.
    """

    # Normalize the paths to handle different separators (e.g., / or \)
    current_working_directory = os.path.normpath(current_working_directory)
    deeper_file_path = os.path.normpath(deeper_file_path)

    # Split the paths into individual directories
    cwd_dirs = current_working_directory.split(os.sep)
    deeper_dirs = deeper_file_path.split(os.sep)

    new_dirs = set(deeper_dirs).difference(set(cwd_dirs)) # Set operation to remove overlap
    new_dirs = list(new_dirs)

    new_dirs = sort_list_b_based_on_list_a(list(deeper_dirs), new_dirs) # Fixes order since sets don't have order

    # Combine the remaining directories to form the new file path
    new_file_path = os.path.join(*new_dirs)

    return new_file_path

def move_files_by_type(start_folder, destination_folder, file_type):
    """
    Move files of a specific type from a source folder to a destination folder.

    Args:
        start_folder (str): Path to the source folder where files will be moved from.
        destination_folder (str): Path to the destination folder where files will be moved to.
        file_type (str): File extension or type of files to be moved (e.g., '.txt', '.csv').

    Returns:
        None
    """

    # Ensure the folders end with a path separator '/'
    start_folder = os.path.normpath(start_folder) + os.sep
    destination_folder = os.path.normpath(destination_folder) + os.sep

    # Create the destination folder if it doesn't exist
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    # Get a list of all files in the starting folder (surface level only)
    files = os.listdir(start_folder)
    for file in files:
        if os.path.isfile(os.path.join(start_folder, file)) and file.endswith(file_type):
            source_file_path = os.path.join(start_folder, file)
            destination_file_path = os.path.join(destination_folder, file)
            shutil.move(source_file_path, destination_file_path)

def find_files_with_strings(folder_path, search_strings):
    """
    Find files in a folder that contain specific search strings in their names.

    Args:
        folder_path (str): Path to the folder where files will be searched.
        search_strings (list): List of search strings to match in file names.

    Returns:
        list: List of file paths that match the search strings.
    """

    # Create an empty list to store the matching file paths
    matching_files = []

    # Get a list of all files in the folder (not diving into subfolders)
    with os.scandir(folder_path) as entries:
        for entry in entries:
            if entry.is_file() and any(search_str in entry.name for search_str in search_strings):
                matching_files.append(entry.path)

    return matching_files

def calculate_and_save_result(npy_files, float_list, name, saveLoc):
    """
    Calculate a weighted sum using data from .npy files and save the result to a new .npy file.

    Args:
        npy_files (list): List of paths to .npy files containing data.
        float_list (list): List of floating-point weights for each .npy file.
        name (str): Name of the output .npy file (without extension).
        saveLoc (str): Directory where the output .npy file will be saved.

    Returns:
        None
    """

    if len(float_list) != len(npy_files) + 1:
        print(f"npy files: '{npy_files}'")
        print(f"float list: '{float_list}'")
        raise ValueError("The length of float_list should be one more than the number of npy_files.")

    # Read the data from each .npy file and store it in a list
    npy_data = [np.load(file_path) for file_path in npy_files]

    # Perform the calculations
    result = float_list[0]
    for i in range(len(npy_data)):
        result += float_list[i+1] * npy_data[i]

    name = name + '.npy'
    savePath = os.path.join(saveLoc, name)

    # Save the result to a new .npy file
    np.save(savePath, result)

def unzip_all_zip_files(directory):
    """
    Unzip all the .zip files in a directory and remove the original zip files (optional).

    Args:
        directory (str): Path to the directory containing .zip files.

    Returns:
        None
    """

    # Iterate through all the files in the directory
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        # Check if the current item is a zip file
        if filename.lower().endswith(".zip"):
            # Create a ZipFile object and extract its contents
            with zipfile.ZipFile(filepath, 'r') as zip_ref:
                zip_ref.extractall(directory)

            # Remove the original zip file if desired (optional)
            os.remove(filepath)

def move_elements_down_one(input_list):
    """
    Move elements in a list down by one position, creating an empty element at the beginning.

    Args:
        input_list (list): The input list to be shifted.

    Returns:
        list: A new list with elements shifted down by one position.
    """

    # Create a new list with an empty element at the beginning
    new_list = [''] + input_list[:-1]
    return new_list

def bbox_to_WKT(bbox):
    """
    Convert a bounding box to a Well-Known Text (WKT) representation.

    Args:
        bbox (tuple): Bounding box coordinates as a tuple (min_x, min_y, max_x, max_y).

    Returns:
        str: Well-Known Text (WKT) representation of the bounding box.
    """
    # https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry
    # bbox is read in as a tuple, not a SentinelHub bbox type

    # Convert the bounding box coordinates to WKT format using GeoJSON
    wkt_bbox = geojson_to_wkt({'type': 'Polygon', 'coordinates': [[
        [bbox[0], bbox[1]],
        [bbox[0], bbox[3]],
        [bbox[2], bbox[3]],
        [bbox[2], bbox[1]],
        [bbox[0], bbox[1]]]]})

    return wkt_bbox


def create_folder(path, folder_name, do_prints=False):
    """
    Create a folder with the given name in the specified path.

    Args:
        path (str): Path where the folder will be created.
        folder_name (str): Name of the folder to be created.
        do_prints (bool): Whether to print status messages (default is False).

    Returns:
        None
    """

    # Combine the path and folder name
    folder_path = os.path.join(path, folder_name)

    # Check if the folder already exists
    if not os.path.exists(folder_path):
        # Create the folder
        os.makedirs(folder_path)
        if (do_prints):
            print(f"Folder '{folder_name}' created at '{folder_path}'")
    else:
        if (do_prints):
            print(f"Folder '{folder_name}' already exists at '{folder_path}'")


def convert_all_npy_and_nc(path, preface="image", date_tuples=None, project_name='name', folder_name='sen'):
    """
    Convert multiple .npy files to NetCDF (.nc) format, organized in folders.

    Args:
        path (str): Path to the directory containing the .npy files.
        preface (str): Prefix for filenames (default is "image").
        date_tuples (list of tuple): List of tuples, each containing start and end dates (default is None).
        project_name (str): Project name to be included in the filenames (default is 'name').
        folder_name (str): Name of the subfolder where converted files will be saved (default is 'sen').

    Returns:
        None
    """

    for i in range(len(date_tuples)):
        tmp = str(date_tuples[i]) + '_' + preface + '_' + project_name + '_' + folder_name
        create_folder(path, tmp)

        path2 = path + tmp

        # Generate the filename
        filename = f"{preface}_{i}."
        if date_tuples and i < len(date_tuples) and len(date_tuples[i]) == 2:
            date_str_1 = date_tuples[i][0]
            date_str_2 = date_tuples[i][1]
            filename = f"{date_str_1}_{date_str_2}_{filename}"

        filename = project_name + '_' + filename

        # Save the ndarray as .npy file
        full_filename1 = os.path.join(path, filename)
        full_filename2 = os.path.join(path2, filename)
        convert_npy_to_nc(full_filename1 + 'npy', full_filename2 + 'nc')

def convert_npy_to_nc(npy_path, download_path):
    """
    Convert a NumPy array saved as .npy file to a NetCDF (.nc) file.

    Args:
        npy_path (str): Path to the input .npy file.
        download_path (str): Path to save the output NetCDF file.

    Returns:
        None
    """

    # Load npy file
    np_array = load_npy_file(npy_path)

    # Create netCDF file
    nc_file = Dataset(download_path, 'w', format='NETCDF4')

    # Create dimensions based on np_array shape
    for dim_idx, dim_size in enumerate(np_array.shape):
        nc_file.createDimension(f'dim_{dim_idx}', dim_size)

    # Create variable with the same shape as np_array
    nc_var = nc_file.createVariable('data', np_array.dtype, tuple(f'dim_{i}' for i in range(np_array.ndim)))

    # Assign data from np_array to the variable
    nc_var[:] = np_array[:]

    # Close the netCDF file
    nc_file.close()

def process_directory(directory, save_to=None):
    """
    Convert NetCDF (.nc) files in a directory and its subdirectories to NumPy arrays.

    Args:
        directory (str): Path to the directory containing .nc files.
        save_to (str): Directory path to save the converted .npy files (default is None).

    Returns:
        None
    """

    # Get a list of all files with the '.nc' extension in the specified directory and its subdirectories
    nc_files = glob.glob(os.path.join(directory, '**', '*.nc'), recursive=True)

    for nc_file in nc_files:
        # Call the 'convert_nc_to_npy' function for each .nc file found
        convert_nc_to_npy(nc_file, save_to)

def convert_nc_to_npy(nc_file_path, save_to=None):
    """
    Convert a NetCDF (.nc) file to a NumPy array saved as .npy file.

    Args:
        nc_file_path (str): Path to the input .nc file.
        save_to (str): Directory path to save the converted .npy file (default is None).

    Returns:
        None
    """

    try:
        # Open the NetCDF file
        dataset = nc.Dataset(nc_file_path)

        for variable_name in list(dataset.variables.keys()):
            try:
                # Check if the variable_name exists in the NetCDF file
                if variable_name not in dataset.variables:
                    print("Variable not found in the NetCDF file:", variable_name)
                    continue  # Skip to the next variable

                if isinstance(save_to, str) and save_to is not None:
                    npy_file_path_tmp = os.path.join(os.getcwd(), os.path.dirname(nc_file_path)) # Excludes file name
                    create_folder(npy_file_path_tmp, save_to) # Creates folder to save to
                    npy_file_path1 = os.path.join(npy_file_path_tmp, save_to, os.path.basename(nc_file_path))
                else:
                    npy_file_path1 = nc_file_path

                npy_file_path = remove_file_extension(npy_file_path1) + str(variable_name)

                # Read the data from the NetCDF file
                data = dataset.variables[variable_name][:]

                # Convert the data to NumPy array
                np_data = np.array(data)

                # Save the NumPy array to an npy file
                np.save(npy_file_path, np_data)

            except Exception as e:
                if not (isinstance(e, FileNotFoundError) and "No such file or directory: 'None'" in str(e)):
                    print("An error occurred while processing variable", variable_name, ":", e)

        # Close the NetCDF file outside the loop
        dataset.close()

    except Exception as e:
        if not (isinstance(e, FileNotFoundError) and "No such file or directory: 'None'" in str(e)):
            print("An error occurred:", e)


def load_npy_file(file_path):
    """
    Load a NumPy array from a .npy file.

    Args:
        file_path (str): Path to the input .npy file.

    Returns:
        np.ndarray: Loaded NumPy array.
    """

    try:
        array = np.load(file_path)
        return array
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except ValueError:
        print(f"Error: Unable to load file '{file_path}'. Verify it is a valid .npy file.")
    except Exception as e:
        print(f"Error: An error occurred while loading file '{file_path}': {str(e)}")

def remove_file_extension(file_path):
    """
    Remove the file extension from a given file path.

    Args:
        file_path (str): File path from which the extension will be removed.

    Returns:
        str: File name without the extension.
    """

    filename, file_extension = os.path.splitext(file_path)
    return filename

def kelvin_to_fahrenheit(kelvin):
    """
    Convert temperature in Kelvin to Fahrenheit.

    Args:
        kelvin (float): Temperature in Kelvin.

    Returns:
        float: Temperature in Fahrenheit.
    """

    fahrenheit = (kelvin - 273.15) * 9/5 + 32
    return fahrenheit

def get_timeslots(start, end, n_chunks):
    """
    Divide a time period into equal-sized time slots.

    Args:
        start (datetime): Start datetime of the time period.
        end (datetime): End datetime of the time period.
        n_chunks (int): Number of equal-sized time slots.

    Returns:
        list of tuple: List of tuples representing start and end datetime for each time slot.
    """

    tdelta = (end - start) / n_chunks
    edges = [(start + i * tdelta).date().isoformat() for i in range(n_chunks)]
    date_tuples = [(edges[i], edges[i + 1]) for i in range(len(edges) - 1)]

    return date_tuples


def create_blank_file(filename):
    """
    Create an empty file if it doesn't already exist.

    Args:
        filename (str): Name of the file to be created.

    Returns:
        None
    """

    # Split the filename into name and extension
    _, file_extension = os.path.splitext(filename)

    if os.path.exists(filename):
        print(f"Error: File '{filename}' already exists, continuing. If you are seeing this something went wrong.")
    else:
        with open(filename, 'w'):
            pass


def write_data_to_csv(ndarrays,  # List of ndarrays containing data to be written to CSV.
                      date_tuples,  # List of tuples, each containing start and end dates.
                      csv_path  # Path to the CSV file where data will be written.
                      ):
    """
    Write data from ndarrays to a CSV file, including statistics for each date range.

    Args:
        ndarrays (list of np.ndarray): List of ndarrays containing data to be written to CSV.
        date_tuples (list of tuple): List of tuples, each containing start and end dates.
        csv_path (str): Path to the CSV file where data will be written.

    Returns:
        None
    """

    # Prepare the data for writing to CSV
    data = []
    for date, arr in zip(date_tuples, ndarrays):
        average = np.average(arr)
        minimum = np.min(arr)
        maximum = np.max(arr)
        std_dev = np.std(arr)
        data.append([date, average, minimum, maximum, std_dev])

    # Check if the file already exists
    file_exists = os.path.isfile(csv_path)

    # Write data to the CSV file
    with open(csv_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Write header row if the file doesn't exist or if the header is different
        if not file_exists or not has_matching_header(csv_path):
            writer.writerow(['Date Range', 'Average', 'Minimum', 'Maximum', 'Standard Deviation'])

        writer.writerows(data)

def has_matching_header(csv_path):
    """
    Check if a CSV file has a matching header with expected column names.

    Args:
        csv_path (str): Path to the CSV file to be checked.

    Returns:
        bool: True if the header matches the expected column names, False otherwise.
    """

    with open(csv_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header_row = next(reader, [])
        expected_header = ['Date Range', 'Average', 'Minimum', 'Maximum', 'Standard Deviation']
        return header_row == expected_header


def sort_csv_by_date(csv_file):
    """
    Sort a CSV file by date in the first column.

    Args:
        csv_file (str): Path to the CSV file to be sorted.

    Returns:
        None
    """

    temp_file = 'temp.csv'

    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

        header = rows[0]
        data = rows[1:]

        sorted_data = sorted(data, key=lambda x: datetime.strptime(eval(x[0])[0], '%Y-%m-%d'))

        sorted_rows = [header] + sorted_data

        with open(temp_file, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(sorted_rows)

    shutil.move(temp_file, csv_file)


def save_ndarrays_as_png(ndarrays,  # List of ndarrays to be saved as PNGs.
                         path,  # Directory path where PNG files will be saved.
                         preface="image",  # Prefix for filenames (default is "image").
                         date_tuples=None,  # List of tuples, each containing start and end dates (default is None).
                         project_name='name'  # Project name (default is 'name').
                         ):
    """
    Save ndarrays as PNG image files with optional date-based filenames.

    Args:
        ndarrays (list of np.ndarray): List of ndarrays to be saved as PNGs.
        path (str): Directory path where PNG files will be saved.
        preface (str): Prefix for filenames (default is "image").
        date_tuples (list of tuple): List of tuples, each containing start and end dates (default is None).
        project_name (str): Project name (default is 'name').

    Returns:
        None
    """

    # Create the directory if it doesn't exist
    if not os.path.exists(path):
        os.makedirs(path)

    # Iterate over the ndarrays and save them as PNGs
    for i, arr in enumerate(ndarrays):
        # Normalize the array values to 0-255 range
        normalized_arr = (arr - np.min(arr)) / (np.max(arr) - np.min(arr)) * 255
        # Convert to unsigned 8-bit integers
        uint8_arr = normalized_arr.astype(np.uint8)
        # Create an Image object from the ndarray
        image = Image.fromarray(uint8_arr)

        # Generate the filename
        filename = f"{preface}_{i}.png"
        if date_tuples and i < len(date_tuples) and len(date_tuples[i]) == 2:
            date_str_1 = date_tuples[i][0]
            date_str_2 = date_tuples[i][1]
            # Convert string dates to datetime objects
            date_obj_1 = datetime.strptime(date_str_1, "%Y-%m-%d")
            date_obj_2 = datetime.strptime(date_str_2, "%Y-%m-%d")
            date_formatted_1 = date_obj_1.strftime("%Y-%m-%d")
            date_formatted_2 = date_obj_2.strftime("%Y-%m-%d")
            filename = f"{date_formatted_1}_{date_formatted_2}_{filename}"

        filename = project_name + '_' + filename

        # Save the image as PNG
        full_filename = os.path.join(path, filename)
        image.save(full_filename)

def save_ndarrays_as_npy(ndarrays,  # List of ndarrays to be saved.
                         path,  # Directory path where .npy files will be saved.
                         preface="array",  # Prefix for filenames (default is "array").
                         date_tuples=None,  # List of tuples, each containing start and end dates (default is None).
                         project_name='name'  # Project name (default is 'name').
                         ):
    """
    Save ndarrays as .npy files with optional date-based filenames.

    Args:
        ndarrays (list of np.ndarray): List of ndarrays to be saved.
        path (str): Directory path where .npy files will be saved.
        preface (str): Prefix for filenames (default is "array").
        date_tuples (list of tuple): List of tuples, each containing start and end dates (default is None).
        project_name (str): Project name (default is 'name').

    Returns:
        None
    """

    # Create the directory if it doesn't exist
    if not os.path.exists(path):
        os.makedirs(path)

    # Iterate over the ndarrays and save them as .npy files
    for i, arr in enumerate(ndarrays):
        # Generate the filename
        filename = f"{preface}_{i}.npy"
        if date_tuples and i < len(date_tuples) and len(date_tuples[i]) == 2:
            date_str_1 = date_tuples[i][0]
            date_str_2 = date_tuples[i][1]
            filename = f"{date_str_1}_{date_str_2}_{filename}"

        filename = project_name + '_' + filename

        # Save the ndarray as .npy file
        full_filename = os.path.join(path, filename)
        np.save(full_filename, arr)


def populate_text_file(date_tuples,  # List of tuples, each containing start and end dates.
                       file_extension,  # File extension for filenames.
                       path,  # File path to the text file.
                       preface,  # Prefix for filenames.
                       project_name='name'  # Project name (default is 'name').
                       ):
    """
    Populate a text file with generated filenames based on date tuples.

    Args:
        date_tuples (list of tuple): A list of tuples, each containing start and end dates.
        file_extension (str): File extension for filenames.
        path (str): File path to the text file.
        preface (str): Prefix for filenames.
        project_name (str): Project name (default is 'name').

    Returns:
        None
    """

    # Open the text file in append mode
    with open(path, "a") as file:
        # Iterate over the date tuples
        for i, date_tuple in enumerate(date_tuples):
            # Generate the filename
            filename = f"{preface}_{i}{file_extension}"
            if len(date_tuple) == 2:
                date_str_1 = date_tuple[0]
                date_str_2 = date_tuple[1]
                # Convert string dates to datetime objects
                date_obj_1 = datetime.strptime(date_str_1, "%Y-%m-%d")
                date_obj_2 = datetime.strptime(date_str_2, "%Y-%m-%d")
                date_formatted_1 = date_obj_1.strftime("%Y-%m-%d")
                date_formatted_2 = date_obj_2.strftime("%Y-%m-%d")
                filename = f"{date_formatted_1}_{date_formatted_2}_{filename}"

            filename = project_name + '_' + filename

            # Write the filename to the text file
            file.write(filename + "\n")


def check_files_exist(date_tuples,  # List of tuples, each containing start and end dates.
                      file_extension,  # File extension to check.
                      directory_path,  # Directory path where files are expected to exist.
                      preface  # Prefix for filenames.
                      ):
    """
    Check for the existence of files with specific names in a directory.

    Args:
        date_tuples (list of tuple): A list of tuples, each containing start and end dates.
        file_extension (str): File extension to check.
        directory_path (str): Directory path where files are expected to exist.
        preface (str): Prefix for filenames.

    Returns:
        list of str: List of filenames that do not exist in the specified directory.
    """

    non_existing_files = []

    for i, (start_date, end_date) in enumerate(date_tuples):
        file_name = f"{start_date}_{end_date}_{preface}_{i}{file_extension}"
        file_path = os.path.join(directory_path, file_name)

        if not os.path.exists(file_path):
            non_existing_files.append(file_name)

    return non_existing_files


def check_files_exist_in_text_file(date_tuples,  # List of tuples, each containing start and end dates.
                                   file_extension,  # File extension to check.
                                   file_path,  # Path to the text file containing existing filenames.
                                   preface,  # Prefix for filenames.
                                   project  # Project name.
                                   ):
    """
    Check for the existence of files listed in a text file.
    Used for log file, so extra API calls are not used when downloading data from the SentinelHub API.

    Args:
        date_tuples (list): A list of tuples, each containing start and end dates.
        file_extension (str): File extension to check.
        file_path (str): Path to the text file containing existing filenames.
        preface (str): Prefix for filenames.
        project (str): Project name.

    Returns:
        list: List of filenames that do not exist in the text file.
    """

    # Read the contents of the text file
    with open(file_path, "r") as file:
        existing_files = file.read().splitlines()

    non_existing_files = []

    # Iterate over the date tuples
    for i, date_tuple in enumerate(date_tuples):
        # Generate the filename
        filename = f"{project}_{'_'.join(date_tuple)}_{preface}_{i}{file_extension}"

        # Check if the filename exists in the text file
        if filename not in existing_files:
            non_existing_files.append(filename)

    return non_existing_files

def reshape_data(data, p):
    """
    Reshape data arrays to extract a specific slice along a specified axis.

    Args:
        data (list of np.ndarray): List of data arrays to be reshaped.
        p (int): Index along the third axis to extract from each data array.

    Returns:
        list of np.ndarray: List of reshaped data arrays, each containing the specified slice.
    """
    # Used for when a SentinelHub request has multiple bands.
    # This reshapes the data so that each band can be analyzed separately.

    reshaped_data = []
    for arr in data:
        reshaped_arr = np.transpose(arr, axes=(0, 1, 2))
        reshaped_arr = reshaped_arr[:, :, p]
        reshaped_data.append(reshaped_arr)
    return reshaped_data

def sentinelsat_routine(bbox,  # Bounding box coordinates [min_lon, min_lat, max_lon, max_lat].
                        date_tuples,  # List of tuples, each containing start and end dates for data retrieval.
                        download_directory,  # Directory where downloaded zip files will be saved.
                        request_function  # Function used for making API requests and downloading zips.
                        ):
    """
    Routine for using SentinelSat API to download and process Sentinel data.

    Args:
        bbox (list): Bounding box coordinates [min_lon, min_lat, max_lon, max_lat].
        date_tuples (list): A list of tuples, each containing start and end dates for data retrieval.
        download_directory (str): Directory where downloaded zip files will be saved.
        request_function (function): Function used for making API requests and downloading zip files.

    Returns:
        None
    """

    tmp = download_directory.split('/')
    tmp = move_elements_down_one(tmp)

    for i in range(len(tmp) - 1): # Creates folders
        create_folder(tmp[i], tmp[i + 1])

    request_function(date_tuples, bbox, download_directory)  # Downloads zips

    unzip_all_zip_files(download_directory)  # Unzips all the folders, so we have folders of .nc files, also deletes zips


def routine(farm_bbox,  # Bounding box of the farm area.
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
        data = reshape_data(data, i)

    # We are going to download these now as pngs so we don't have to call the api every time,
                                        # only done if createImages variable is True, or as_nc is True
    if (createImages or as_nc):
        save_ndarrays_as_npy(data, sat_image_save_path, preface, date_tuples=date_tuples, project_name = project_name)
        save_ndarrays_as_png(data, sat_image_save_path, preface, date_tuples=date_tuples, project_name = project_name)

    if (as_nc):
        convert_all_npy_and_nc(sat_image_save_path, preface, date_tuples=date_tuples, project_name = project_name)

    # Now we create a text file with the data we have, so we don't waste api calls if we are just filling data
    populate_text_file(date_tuples, operext, operations_save_path, preface, project_name)

    name = date_tuples[0][0] + "_" + date_tuples[len(date_tuples)-1][1] + preface + '.png'

    # plot the data nicely
    if (date_tuples < 52): # Ideally this would change with allocated ram amount
        plotFunctions.plot_ndarrays(data, date_tuples, farm_coords_wgs84, save_path=figure_save_path + project_name + '_' + name)

    ## Writing thermal data to csv

    write_data_to_csv(data, date_tuples, csvpath)
    sort_csv_by_date(csvpath) # We do this here instead of in the write so its more efficient and can be moved


def core(resolution,  # Spatial resolution for data retrieval.
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
    Core function for managing data retrieval, processing, and storage. For the SentinelHub API.

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
        create_batch_folders(operations_save_path) # Creates folders leading up to file
        create_blank_file(operations_save_path) # Create operation log file if it doesn't already exist

    if (not (type(preface) is list)):
        preface = [preface]
        csvpath = [csvpath]

    for i in range(len(preface)):

        # Creating csv
        if (not os.path.exists(csvpath[i])): # Checks if csv already exists
            create_batch_folders(csvpath[i])
            create_blank_file(csvpath[i])

        if (createImages):
            nonexisting = check_files_exist(date_tuples, operext, sat_image_save_path, preface[i])
        else:
            nonexisting = check_files_exist_in_text_file(date_tuples, operext, operations_save_path, preface[i], project_name)

        if (len(nonexisting) == len(date_tuples)):
            routine(farm_bbox, farm_size, date_tuples, sat_image_save_path, operations_save_path, preface[i],
                                farm_coords_wgs84, figure_save_path, csvpath[i], operext, project_name,
                                request_function, createImages = createImages, i=i, as_nc = as_nc)
        elif (len(nonexisting) != 0):
            flots = []

            for file_name in nonexisting:
                date_strings = file_name.split("_")[0:2]
                start_date, end_date = date_strings
                flots.append((start_date, end_date))

            routine(farm_bbox, farm_size, flots, sat_image_save_path, operations_save_path, preface[i],
                                farm_coords_wgs84, figure_save_path, csvpath[i], operext, project_name,
                                request_function, createImages = createImages, i=i, as_nc = as_nc)
        else:
            print("All of these files are already downloaded")