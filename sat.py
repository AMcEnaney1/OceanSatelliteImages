## Aidan McEnaney
## June 30th, 2023
## Code for satellite image analysis


## Imports

import satFunctions
import plotFunctions
import requestFunctions
from configg import *
import datetime

## End of Imports

def main():

    ## Setting variables ##

    createImages = False # Set to True in order to create .npy and .png files of downloaded images.
                                        # Double check that it actually passed to the routine funcion if set to True

    operext = '.npy'
    operations_txt_filename = 'oper.txt'
    csvpath_base = 'out/data/compData'
    csvpath_thermal =  csvpath_base + '_Thermal.csv'
    csvpath_chlorophyll = csvpath_base + '_Chlor.csv'
    figure_save_path = 'out/figures/'
    sat_image_save_path = 'out/satData/images/'
    operations_save_path = 'out/satData/logs/' + operations_txt_filename
    thermalPreface = 'Thermal'
    chlorophyllPreface = 'Chlor'

    ## End of setting variables ##

    if not config.sh_client_id or not config.sh_client_secret:
        print("Warning! To use Process API, please provide the credentials (OAuth client ID and client secret).")

    ## Setting up farm coordinates
    farm_coords_wgs84 = (-69.9040, 43.8586, -69.8987, 43.8651) # Coordinates for the farm

    # Setting up start and end date as well as the amount of snapshots
    start = datetime.datetime(2017, 1, 1)
    end = datetime.datetime(2022, 12, 31)
    n_chunks = 121
    date_tuples = satFunctions.get_timeslots(start, end, n_chunks)

    # Creating operation logging text file

    satFunctions.create_blank_file(operations_save_path)

    # Thermal Data

    resolution = 30  # Resolution for thermal images
    satFunctions.core(resolution, date_tuples, sat_image_save_path, operations_save_path, thermalPreface, farm_coords_wgs84,
                    figure_save_path, csvpath_thermal, operext, request_function=requestFunctions.get_thermal_request)

    # Chlorophyll Data

    resolution = 100  # Resolution for chlorophyll images, actual res is 300,
                                    # but we can't assume our bbox line up exactl, especially with such a small area
    satFunctions.core(resolution, date_tuples, sat_image_save_path, operations_save_path, chlorophyllPreface, farm_coords_wgs84,
                    figure_save_path, csvpath_chlorophyll, operext, request_function=requestFunctions.get_chlorophyll_request)


    # Creating plots of data

    plotFunctions.plot_csv_data(csvpath_thermal, figure_save_path, 'Average')
    plotFunctions.plot_csv_data(csvpath_chlorophyll, figure_save_path, 'Average')


if __name__ == "__main__":
    main()