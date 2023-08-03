## Aidan McEnaney
## June 30th, 2023
## Code for satellite image analysis

## Start of imports

import satFunctions
import plotFunctions
import requestFunctions
import models
import sentinelsatRequests
from configg import *
from globalVars import *
import os

## End of imports

def main():

    satFunctions.del_file('shell_input.txt')
    satFunctions.del_file('polymer_root_name.txt')

    # Check if sentinelHub config is configured properly
    if not config.sh_client_id or not config.sh_client_secret:
        print("Warning! To use Process API, please provide the credentials (OAuth client ID and client secret).")

    with open('polymer_root_name.txt', "w") as file:
        file.write(polymer_root_name + '/')  # Writing polymer root name to file for outside use

    for i in range(length):

        ## Below are various calls of the 'core()' function, this is what handles just about everything involving
        ## the sentinelHub API.
        ## The resolution is defined right before the call before being passed along with everything else.

        # Thermal Data

        resolution = 30  # Resolution for thermal images
        satFunctions.core(resolution, date_tuples, sat_image_save_path, operations_save_path[i], thermalPreface, farm_coords_wgs84[i],
                        figure_save_path, csvpath_thermal[i], operext, projectName[i],
                          request_function=requestFunctions.get_thermal_request, createImages= createImages[i])

        # Chlorophyll Data

        resolution = 100  # Resolution for chlorophyll images, actual res is 300, example of how it doesn't need to be exact
        satFunctions.core(resolution, date_tuples, sat_image_save_path, operations_save_path[i], chlorophyllPreface, farm_coords_wgs84[i],
                        figure_save_path, csvpath_chlorophyll[i], operext, projectName[i],
                          request_function=requestFunctions.get_chlorophyll_request, createImages= createImages[i])


        # Sediment Data

        resolution = 100  # Resolution for sediment images, actual res is 300,
        satFunctions.core(resolution, date_tuples, sat_image_save_path, operations_save_path[i], sedimentPreface,
                          farm_coords_wgs84[i],
                          figure_save_path, csvpath_sediment[i], operext, projectName[i],
                          request_function=requestFunctions.get_sediment_request, createImages=createImages[i])

        # Oxygen Absorption Data

        resolution = 100  # Resolution for oxygen images, actual res is 300,
        satFunctions.core(resolution, date_tuples, sat_image_save_path, operations_save_path[i], oxygenPreface,
                          farm_coords_wgs84[i],
                          figure_save_path, csvpath_oxygen[i], operext, projectName[i],
                          request_function=requestFunctions.get_oxygen_request, createImages=createImages[i])

        # A ton of stuff to get dissolved oxygen in water, from this paper: https://www.sciencedirect.com/science/article/pii/S2352938522000672

        resolution = 20  # Resolution for all bands from s2l2a images, actual res is 10 or 20,so I just went to the larger one
        satFunctions.core(resolution, date_tuples, sat_image_save_path, operations_save_path[i], oxygen2Preface[i],
                          farm_coords_wgs84[i],
                          figure_save_path, csvpath_oxygen2[i], operext, projectName[i],
                          request_function=requestFunctions.get_all_s2l2a_request, createImages=True)

        # A ton of stuff to get chlorophyll in water, from this paper: https://www.sciencedirect.com/science/article/pii/S1569843223000456#b0040

        resolution = 300  # Resolution for all bands from OLCI
        satFunctions.core(resolution, date_tuples, sat_image_save_path, operations_save_path[i], chlorophyll2Preface[i],
                          farm_coords_wgs84[i],
                          figure_save_path, csvpath_chlorophyll2[i], operext, projectName[i],
                          request_function=requestFunctions.get_chlor_algo_request, createImages=True)
        # How this chlorophyll band works:
        # https://sentinels.copernicus.eu/web/sentinel/technical-guides/sentinel-3-olci/level-2/oc4me-chlorophyll


        # Creating plots of data
        # This is where I am creating plots of data collected via the sentinelHub API.

        plotFunctions.plot_csv_data(csvpath_thermal[i], figure_save_path, 'Average', 'Average Temperature (Kelvin)',
                                    farm_coords_wgs84[i], 'Average Temperature vs. Time')
        plotFunctions.plot_csv_data(csvpath_thermal[i], figure_save_path, 'Average', 'Average Temperature (Fahrenheit)',
                                    farm_coords_wgs84[i], 'Average Temperature vs. Time', fah=True)
        plotFunctions.plot_csv_data(csvpath_chlorophyll[i], figure_save_path, 'Average',
                                    'Average Chlorophyll Concentration', farm_coords_wgs84[i],
                                    'Average Chlorophyll Concentration vs. Time')


        # Calling models and sentinelsat API here. It can take a while to get images from the sentinelsat API,
        # especially when they are in the long term archive.
        # Running the POLYMER algorithm is also extremely time-consuming, hence why this is done after everything else.

        # Calling the chlorophyll algorithm, this is also calling and running POLYMER.
        models.model_routine(farm_coords_wgs84[i], date_tuples, projectName[i], chlorPoly_save_path, models.chlor,
                             (poly_dir_app[i] + '/'), request_function=sentinelsatRequests.get_olci, npy_save_to=npy_save_to[i])


    # Deleting the files we made earlier
    satFunctions.del_file('conda_source_path.txt')
    satFunctions.del_file('polymer_root_name.txt')

if __name__ == "__main__":
    main()