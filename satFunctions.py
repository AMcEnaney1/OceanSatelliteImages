## Aidan McEnaney
## June 30th, 2023
## Functions used in the satellite image analysis code


## Imports

import plotFunctions
from configg import *
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

## End of Imports

def create_batch_folders(save_path): # Takes in path terminating with file
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
    # Create a dictionary to store the indices of elements in list 'a'
    index_dict = {value: index for index, value in enumerate(a)}

    # Sort list 'b' based on the indices in list 'a'
    sorted_b = sorted(b, key=lambda x: index_dict[x])

    return sorted_b

def del_file(file_path):
    try:
        os.remove(file_path)
    except OSError as e:
        print(f"Error: {e}")

def get_surface_level_folders(folder_path):
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
    # Create an empty list to store the matching file paths
    matching_files = []

    # Get a list of all files in the folder (not diving into subfolders)
    with os.scandir(folder_path) as entries:
        for entry in entries:
            if entry.is_file() and any(search_str in entry.name for search_str in search_strings):
                matching_files.append(entry.path)

    return matching_files

def calculate_and_save_result(npy_files, float_list, name, saveLoc):
    if len(float_list) != len(npy_files) + 1:
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
    new_list = [''] + input_list[:-1]
    return new_list

def bbox_to_WKT(bbox): # Converts a bounding box to well-known text representation form
    # https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry
    # bbox is read in as a tuple, not a SentinelHub bbox type

    wkt_bbox = geojson_to_wkt({'type': 'Polygon', 'coordinates': [[
        [bbox[0], bbox[1]],
        [bbox[0], bbox[3]],
        [bbox[2], bbox[3]],
        [bbox[2], bbox[1]],
        [bbox[0], bbox[1]]]]})

    return wkt_bbox

def create_folder(path, folder_name, do_prints = False):
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


def convert_all_npy_and_nc(path, preface="image", date_tuples=None, project_name='name', folder_name = 'sen'):

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

def process_directory(directory, save_to = None):

    # Get a list of all files with the '.nc' extension in the specified directory and its subdirectories
    nc_files = glob.glob(os.path.join(directory, '**', '*.nc'), recursive=True)

    for nc_file in nc_files:
        # Call the 'convert_nc_to_npy' function for each .nc file found
        convert_nc_to_npy(nc_file, save_to)

def convert_nc_to_npy(nc_file_path, save_to=None):
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
                print("An error occurred while processing variable", variable_name, ":", e)

        # Close the NetCDF file outside the loop
        dataset.close()

    except Exception as e:
        print("An error occurred:", e)

def load_npy_file(file_path):
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
    filename, file_extension = os.path.splitext(file_path)
    return filename

def kelvin_to_fahrenheit(kelvin):
    fahrenheit = (kelvin - 273.15) * 9/5 + 32
    return fahrenheit

def get_timeslots(start, end, n_chunks):
    tdelta = (end - start) / n_chunks
    edges = [(start + i * tdelta).date().isoformat() for i in range(n_chunks)]
    date_tuples = [(edges[i], edges[i + 1]) for i in range(len(edges) - 1)]

    return date_tuples

def create_blank_file(filename):
    _, file_extension = os.path.splitext(filename)
    if os.path.exists(filename):
        print(f"Error: File '{filename}' already exists, continuing. If you are seeing this something went wrong.")
    else:
        with open(filename, 'w'):
            pass

def write_data_to_csv(ndarrays, date_tuples, csv_path):
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
    with open(csv_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header_row = next(reader, [])
        expected_header = ['Date Range', 'Average', 'Minimum', 'Maximum', 'Standard Deviation']
        return header_row == expected_header


def sort_csv_by_date(csv_file):
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

def save_ndarrays_as_png(ndarrays, path, preface="image", date_tuples=None, project_name='name'):
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

def save_ndarrays_as_npy(ndarrays, path, preface="array", date_tuples=None, project_name='name'):
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


def populate_text_file(date_tuples, file_extension, path, preface, project_name = 'name'):
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


def check_files_exist(date_tuples, file_extension, directory_path, preface):
    non_existing_files = []

    for i, (start_date, end_date) in enumerate(date_tuples):
        file_name = f"{start_date}_{end_date}_{preface}_{i}{file_extension}"
        file_path = os.path.join(directory_path, file_name)

        if not os.path.exists(file_path):
            non_existing_files.append(file_name)

    return non_existing_files

def check_files_exist_in_text_file(date_tuples, file_extension, file_path, preface, project):
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
    reshaped_data = []
    for arr in data:
        reshaped_arr = np.transpose(arr, axes=(0, 1, 2))
        reshaped_arr = reshaped_arr[:, :, p]
        reshaped_data.append(reshaped_arr)
    return reshaped_data

def routine(farm_bbox, farm_size, date_tuples, sat_image_save_path, operations_save_path, preface, farm_coords_wgs84,
            figure_save_path, csvpath, operext, project_name, request_function, createImages = False, i=0, as_nc = False):

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
    plotFunctions.plot_ndarrays(data, date_tuples, farm_coords_wgs84, save_path=figure_save_path + project_name + '_' + name)

    ## Writing thermal data to csv

    write_data_to_csv(data, date_tuples, csvpath)
    sort_csv_by_date(csvpath) # We do this here instead of in the write so its more efficient and can be moved

def core(resolution, date_tuples, sat_image_save_path, operations_save_path, preface, farm_coords_wgs84,
            figure_save_path, csvpath, operext, project_name, request_function, createImages = False, as_nc = False):

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
