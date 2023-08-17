"""
File: file_conversion_functions.py
Author: Aidan McEnaney
Date: 2023-08-11

Description: This module contains all functions involving file conversions for this project.

Contents:
    - convert_nc_to_npy: Function that takes an nc files and converts it to an npy file.
    - convert_npy_to_nc: Function that takes a npy file and writes it as a nc file.
    - convert_all_nc_and_npy: Function that converts multiple npy files to nc files.

Notes:
    - This code is distributed under the MIT License. See LICENSE.txt for more details.
"""

# Standard library imports
import os

# Third-party library imports
from netCDF4 import Dataset
import netCDF4 as nc
import numpy as np

# Local module imports
import utils.io_functions as io
import utils.load_file_functions as lff
import utils.misc_functions as mf

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
                    io.create_folder(npy_file_path_tmp, save_to) # Creates folder to save to
                    npy_file_path1 = os.path.join(npy_file_path_tmp, save_to, os.path.basename(nc_file_path))
                else:
                    npy_file_path1 = nc_file_path

                npy_file_path = mf.remove_file_extension(npy_file_path1) + str(variable_name)

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
    np_array = lff.load_npy_file(npy_path)

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
        io.create_folder(path, tmp)

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
