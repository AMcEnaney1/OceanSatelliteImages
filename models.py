## Aidan McEnaney
## July 12th, 2023
## Code for various models used to get parameters

## Imports

from polymer.main import run_atm_corr, Level1, Level2
from polymer.level1_olci import Level1_OLCI
from polymer.level2_nc import Level2_NETCDF
import satFunctions
import os

## End of Imports

def chlor_algorithm_apply(path, preface="image", date_tuples=None, project_name='name', folder_name = 'sen', folder_name_out = 'tmp'):
    tmp = folder_name_out

    for i in range(len(preface)):
        for j in range(len(date_tuples)):

            folder_name_out = str(date_tuples[j]) + '_' + preface[i] + '_' + project_name + '_' + tmp
            folder_name_in = str(date_tuples[j]) + '_' + preface[i] + '_' + project_name + '_' + folder_name
            satFunctions.create_folder(path, folder_name_out)

            # Apply POLYMER
            run_atm_corr(
                Level1_OLCI(
                    folder_name_in[i],
                    sline=9000, eline=10000),
                Level2_NETCDF(outdir=os.path.join(path, folder_name_out))
            )

            # Now we make the outputted .nc file into a .npy with the chlorophyll model applied

            output_nc = satFunctions.load_npy_file(folder_name_out + 'output.nc')


def RemoteReflectance():
    # Atmospheric Correction algorithm
    # Calculates water reflectance, used to get chlorophyll-a. This is the POLYMER algorithm.
    # This algorithm came from here: https://opg.optica.org/oe/fulltext.cfm?uri=oe-19-10-9783&id=213648
    # And was used to get chlorophyll-a in this paper: https://www.sciencedirect.com/science/article/pii/S1569843223000456#b0190



    return 0

def chlorophyll(arr):
    # Algorithm to get chlorophyll-a, from this paper:
    # https://www.sciencedirect.com/science/article/pii/S1569843223000456#b0040

    # Defining regression coefficients
    B0 = 0.761
    B1 = 0.3495
    B2 = -1.512
    B3 = 1.925
    B4 = -9.0585
    B5 = 8.4015


    ### Needs to be finished

    # Defining reflectance values
    R1 = RemoteReflectance()
    R2 = RemoteReflectance()
    R3 = RemoteReflectance()
    R4 = RemoteReflectance()
    R5 = RemoteReflectance()

    val = B0 + (B1 * R1) + (B2 * R2) + (B3 * R3) + (B4 * R4) + (B5 * R5)

    return val