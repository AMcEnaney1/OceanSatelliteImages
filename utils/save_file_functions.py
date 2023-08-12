"""
File: save_file_functions.py
Author: Aidan McEnaney
Date: 2023-08-11

Description: This module contains all functions involving saving data as files for this project.

Contents:
    - save_ndarrays_as_png: Function that takes a list of ndarrays and writes them to pngs.
    - save_ndarrays_as_npy: Function that takes a list of ndarrays and writes them to npys.
    - write_data_to_csv: Function that takes a list of ndarrays and writes some stats to a csv file.
    - populate_text_file: Funciton that write filenames to text file.

Notes:
    - This code is distributed under the MIT License. See LICENSE.txt for more details.
"""

# Standard library imports
import os
import csv
from datetime import datetime

# Third-party library imports
import numpy as np
from PIL import Image

# Local module imports
import utils.io_functions as io

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
        if not file_exists or not io.has_matching_header(csv_path):
            writer.writerow(['Date Range', 'Average', 'Minimum', 'Maximum', 'Standard Deviation'])

        writer.writerows(data)