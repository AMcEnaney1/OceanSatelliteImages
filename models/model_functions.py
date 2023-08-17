"""
File: model_functions.py
Author: Aidan McEnaney
Date: 2023-08-16

Description: This module contains all functions for parameter models.

Contents:
    - chlor: Function to perform linear chlorophyll model.

Notes:
    - This code is distributed under the MIT License. See LICENSE.txt for more details.
"""

# Standard library imports
import os

# Third-party library imports

# Local module imports
import utils.model_application_functions as maf
import utils.misc_functions as mf
import utils.io_functions as io

def chlor(changeDir, tmp_, npy_save_to, name):
    """
    Algorithm to calculate chlorophyll-a concentration from remote sensing data.
    https://www.sciencedirect.com/science/article/pii/S1569843223000456#b0040

    Args:
        changeDir (str): Directory path for changing directory.
        tmp_ (str): Temporary directory path.
        npy_save_to (str): Path to save NumPy files.
        name (str): Name for saving results.

    Returns:
        None
    """

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

    paths = mf.find_files_with_strings(path2, filevals) # Getting file paths for npy files

    saveLoc = os.path.join(os.getcwd(), tmp_)
    io.create_folder(saveLoc, chlor_alg)
    saveLoc = os.path.join(saveLoc, chlor_alg)

    maf.calculate_and_save_result(paths, vals, name, saveLoc)