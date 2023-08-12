"""
File: file_conversion_functions.py
Author: Aidan McEnaney
Date: 2023-08-11

Description: This module contains all functions involving file conversions for this project.

Contents:
    - convert_npy_to_nc: Function that takes a npy file and writes it as a nc file.
    - convert_all_nc_and_npy: Function that converts multiple npy files to nc files.

Notes:
    - This code is distributed under the MIT License. See LICENSE.txt for more details.
"""

# Standard library imports
import os

# Third-party library imports
from netCDF4 import Dataset

# Local module imports
import utils.io_functions as io
import utils.load_file_functions as lff

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
