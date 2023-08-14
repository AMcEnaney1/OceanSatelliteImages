"""
File: io_functions.py
Author: Aidan McEnaney
Date: 2023-08-11

Description: This module contains all the IO functions for this project.

Contents:
    - unzip_all_zip_files: Function to unzip all files in given directory.
    - create_batch_folders: Function that takes a path and creates all folders along it.
    - create_folder: Function that creates a folder.
    - create_blank_file: Function that creates a blank file at a passed location.
    - check_files_exist: Function that checks if files exist and returns names of ones that don't.
    - check_files_exist_in_text_file: Function that takes strings and a file path and returns the strings not present in the file.
    - has_matching_header: Function to check if header is an expected in a csv file.
    - sort_csv_by_date: Function to sort a passed csv by date.

Notes:
    - This code is distributed under the MIT License. See LICENSE.txt for more details.
"""

# Standard library imports
import os
import csv
import shutil
from datetime import datetime

# Third-party library imports
import zipfile

# Local module imports
import utils.misc_functions as mf

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


def create_batch_folders(save_path):
    """
    Create a series of nested folders based on the provided file path.

    Args:
        save_path (str): Path to the file, including the filename at the end.

    Returns:
        None
    """

    # Get only deeper folders
    save_path = mf.remove_overlap(os.getcwd(), save_path)

    folders = save_path.split('/')  # Gets names of required folders

    for i in range(len(folders) - 1):
        tmp_path = os.path.join(*list(folders[:i + 1]))
        if (i > 0):
            tmp_path2 = os.path.join(*list(folders[:i]))
        else:
            tmp_path2 = ''
        if (not os.path.exists(tmp_path)):
            create_folder(tmp_path2, folders[i])


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
