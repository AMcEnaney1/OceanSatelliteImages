## Aidan McEnaney
## June 30th, 2023
## Functions used in the satellite image analysis code


## Imports

import plotFunctions
from configg import *
import shutil
import numpy as np
from PIL import Image
from datetime import datetime
import os
import csv
from sentinelhub import (
    CRS,
    BBox,
    SentinelHubDownloadClient,
    bbox_to_dimensions,
)

## End of Imports

def convert_to_celsius(temperature_array):
    temperature_celsius = temperature_array - 273.15
    return temperature_celsius

def convert_to_fahrenheit(temperature_array):
    temperature_fahrenheit = (temperature_array * 9/5) - 459.67
    return temperature_fahrenheit

def get_timeslots(start, end, n_chunks):
    tdelta = (end - start) / n_chunks
    edges = [(start + i * tdelta).date().isoformat() for i in range(n_chunks)]
    date_tuples = [(edges[i], edges[i + 1]) for i in range(len(edges) - 1)]

    return date_tuples


def create_blank_file(filename):
    _, file_extension = os.path.splitext(filename)
    if os.path.exists(filename):
        print(f"Error: File '{filename}' already exists, continuing.")
    else:
        with open(filename, 'w'):
            pass # Removed creation of empty row as that caused issues with the
                            # current writing method due to now using append mode instead of write mode
                            # Not the main fix for this commit so commenting here, will remove later

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


def routine(farm_bbox, farm_size, date_tuples, sat_image_save_path, operations_save_path, preface, farm_coords_wgs84,
            figure_save_path, csvpath, operext, project_name, request_function, createImages = False):

    # create a list of requests
    list_of_requests = [request_function(slot, farm_bbox, farm_size, config) for slot in date_tuples]
    list_of_requests = [request.download_list[0] for request in list_of_requests]

    # download data with multiple threads
    data = SentinelHubDownloadClient(config=config).download(list_of_requests, max_threads=5)

    # We are going to download these now as pngs so we don't have to call the api every time,
                                        # only done if createImages variable is True
    if (createImages):
        save_ndarrays_as_npy(data, sat_image_save_path, preface, date_tuples=date_tuples, project_name = project_name)
        save_ndarrays_as_png(data, sat_image_save_path, preface, date_tuples=date_tuples, project_name = project_name)

    # Now we create a text file with the data we have so we don't waste api calls if we are just filling data
    populate_text_file(date_tuples, operext, operations_save_path, preface, project_name)

    name = date_tuples[0][0] + "_" + date_tuples[len(date_tuples)-1][1] + preface + '.png'

    # plot the data nicely
    plotFunctions.plot_ndarrays(data, date_tuples, farm_coords_wgs84, save_path=figure_save_path + project_name + '_' + name)

    ## Writing thermal data to csv

    write_data_to_csv(data, date_tuples, csvpath)
    sort_csv_by_date(csvpath) # We do this here instead of in the write so its more efficient and can be moved

def core(resolution, date_tuples, sat_image_save_path, operations_save_path, preface, farm_coords_wgs84,
            figure_save_path, csvpath, operext, project_name, request_function, createImages = False):

    # Setting up resolution and stuff

    farm_bbox = BBox(bbox=farm_coords_wgs84, crs=CRS.WGS84)
    farm_size = bbox_to_dimensions(farm_bbox, resolution=resolution)

    # print(f"Image shape at {resolution} m resolution: {farm_size} pixels") # Troubleshooting code

    # Creating csv

    create_blank_file(csvpath)

    # I want to do a check here so I don't waste api calls on data I already have
    # This will get a list of any expected files that may not be there

    # We also need to create our log file, if one doesn't already exist

    if (not os.path.exists(operations_save_path)): # Operation log file doesn't already exist
        create_blank_file(operations_save_path) # Create operation log file if it doesn't already exist

    if (createImages):
        nonexisting = check_files_exist(date_tuples, operext, sat_image_save_path, preface)
    else:
        nonexisting = check_files_exist_in_text_file(date_tuples, operext, operations_save_path, preface, project_name)

    if (len(nonexisting) == len(date_tuples)):
        routine(farm_bbox, farm_size, date_tuples, sat_image_save_path, operations_save_path, preface,
                             farm_coords_wgs84, figure_save_path, csvpath, operext, project_name, request_function, createImages = createImages)
    elif (len(nonexisting) != 0):
        flots = []

        for file_name in nonexisting:
            date_strings = file_name.split("_")[0:2]
            start_date, end_date = date_strings
            flots.append((start_date, end_date))

        routine(farm_bbox, farm_size, flots, sat_image_save_path, operations_save_path, preface,
                             farm_coords_wgs84, figure_save_path, csvpath, operext, project_name, request_function, createImages = createImages)
    else:
        print("All of these files are already downloaded")
