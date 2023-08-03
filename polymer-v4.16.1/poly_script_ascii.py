## Aidan McEnaney
## August 1st, 2023
## Script used to run the POLYMER algorithm

## Start of imports

from polymer_format_functions import *
from polymer.main import run_atm_corr, Level2
from polymer.level1_ascii import Level1_ASCII

## End of imports

## This script is meant to run POLYMER from a csv, errors will occur if using on other formats

def run_olci(dirname, square=None, blocksize=None, additional_headers=None, dir_smile=None,
             sensor=None, BANDS=None, TOAR=None, headers=None, relative_azimuth=None, wind_module=None, na_values=None,
             ozone_unit=None, datetime_fmt=None, verbose=None, sep=None, skiprows=None, datasets=None,
             multiprocessing=None, dir_base=None, calib=None, normalize=None):

    """
    dirname: This is a string representing the name of the csv file that the algorithm will be run on
    filetype: This is a boolean to choose what filetype the output is in. True = nc file, False = hdf file
    """

    ## Making sure passed variables are of the correct format

    if (not(dirname.endswith(".csv"))):
        print(f"Error, please enter a valid csv file for variable 'dirname'. Received: '{dirname}'")
        return

    ## Creating a dictionary of all the optional inputs

    # List of 'opt_input' and 'input' strings
    level1_input_strings = ['square', 'blocksize', 'additional_headers', 'dir_smile', 'sensor', 'BANDS', 'TOAR',
                            'headers', 'relative_azimuth', 'wind_module', 'na_values', 'ozone_unit', 'datetime_fmt',
                            'verbose', 'sep, skiprows']
    level1_input_variables = [square, blocksize, additional_headers, dir_smile, sensor, BANDS, TOAR, headers,
                            relative_azimuth, wind_module, na_values, ozone_unit, datetime_fmt, verbose, sep, skiprows]

    level2_input_strings = ['datasets']
    level2_input_variables = [datasets]

    run_opt_corr_input_strings = ['multiprocessing', 'dir_base', 'calib', 'normalize']
    run_opt_corr_input_variables = [multiprocessing, dir_base, calib, normalize]

    # Create a dictionary to collect the non-None arguments
    level1_args_dict = {opt: arg for opt, arg in zip(level1_input_strings, level1_input_variables) if arg is not None}
    level2_args_dict = {opt: arg for opt, arg in zip(level2_input_strings, level2_input_variables) if arg is not None}
    run_opt_corr_args_dict = {opt: arg for opt, arg in zip(run_opt_corr_input_strings, run_opt_corr_input_variables) if arg is not None}

    ## ## Calling run_atm_corr and unpacking the arguments using **args_dict

    run_atm_corr(Level1_ASCII(dirname, **level1_args_dict), Level2(**level2_args_dict), **run_opt_corr_args_dict)