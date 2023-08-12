"""
File: array_operations.py
Author: Aidan McEnaney
Date: 2023-08-11

Description: This module contains functions performing array operations.

Contents:
    - reshape_data: Function that reshapes a np.ndarry so a multiple band request can be treated as multiple singular band requests.

Notes:
    - This code is distributed under the MIT License. See LICENSE.txt for more details.
"""

# Standard library imports


# Third-party library imports
import numpy as np

# Local module imports


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