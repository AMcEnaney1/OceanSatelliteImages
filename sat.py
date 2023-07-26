## Aidan McEnaney
## June 30th, 2023
## Code for satellite image analysis

## Start of imports

import satFunctions
import plotFunctions
import requestFunctions
import models
from configg import *
from globalVars import *
import os

## End of imports

def main():

    if not config.sh_client_id or not config.sh_client_secret:
        print("Warning! To use Process API, please provide the credentials (OAuth client ID and client secret).")

    for i in range(length):

        # Thermal Data

        resolution = 30  # Resolution for thermal images
        satFunctions.core(resolution, date_tuples, sat_image_save_path, operations_save_path[i], thermalPreface, farm_coords_wgs84,
                        figure_save_path, csvpath_thermal[i], operext, projectName[i], request_function=requestFunctions.get_thermal_request, createImages= createImages[i])

        # Chlorophyll Data

        resolution = 100  # Resolution for chlorophyll images, actual res is 300,
                                        # but we can't assume our bbox line up exactly, especially with such a small area
        satFunctions.core(resolution, date_tuples, sat_image_save_path, operations_save_path[i], chlorophyllPreface, farm_coords_wgs84,
                        figure_save_path, csvpath_chlorophyll[i], operext, projectName[i], request_function=requestFunctions.get_chlorophyll_request, createImages= createImages[i])


        # Sediment Data

        resolution = 100  # Resolution for sediment images, actual res is 300,
        # but we can't assume our bbox line up exactly, especially with such a small area
        satFunctions.core(resolution, date_tuples, sat_image_save_path, operations_save_path[i], sedimentPreface,
                          farm_coords_wgs84,
                          figure_save_path, csvpath_sediment[i], operext, projectName[i],
                          request_function=requestFunctions.get_sediment_request, createImages=createImages[i])

        # Oxygen Absorption Data

        resolution = 100  # Resolution for oxygen images, actual res is 300,
        # but we can't assume our bbox line up exactly, especially with such a small area
        satFunctions.core(resolution, date_tuples, sat_image_save_path, operations_save_path[i], oxygenPreface,
                          farm_coords_wgs84,
                          figure_save_path, csvpath_oxygen[i], operext, projectName[i],
                          request_function=requestFunctions.get_oxygen_request, createImages=createImages[i])

        # A ton of stuff to get dissolved oxygen in water, from this paper: https://www.sciencedirect.com/science/article/pii/S2352938522000672

        resolution = 20  # Resolution for all bands from s2l2a images, actual res is 10 or 20,so I just went to the larger one
        satFunctions.core(resolution, date_tuples, sat_image_save_path, operations_save_path[i], oxygen2Preface[i],
                          farm_coords_wgs84,
                          figure_save_path, csvpath_oxygen2[i], operext, projectName[i],
                          request_function=requestFunctions.get_all_s2l2a_request, createImages=True)

        # A ton of stuff to get chlorophyll in water, from this paper: https://www.sciencedirect.com/science/article/pii/S1569843223000456#b0040

        resolution = 300  # Resolution for all bands from OLCI
        satFunctions.core(resolution, date_tuples, sat_image_save_path, operations_save_path[i], chlorophyll2Preface[i],
                          farm_coords_wgs84,
                          figure_save_path, csvpath_chlorophyll2[i], operext, projectName[i],
                          request_function=requestFunctions.get_chlor_algo_request, createImages=True)
        # How this chlorophyll band works:
        # https://sentinels.copernicus.eu/web/sentinel/technical-guides/sentinel-3-olci/level-2/oc4me-chlorophyll

        # Creating plots of data

        plotFunctions.plot_csv_data(csvpath_thermal[i], figure_save_path, 'Average', 'Average Temperature (Kelvin)',
                                    farm_coords_wgs84, 'Average Temperature vs. Time')
        plotFunctions.plot_csv_data(csvpath_thermal[i], figure_save_path, 'Average', 'Average Temperature (Fahrenheit)',
                                    farm_coords_wgs84, 'Average Temperature vs. Time', fah=True)
        plotFunctions.plot_csv_data(csvpath_chlorophyll[i], figure_save_path, 'Average',
                                    'Average Chlorophyll Concentration', farm_coords_wgs84,
                                    'Average Chlorophyll Concentration vs. Time')

        # Models, due to computation time models go  after api calls and figures are made

        with open('shell_input.txt', "w") as file:
            file.write(poly_dir) # Writing as a text file for bash script to use

        models.chlor(farm_coords_wgs84, date_tuples, projectName[i], chlorPoly_save_path, npy_save_to=npy_save_to)

        satFunctions.del_file('shell_input.txt')  # Deletes the file we made earlier


if __name__ == "__main__":
    main()
