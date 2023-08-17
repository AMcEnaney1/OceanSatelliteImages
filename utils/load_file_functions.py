"""
File: load_file_functions.py
Author: Aidan McEnaney
Date: 2023-08-11

Description: This module contains all functions involving loading data from files for this project.

Contents:
    - load_npy_file: Function to load npy file and return it as an array.

Notes:
    - This code is distributed under the MIT License. See LICENSE.txt for more details.
"""

# Standard library imports


# Third-party library imports
import numpy as np

# Local module imports


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