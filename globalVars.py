## Aidan McEnaney
## July 25th, 2023
## Python file to set and store global variables

##################################################################################################################
# Here you change global variables as needed, most of these are just folder names or labels for files,
# However it is important to set stuff like coordinates, start/end time and n_chunks
# File and folder names need only be added if you are adding a new request
# You can simply define them here and then use them in the request call of main in sat.py
# If adding a new bulk request, make sure you create a for loop of the band number initializing the proper arrays
##################################################################################################################

## Start of imports

import satFunctions
import datetime
import os

## End of imports

## Start of General Global Variables

# List of coordinates/bounding boxes, one per farm location, works fine with N of these
coordinates = [(-69.9040, 43.8586, -69.8987, 43.8651)] # These will be turned into bounding boxes

# List of project names, one for each bounding box you have defined
projectName = ['MaxFarm'] # These will be prefixes in the relevant files

# These variables set the start and end dates for the data collection
start_year = 2021
end_year = 2023
start_month = 5
end_month = 5
start_day = 1
end_day = 30

# This is 1 more than the amount of data points you want to collect
n_chunks = 13

# List of boolean values, one per bounding box
createImages = [False] # If True, .npy and .png images will be created when making calls with SentinelHub

# This the name of the folder in which will serve as the root for downloaded data from SentinelHub
outputs_folder = 'out'

## End of General Global Variables


## Start of sentinelHub data file/folder names

# This is the file type that will be looked at when checking for what api calls have already been made
operext = '.npy'

# This is the suffix for your operations text file that each project will have, the prefix will be the project name.
operations_txt_suffix = '_oper'

# This is the name for the folder that csvs for data from SentinelHub will be stored
csv_path_folder_name = 'data'

# This is the suffix for the prefix of each csv's name, the prefix here is once again the project name
csv_path_folder_suffix = '_compData'

# This is the name that the created figures will be placed in
figure_path_folder_name = 'figures'

# This is the name for the folder used for general satellite data from sentinelHub
sat_image_folder_name = 'satData'

# This is the name of the folder where your images (.npy and .png) from sentinelHub will be stored
image_folder_name = 'images'

# This is the name for the folder used for the log file
log_file_folder_name = sat_image_folder_name

# This is the name of the folder that the log file will be called in, log is used to check previous api calls
log_folder_name = 'logs'

# This is the suffix for the thermal data cvs from sentinelHub
csv_path_thermal_suffix = '_Thermal'

# Used throughout the code and file names to keep track of thermal data from sentinelHub
thermalPreface = 'Thermal'

# This is the suffix for the chlorophyll data cvs from sentinelHub
csv_path_chlorophyll_suffix = '_Chlor'

# Used throughout the code and file names to keep track of chlorophyll data from sentinelHub
chlorophyllPreface = 'Chlor'

# This is the suffix for the sediment data cvs from sentinelHub
csv_path_sediment_suffix = '_Sed'

# Used throughout the code and file names to keep track of sediment data from sentinelHub
sedimentPreface = 'Sed'

# This is the suffix for the oxygen data cvs from sentinelHub
csv_path_oxygen_suffix = '_Oxy'

# Used throughout the code and file names to keep track of oxygen data from sentinelHub
oxygenPreface = 'Oxy'

# String used in the name of csvs for the bulk request of dissolved oxygen bands, and the preface as well
bulk_request_DO = 's2l2a'

# String used in the name of csvs for the bulk request of chlorophyll bands, and the preface as well
bulk_request_chloro = 'chlor_algo'

## End of sentinelHub data file/folder names


## Start of sentinelsat file/folder names

# This is the name of the root folder for polymer, you should likely only need to change the version
polymer_root_name = 'polymer-v4.16.1'

# Sets the folder that your chlorophyll data folder is located in, used for sentinelsat
chlorPoly_save_path1 = polymer_root_name

# This is the name of the folder where everything for the chlorophyll algorithm will take place
chlorPoly_folder_name = 'chlorPoly'

# This is the name of the folder for .npy files created from post-polymer nc files
npy_file_folder_name_suffix = '_poly_files'

## End of sentinelsat file/folder names


## Start of required computations

# Setting up start and end date as well as the amount of snapshots
start = datetime.datetime(start_year, start_month, start_day)
end = datetime.datetime(end_year, end_month, end_day)
date_tuples = satFunctions.get_timeslots(start, end, n_chunks)

figure_save_path = os.path.join(outputs_folder, figure_path_folder_name, '')
sat_image_save_path = os.path.join(outputs_folder, sat_image_folder_name, image_folder_name, '')
chlorPoly_save_path2 = os.path.join(chlorPoly_folder_name, '')
chlorPoly_save_path = os.path.join(chlorPoly_save_path1, chlorPoly_save_path2)

length = len(projectName)

# Doing this in multiple lines, so I can get them through bash later
operations_txt_filename = [None] * length
csvpath_base = [None] * length
operations_save_path = [None] * length
csvpath_thermal = [None] * length
csvpath_chlorophyll = [None] * length
csvpath_sediment = [None] * length
csvpath_oxygen = [None] * length
csvpath_oxygen2 = [[] for _ in range(length)]
oxygen2Preface = [[] for _ in range(length)]
csvpath_chlorophyll2 = [[] for _ in range(length)]
chlorophyll2Preface = [[] for _ in range(length)]

for i in range(length):
    operations_txt_filename[i] = projectName[i] + operations_txt_suffix + '.txt'
    csvpath_base[i] = os.path.join(outputs_folder, csv_path_folder_name, '') + projectName[i] + csv_path_folder_suffix
    operations_save_path[i] = os.path.join(outputs_folder, log_file_folder_name, log_folder_name, '') + operations_txt_filename[i]
    csvpath_thermal[i] = csvpath_base[i] + projectName[i] + csv_path_thermal_suffix + '.csv'
    csvpath_chlorophyll[i] = csvpath_base[i] + projectName[i] + csv_path_chlorophyll_suffix + '.csv'
    csvpath_sediment[i] = csvpath_base[i] + projectName[i] + csv_path_sediment_suffix + '.csv'
    csvpath_oxygen[i] = csvpath_base[i] + projectName[i] + csv_path_sediment_suffix + '.csv'

    # Bulk Requests Start

    for j in range(12):
        csvpath_oxygen2[i].append(csvpath_base[i] + projectName[i] + '_' + bulk_request_DO + str(j) + '.csv')
        oxygen2Preface[i].append(bulk_request_DO + str(j))

    for j in range(5):
        csvpath_chlorophyll2[i].append(csvpath_base[i] + projectName[i] + '_' + bulk_request_chloro + str(j) + '.csv')
        chlorophyll2Preface[i].append(bulk_request_chloro + str(j))

    # Bulk Requests End

    poly_dir = os.path.join(chlorPoly_save_path2, projectName[i])  # Needs to be moved, right now is reliant on stuff done in models.py
    npy_save_to = projectName[i] + npy_file_folder_name_suffix  # Sets folder name for where the npy files taken from polymer output go

    # Setting up farm coordinates
    farm_coords_wgs84 = coordinates[i]

## End of required computations