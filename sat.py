## Aidan McEnaney
## June 30th, 2023
## Code for satellite image analysis

## Imports

import satFunctions
import plotFunctions
import requestFunctions
import models
from configg import *
import datetime
import os

## End of Imports

def main():

    ## Setting variables ##

    #createImages = [False, False] # Set to True in order to create .npy and .png files of downloaded images.
                                        # Double check that it actually passed to the routine funcion if set to True

    #projectName = ['MaxFarm','ME_Harbor'] # These will be prefixes in the relevant files
    #coordinates = [(-69.9040, 43.8586, -69.8987, 43.8651), (-68.447721,44.146632,-68.444996,44.151682)]
    projectName = ['MaxFarm'] # These will be prefixes in the relevant files
    coordinates = [(-69.9040, 43.8586, -69.8987, 43.8651)]
    createImages = [False]
    outputs_folder = 'out'


    for i in range(len(projectName)):
        operext = '.npy'
        operations_txt_filename = projectName[i] + '_oper.txt'
        csvpath_base = os.path.join(outputs_folder, 'data', '') + projectName[i] + '_compData'
        figure_save_path = os.path.join(outputs_folder, 'figures', '')
        sat_image_save_path = os.path.join(outputs_folder, 'satData', 'images', '')
        operations_save_path = os.path.join(outputs_folder, 'satData', 'logs', '') + operations_txt_filename

        csvpath_thermal = csvpath_base + projectName[i] + '_Thermal.csv'
        thermalPreface = 'Thermal'
        csvpath_chlorophyll = csvpath_base + projectName[i] + '_Chlor.csv'
        chlorophyllPreface = 'Chlor'
        csvpath_sediment = csvpath_base + projectName[i] + '_Sed.csv'
        sedimentPreface = 'Sed'
        csvpath_oxygen = csvpath_base + projectName[i] + '_Oxy.csv'
        oxygenPreface = 'Oxy'

        csvpath_oxygen2 = []
        oxygen2Preface = []
        csvpath_chlorophyll2 = []
        chlorophyll2Preface = []

        for j in range(12): # Use for bulk requests only
            csvpath_oxygen2.append(csvpath_base + projectName[i] + '_' + 's2l2a' + str(j) + '.csv')
            oxygen2Preface.append('s2l2a' + str(j))

        for j in range(5):
            csvpath_chlorophyll2.append(csvpath_base + projectName[i] + '_' + 'chlor_algo' + str(j) + '.csv')
            chlorophyll2Preface.append('chlor_algo' + str(j))

        chlorPoly_save_path1 = 'polymer-v4.16.1'
        #chlorPoly_save_path2 = os.path.join(outputs_folder, 'chlorPoly', '')
        chlorPoly_save_path2 = os.path.join('chlorPoly', '')
        poly_dir = os.path.join(chlorPoly_save_path2, projectName[i]) # Needs to be moved, right now is reliant on stuff done in models.py
        chlorPoly_save_path = os.path.join(chlorPoly_save_path1, chlorPoly_save_path2)
        npy_save_to = projectName[i] + '_' + 'poly_files' # Sets folder name for where the npy files taken from polymer output go

        ## Setting up farm coordinates

        farm_coords_wgs84 = coordinates[i]

        # Setting up start and end date as well as the amount of snapshots
        start = datetime.datetime(2022, 7, 1)
        end = datetime.datetime(2023, 7, 30)
        n_chunks = 13
        date_tuples = satFunctions.get_timeslots(start, end, n_chunks)


        ## End of setting variables ##

        if not config.sh_client_id or not config.sh_client_secret:
            print("Warning! To use Process API, please provide the credentials (OAuth client ID and client secret).")

        # Thermal Data

        resolution = 30  # Resolution for thermal images
        satFunctions.core(resolution, date_tuples, sat_image_save_path, operations_save_path, thermalPreface, farm_coords_wgs84,
                        figure_save_path, csvpath_thermal, operext, projectName[i], request_function=requestFunctions.get_thermal_request, createImages= createImages[i])

        # Chlorophyll Data

        resolution = 100  # Resolution for chlorophyll images, actual res is 300,
                                        # but we can't assume our bbox line up exactly, especially with such a small area
        satFunctions.core(resolution, date_tuples, sat_image_save_path, operations_save_path, chlorophyllPreface, farm_coords_wgs84,
                        figure_save_path, csvpath_chlorophyll, operext, projectName[i], request_function=requestFunctions.get_chlorophyll_request, createImages= createImages[i])


        # Sediment Data

        resolution = 100  # Resolution for sediment images, actual res is 300,
        # but we can't assume our bbox line up exactly, especially with such a small area
        satFunctions.core(resolution, date_tuples, sat_image_save_path, operations_save_path, sedimentPreface,
                          farm_coords_wgs84,
                          figure_save_path, csvpath_sediment, operext, projectName[i],
                          request_function=requestFunctions.get_sediment_request, createImages=createImages[i])

        # Oxygen Absorption Data

        resolution = 100  # Resolution for oxygen images, actual res is 300,
        # but we can't assume our bbox line up exactly, especially with such a small area
        satFunctions.core(resolution, date_tuples, sat_image_save_path, operations_save_path, oxygenPreface,
                          farm_coords_wgs84,
                          figure_save_path, csvpath_oxygen, operext, projectName[i],
                          request_function=requestFunctions.get_oxygen_request, createImages=createImages[i])

        # A ton of stuff to get dissolved oxygen in water, from this paper: https://www.sciencedirect.com/science/article/pii/S2352938522000672

        resolution = 20  # Resolution for all bands from s2l2a images, actual res is 10 or 20,so I just went to the larger one
        satFunctions.core(resolution, date_tuples, sat_image_save_path, operations_save_path, oxygen2Preface,
                          farm_coords_wgs84,
                          figure_save_path, csvpath_oxygen2, operext, projectName[i],
                          request_function=requestFunctions.get_all_s2l2a_request, createImages=True)

        # A ton of stuff to get chlorophyll in water, from this paper: https://www.sciencedirect.com/science/article/pii/S1569843223000456#b0040

        resolution = 300  # Resolution for all bands from OLCI
        satFunctions.core(resolution, date_tuples, sat_image_save_path, operations_save_path, chlorophyll2Preface,
                          farm_coords_wgs84,
                          figure_save_path, csvpath_chlorophyll2, operext, projectName[i],
                          request_function=requestFunctions.get_chlor_algo_request, createImages=True)
        # How this chlorophyll band works:
        # https://sentinels.copernicus.eu/web/sentinel/technical-guides/sentinel-3-olci/level-2/oc4me-chlorophyll



        # Creating plots of data

        plotFunctions.plot_csv_data(csvpath_thermal, figure_save_path, 'Average', 'Average Temperature (Kelvin)',
                                    farm_coords_wgs84, 'Average Temperature vs. Time')
        plotFunctions.plot_csv_data(csvpath_thermal, figure_save_path, 'Average', 'Average Temperature (Fahrenheit)',
                                    farm_coords_wgs84, 'Average Temperature vs. Time', fah=True)
        plotFunctions.plot_csv_data(csvpath_chlorophyll, figure_save_path, 'Average',
                                    'Average Chlorophyll Concentration', farm_coords_wgs84,
                                    'Average Chlorophyll Concentration vs. Time')

        # Models, due to computation time models go  after api calls and figures are made

        models.chlor(farm_coords_wgs84, date_tuples, projectName[i], chlorPoly_save_path, npy_save_to=npy_save_to)

        with open('shell_input.txt', "w") as file:
            file.write(poly_dir) # Writing as a text file for bash script to use

def convert():
    with open('process_input.txt', 'r') as file:
        tmp_ = file.readline().strip()
        npy_save_to = file.readline().strip()

    satFunctions.del_file('shell_input.txt') # Deletes the file we just read from

    os.chdir(os.path.join(os.getcwd(), 'polymer-v4.16.1')) # Change directory to that of polymer

    tmp_ = satFunctions.remove_overlap(os.getcwd(), tmp_)

    satFunctions.move_files_by_type(os.getcwd(), tmp_, '.nc') # Moves the outputs from POLYMER

    filevals = satFunctions.get_surface_level_folders(tmp_) # Gets a list of the downloaded folders

    paths = satFunctions.find_files_with_strings(tmp_, filevals) # Get nc files output by POLYMER to convert to npy

    for path in paths: # Creates npy files for all the parts of each nc file
        satFunctions.convert_nc_to_npy(path, save_to=npy_save_to)

    models.chlorophyll(os.getcwd(), tmp_, npy_save_to) # Calls the chlorophyll model

if __name__ == "__main__":
    main()
    #convert()
