"""
File: misc_functions.py
Author: Aidan McEnaney
Date: 2023-08-11

Description: Module containing misc functions.

Contents:
    - folder_creation_manage: Function that decides which folder creation function to use.
    - remove_file_extension: Function to remove file extension.
    - find_files_with_strings: Function that finds files in folders with given strings in their name.
    - most_recent_folders: Function to determine the newest folders of passed folders.
    - most_recent_folder: Function to determine the newest folder of passed folders.
    - get_surface_level_folders: Function that returns the name of folders present at the surface level of passed path.
    - bbox_to_WKT: Function to convert bbox to WKT format.
    - sort_list_b_based_on_list_a: Function to sort list.
    - remove_overlap: Function to make an absolute path into a local path.
    - make_absolute_paths: Function that turns local paths into absolute paths, operates on lists.
    - make_absolute_paths_dict: Function that turns local paths into absolute paths, operates on dictionaries.
    - make_absolute_paths_list: Does the same thing on a list of dictionaries.
    - get_timeslots: Function that turns start and end data into date tuples.
    - kelvin_to_fahrenheit: Function that converts Kelvin to Fahrenheit.

Notes:
    - This code is distributed under the MIT License. See LICENSE.txt for more details.
"""

# Standard library imports
import os
from operator import itemgetter

# Third-party library imports
from sentinelsat import geojson_to_wkt

# Local module imports
import utils.io_functions as io

def folder_creation_manage(path):
    """
    Passes file path to correct function for it to be created.

    Args:
        path (str): File path of which to create folders along.

    Returns:
        None
    """
    if (os.path.isabs(path)):
        io.create_batch_folders_absolute_path(path)
    else:
        io.create_batch_folders(path)


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


def most_recent_folders(folder_paths, num_folders=1):
    """
    Fetches the most recently created folders and returns their absolute paths.

    Args:
        folder_paths (list): List of folder paths to search for the most recent ones.
        num_folders (int): Number of most recent folders to return.

    Returns:
        list: List of absolute paths of the most recently created folders.
    """

    folder_info = []

    for folder_path in folder_paths:
        if not folder_path.endswith('.DS_Store') and os.path.isdir(folder_path):
            creation_time = os.path.getctime(folder_path)
            folder_info.append((folder_path, creation_time))

    folder_info.sort(key=itemgetter(1), reverse=True)

    most_recent_folders = [info[0] for info in folder_info[:num_folders]]

    return most_recent_folders


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


def make_absolute_paths(file_paths):
    """
    Convert a list of file paths to their absolute equivalents, preserving any trailing slashes.

    This function takes a list of file paths and converts each path to its absolute form using the `os.path.abspath()`
    function. If a path originally had a trailing '/', this trailing slash is preserved in the absolute path.

    Args:
        file_paths (list of str): A list of file paths to be converted to absolute paths.

    Returns:
        list of str: A list of absolute paths, with trailing slashes preserved if present in the original paths.
    """
    absolute_paths = []

    for path in file_paths:
        absolute_path = os.path.abspath(path)
        if path.endswith('/'):  # Check if the original path had a trailing '/'
            absolute_path += '/'  # Add the trailing '/' back
        absolute_paths.append(absolute_path)

    return absolute_paths


def make_absolute_paths_dict(file_paths_dict):
    """
    Convert file paths within a dictionary to their absolute equivalents, preserving any trailing slashes.

    This function takes a dictionary where keys represent labels and values are either strings or lists of file paths.
    It converts each file path to its absolute form using the `os.path.abspath()` function. If a path originally had a
    trailing '/', this trailing slash is preserved in the absolute path.

    Args:
        file_paths_dict (dict): A dictionary with keys representing labels and values containing file path(s) to be
                               converted to absolute paths.

    Returns:
        None. The input dictionary is modified in place with absolute paths, and no new dictionary is returned.
    """
    for key, paths in file_paths_dict.items():
        if isinstance(paths, str):
            absolute_path = os.path.abspath(paths)
            if paths.endswith('/'):  # Check if the original path had a trailing '/'
                absolute_path += '/'  # Add the trailing '/' back
            file_paths_dict[key] = absolute_path
        elif isinstance(paths, list):
            absolute_paths = []
            for path in paths:
                absolute_path = os.path.abspath(path)
                if path.endswith('/'):  # Check if the original path had a trailing '/'
                    absolute_path += '/'  # Add the trailing '/' back
                absolute_paths.append(absolute_path)
            file_paths_dict[key] = absolute_paths


def make_absolute_paths_list(list_of_dicts):
    """
    Convert file paths within a list of dictionaries to their absolute equivalents, preserving any trailing slashes.

    This function takes a list of dictionaries, where each dictionary contains key-value pairs. The values can be
    either strings or lists of file paths. The function converts each file path to its absolute form using the
    `os.path.abspath()` function. If a path originally had a trailing '/', this trailing slash is preserved in the
    absolute path.

    Args:
        list_of_dicts (list): A list of dictionaries, where each dictionary contains key-value pairs. The values
                             can be file path(s) to be converted to absolute paths.

    Returns:
        None. The input list of dictionaries is modified in place with absolute paths, and no new list is returned.
    """
    for file_paths_dict in list_of_dicts:
        for key, paths in file_paths_dict.items():
            if isinstance(paths, str):
                absolute_path = os.path.abspath(paths)
                if paths.endswith('/'):  # Check if the original path had a trailing '/'
                    absolute_path += '/'  # Add the trailing '/' back
                file_paths_dict[key] = absolute_path
            elif isinstance(paths, list):
                absolute_paths = []
                for path in paths:
                    absolute_path = os.path.abspath(path)
                    if path.endswith('/'):  # Check if the original path had a trailing '/'
                        absolute_path += '/'  # Add the trailing '/' back
                    absolute_paths.append(absolute_path)
                file_paths_dict[key] = absolute_paths


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