## Aidan McEnaney
## June 30th, 2023
## Functions used in the satellite image analysis code


## Imports

from configg import *
import shutil
import requestFunctions
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import io
from datetime import datetime
import os
from utils import plot_image
import math
import csv
from sentinelhub import (
    CRS,
    BBox,
    DataCollection,
    DownloadRequest,
    MimeType,
    MosaickingOrder,
    SentinelHubDownloadClient,
    SentinelHubRequest,
    bbox_to_dimensions,
    SHConfig,
)

## End of Imports

def plot_ndarrays(ndarrays, titles, coordinates, num_columns=3, save_path=None):
    if len(ndarrays) != len(titles):
        raise ValueError("Number of ndarrays and titles must be the same.")

    if save_path and os.path.exists(save_path):
        print("Error: File already exists. Please choose a different filename.")
        return

    num_plots = len(ndarrays)
    num_rows = (num_plots - 1) // num_columns + 1

    fig, axes = plt.subplots(num_rows, num_columns, figsize=(4 * num_columns, 4 * num_rows))
    axes = axes.ravel()  # Flatten the axes array

    for i, (arr, title) in enumerate(zip(ndarrays, titles)):
        ax = axes[i]

        # Plot the ndarray
        img = ax.imshow(arr)
        ax.set_title(' to '.join(map(str, title)))  # Concatenate the title elements with a '-' character

        # Set the custom coordinate labels
        lon_left, lat_bottom, lon_right, lat_top = coordinates
        x_ticks = np.linspace(0, arr.shape[1] - 1, num=5)
        y_ticks = np.linspace(0, arr.shape[0] - 1, num=5)
        x_labels = np.linspace(lon_left, lon_right, num=5)
        y_labels = np.linspace(lat_bottom, lat_top, num=5)
        ax.set_xticks(x_ticks)
        ax.set_yticks(y_ticks)
        ax.set_xticklabels(["{:.4f}".format(x) for x in x_labels])
        ax.set_yticklabels(["{:.4f}".format(y) for y in y_labels])

        # Rotate x-axis labels by 45 degrees
        ax.tick_params(axis='x', labelrotation=45)

    # Hide any unused subplots
    for j in range(num_plots, num_rows * num_columns):
        fig.delaxes(axes[j])

    plt.tight_layout()

    if save_path:
        plt.savefig(save_path)  # Save the figure as an image file

    plt.show()

def convert_to_celsius(temperature_array):
    temperature_celsius = temperature_array - 273.15
    return temperature_celsius

def convert_to_fahrenheit(temperature_array):
    temperature_fahrenheit = (temperature_array * 9/5) - 459.67
    return temperature_fahrenheit

def get_timeslots(start, end, n_chunks):
    tdelta = (end - start) / n_chunks
    edges = [(start + i * tdelta).date().isoformat() for i in range(n_chunks)]
    slots = [(edges[i], edges[i + 1]) for i in range(len(edges) - 1)]

    return slots

def create_blank_csv(filename):
    if os.path.exists(filename):
        print(f"Error: CSV file '{filename}' already exists, continuing.")
    else:
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([])  # Write an empty row

def write_data_to_csv(ndarrays, slots, csv_path):
    # Prepare the data for writing to CSV
    data = []
    for date, arr in zip(slots, ndarrays):
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


def write_data_to_csv_old(ndarrays, slots, csv_path):
    # Prepare the data for writing to CSV
    data = []
    for date, arr in zip(slots, ndarrays):
        average = np.average(arr)
        minimum = np.min(arr)
        maximum = np.max(arr)
        std_dev = np.std(arr)
        data.append([date, average, minimum, maximum, std_dev])

    # Write data to the CSV file
    with open(csv_path, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # Check if the file is empty
        file_empty = csvfile.tell() == 0

        if file_empty:
            writer.writerow(['Date Range', 'Average', 'Minimum', 'Maximum', 'Standard Deviation'])  # Write header row

        # Read existing data from the file
        existing_data = []
        if not file_empty:
            reader = csv.reader(csvfile)
            existing_data = list(reader)

        # Insert new data in the correct row based on the date
        for new_row in data:
            new_date = new_row[0]
            row_inserted = False
            for i, existing_row in enumerate(existing_data):
                if new_date < existing_row[0]:
                    existing_data.insert(i, new_row)
                    row_inserted = True
                    break

            if not row_inserted:
                existing_data.append(new_row)

        # Write all the data to the file
        csvfile.seek(0)
        writer.writerows(existing_data)


def save_ndarrays_as_pngs(ndarrays, path, preface="image", date_tuples=None):
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

        # Save the image as PNG
        full_filename = os.path.join(path, filename)
        image.save(full_filename)

def save_ndarrays_as_npy(ndarrays, path, preface="array", date_tuples=None):
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

        # Save the ndarray as .npy file
        full_filename = os.path.join(path, filename)
        np.save(full_filename, arr)

def check_files_exist(slots, file_extension, directory_path, preface):
    non_existing_files = []

    for i, (start_date, end_date) in enumerate(slots):
        file_name = f"{start_date}_{end_date}_{preface}_{i}{file_extension}"
        file_path = os.path.join(directory_path, file_name)

        if not os.path.exists(file_path):
            non_existing_files.append(file_name)

    return non_existing_files

def routine(farm_bbox, farm_size, slots, sat_image_save_path, thermalPreface, farm_coords_wgs84, figure_save_path, csvpath):
    # create a list of requests
    list_of_requests = [requestFunctions.get_thermal_request(slot, farm_bbox, farm_size, config) for slot in slots]
    list_of_requests = [request.download_list[0] for request in list_of_requests]

    # download data with multiple threads
    data = SentinelHubDownloadClient(config=config).download(list_of_requests, max_threads=5)

    # We are going to download these now as pngs so we don't have to call the api every time
    save_ndarrays_as_npy(data, sat_image_save_path, preface=thermalPreface, date_tuples=slots)
    save_ndarrays_as_pngs(data, sat_image_save_path, preface=thermalPreface, date_tuples=slots)

    name = slots[0][0] + "_" + slots[len(slots)-1][1] + thermalPreface + '.png'

    # plot the data nicely
    plot_ndarrays(data, slots, farm_coords_wgs84, save_path=figure_save_path + name)

    ## Writing thermal data to csv

    write_data_to_csv(data, slots, csvpath)
    sort_csv_by_date(csvpath) # We do this here instead of in the write so its more efficient and can be moved
