## Aidan McEnaney
## August 1st, 2023
## Script used to run the POLYMER algorithm

## Start of imports

from polymer_format_functions import *
from polymer.main import run_atm_corr, Level1, Level2
from polymer.level2_nc import Level2_NETCDF
from polymer.level1_olci import Level1_OLCI

## End of imports

## This script is meant to run POLYMER on images from the OLCI satellite, errors will occur if using on other images

def run_olci(dirname, filename, sline=None, eline=None, scol=None, ecol=None, blocksize=None, ancillary=None,
             landmask=None, altitude=None, add_noise=None, ext=None, tmpdir=None, outdir=None, overwrite=None,
             datasets=None, compress=None, format=None, multiprocessing=None, dir_base=None, calib=None, normalize=None):

    ## Making sure all passed variables are of the correct format

    if (isinstance(outdir, str) and outdir is not None): # Checks if output folder passed
        output_folder = ensure_start_end_chars(outdir, '/') # Makes sure folder starts and ends with '/' character


    ## Creating a dictionary of all the optional inputs

    # List of 'opt_input' strings
    level1_input_strings = ['sline', 'eline', 'scol', 'ecol', 'blocksize', 'ancillary', 'landmask', 'altitude', 'add_noise']
    level2_input_strings = ['ext', 'tmpdir', 'outdir', 'overwrite', 'datasets', 'compress', 'format']
    run_opt_corr_input_strings = ['multiprocessing', 'dir_base', 'calib', 'normalize']

    # List of 'input' variable names
    level1_input_variables = [sline, eline, scol, ecol, blocksize, ancillary, landmask, altitude, add_noise]
    level2_input_variables = [ext, tmpdir, outdir, overwrite, datasets, compress, format]
    run_opt_corr_input_variables = [multiprocessing, dir_base, calib, normalize, datasets]

    # Create a dictionary to collect the non-None arguments
    level1_args_dict = {opt: arg for opt, arg in zip(level1_input_strings, level1_input_variables) if arg is not None}
    level2_args_dict = {opt: arg for opt, arg in zip(level2_input_strings, level2_input_variables) if arg is not None}
    run_opt_corr_args_dict = {opt: arg for opt, arg in zip(run_opt_corr_input_strings, run_opt_corr_input_variables) if arg is not None}

    # Call run_atm_corr and unpack the arguments using **args_dict
    run_atm_corr(Level1_OLCI(**level1_args_dict), Level2_NETCDF(**level2_args_dict), **run_opt_corr_args_dict)