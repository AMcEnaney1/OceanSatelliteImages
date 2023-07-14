## Aidan McEnaney
## June 30th, 2023
## Functions used in the satellite image analysis code


## Imports

from polymer.main import run_atm_corr, Level1, Level2
from polymer.level1_olci import Level1_OLCI
from polymer.level2_nc import Level2_NETCDF
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
from netCDF4 import Dataset

## End of Imports

def create_folder(path, folder_name):
    # Combine the path and folder name
    folder_path = os.path.join(path, folder_name)

    # Check if the folder already exists
    if not os.path.exists(folder_path):
        # Create the folder
        os.makedirs(folder_path)
        print(f"Folder '{folder_name}' created at '{folder_path}'")
    else:
        print(f"Folder '{folder_name}' already exists at '{folder_path}'")


def chlor_algorithm_apply(path, preface="image", date_tuples=None, project_name='name', folder_name = 'sen', folder_name_out = 'tmp'):
    tmp = folder_name_out

    for i in range(len(preface)):
        for j in range(len(date_tuples)):

            folder_name_out = str(date_tuples[j]) + '_' + preface[i] + '_' + project_name + '_' + tmp
            folder_name_in = str(date_tuples[j]) + '_' + preface[i] + '_' + project_name + '_' + folder_name
            create_folder(path, folder_name_out)

            # Apply POLYMER
            run_atm_corr(
                Level1_OLCI(
                    folder_name_in[i],
                    sline=9000, eline=10000),
                Level2_NETCDF(outdir=os.path.join(path, folder_name_out))
            )

            # Now we make the outputted .nc file into a .npy with the chlorophyll model applied

            output_nc = load_npy_file(folder_name_out + 'output.nc')


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

def convert_nc_to_npy(nc_path, download_path):
    # Open the netCDF file
    nc_file = Dataset(nc_path, 'r')

    # Get the variable
    nc_var = nc_file.variables['data']

    # Read the variable data
    np_array = np.array(nc_var[:])

    # Save the data as .npy file
    np.save(download_path, np_array)

    # Close the netCDF file
    nc_file.close()

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

    # Now we create a text file with the data we have so we don't waste api calls if we are just filling data
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
        create_blank_file(operations_save_path) # Create operation log file if it doesn't already exist

    if (not (type(preface) is list)):
        preface = [preface]
        csvpath = [csvpath]

    for i in range(len(preface)):
        # Creating csv
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
