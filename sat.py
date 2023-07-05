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

    createImages = [False, False] # Set to True in order to create .npy and .png files of downloaded images.
                                        # Double check that it actually passed to the routine funcion if set to True

    projectName = ['MaxFarm','ME_Harbor'] # These will be prefixes in the relevant files
    coordinates = [(-69.9040, 43.8586, -69.8987, 43.8651), (-68.447721,44.146632,-68.444996,44.151682)]

    for i in range(len(projectName)):
        operext = '.npy'
        operations_txt_filename = projectName[i] + '_oper.txt'
        csvpath_base = 'out/data/' + projectName[i] + '_compData'
        csvpath_thermal =  csvpath_base + projectName[i] +'_Thermal.csv'
        csvpath_chlorophyll = csvpath_base + projectName[i] + '_Chlor.csv'
        figure_save_path = 'out/figures/'
        sat_image_save_path = 'out/satData/images/'
        operations_save_path = 'out/satData/logs/' + operations_txt_filename
        thermalPreface = 'Thermal'
        chlorophyllPreface = 'Chlor'

        ## End of setting variables ##

        if not config.sh_client_id or not config.sh_client_secret:
            print("Warning! To use Process API, please provide the credentials (OAuth client ID and client secret).")

        ## Setting up farm coordinates

        farm_coords_wgs84 = coordinates[i]

        # Setting up start and end date as well as the amount of snapshots
        start = datetime.datetime(2022, 1, 1)
        end = datetime.datetime(2022, 12, 31)
        n_chunks = 13
        date_tuples = satFunctions.get_timeslots(start, end, n_chunks)

        # Thermal Data

        resolution = 30  # Resolution for thermal images
        satFunctions.core(resolution, date_tuples, sat_image_save_path, operations_save_path, thermalPreface, farm_coords_wgs84,
                        figure_save_path, csvpath_thermal, operext, projectName[i], request_function=requestFunctions.get_thermal_request, createImages= createImages[i])

        # Chlorophyll Data

        resolution = 100  # Resolution for chlorophyll images, actual res is 300,
                                        # but we can't assume our bbox line up exactl, especially with such a small area
        satFunctions.core(resolution, date_tuples, sat_image_save_path, operations_save_path, chlorophyllPreface, farm_coords_wgs84,
                        figure_save_path, csvpath_chlorophyll, operext, projectName[i], request_function=requestFunctions.get_chlorophyll_request, createImages= createImages[i])


        # Creating plots of data

        plotFunctions.plot_csv_data(csvpath_thermal, figure_save_path, 'Average', 'Average Temperature (Celcius)', farm_coords_wgs84, 'Average Temperature vs. Time')
        plotFunctions.plot_csv_data(csvpath_chlorophyll, figure_save_path, 'Average', 'Average Chlorophyll Concentration', farm_coords_wgs84, 'Average Chlorophyll Concentration vs. Time')

        # How this chlorophyll band works:
                    # https://sentinels.copernicus.eu/web/sentinel/technical-guides/sentinel-3-olci/level-2/oc4me-chlorophyll


if __name__ == "__main__":
    main()