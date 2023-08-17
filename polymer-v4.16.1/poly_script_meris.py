## Aidan McEnaney
## August 1st, 2023
## Script used to run the POLYMER algorithm

## Start of imports

from polymer_format_functions import *
from polymer.main import run_atm_corr
from polymer.level2_nc import Level2_NETCDF
from polymer.level2_hdf import Level2_HDF
from polymer.level1_meris import Level1_MERIS

## End of imports

## This script is meant to run POLYMER on images from MERIS, errors will occur if using on other images

def run_polymer(dirname, filetype=True, sline=None, eline=None, scol=None, ecol=None, blocksize=None, dir_smile=None,
             ancillary=None, landmask=None, altitude=None, filename = None, ext=None, tmpdir=None, outdir=None,
             overwrite=None, datasets=None, compress=None, format=None, multiprocessing=None, dir_base=None, calib=None,
             normalize=None):

    """
    dirname: This is a string representing the name of the '.N1' folder algorithm will be run on
    filetype: This is a boolean to choose what filetype the output is in. True = nc file, False = hdf file
    """

    ## Making sure passed variables are of the correct format

    if (not (dirname.endswith(".N1"))):
        print(f"Error, please enter a valid MERIS directory for variable 'dirname'. Received: '{dirname}'")
        return

    if(not (filetype == True or filetype == False)):
        print(f"Error, please enter a valid boolean value for 'filetype' variable. Received: '{filetype}'")
        return

    if ((not isinstance(sline, int)) and sline is not None):
        print(f"Error, 'sline' not an integer, attempting to cast.")
        sline = try_cast_to_int(sline)
        if (sline == False):
            print(f"Error, please enter a valid integer for 'sline' variable. Received: '{sline}'")
            return

    if ((not isinstance(eline, int)) and eline is not None):
        print(f"Error, 'eline' not an integer, attempting to cast.")
        eline = try_cast_to_int(eline)
        if (eline == False):
            print(f"Error, please enter a valid integer for 'eline' variable. Received: '{eline}'")
            return

    if (isinstance(outdir, str) and outdir is not None): # Checks if output folder passed
        outdir = ensure_end_char(outdir, '/') # Makes sure folder starts and ends with '/' character


    ## Creating a dictionary of all the optional inputs

    # List of 'opt_input' and 'input' strings
    level1_input_strings = ['sline', 'eline', 'scol', 'ecol', 'blocksize', 'ancillary', 'landmask', 'altitude', 'dir_smile']
    level1_input_variables = [sline, eline, scol, ecol, blocksize, ancillary, landmask, altitude, dir_smile]

    if (filetype == False): # The hdf class doesn't take a format variable
        level2_input_strings = ['filename', 'ext', 'tmpdir', 'outdir', 'overwrite', 'datasets', 'compress']
        level2_input_variables = [filename, ext, tmpdir, outdir, overwrite, datasets, compress]
    else:
        level2_input_strings = ['filename', 'ext', 'tmpdir', 'outdir', 'overwrite', 'datasets', 'compress', 'format']
        level2_input_variables = [filename, ext, tmpdir, outdir, overwrite, datasets, compress, format]

    run_opt_corr_input_strings = ['multiprocessing', 'dir_base', 'calib', 'normalize']
    run_opt_corr_input_variables = [multiprocessing, dir_base, calib, normalize]

    # Create a dictionary to collect the non-None arguments
    level1_args_dict = {opt: arg for opt, arg in zip(level1_input_strings, level1_input_variables) if arg is not None}
    level2_args_dict = {opt: arg for opt, arg in zip(level2_input_strings, level2_input_variables) if arg is not None}
    run_opt_corr_args_dict = {opt: arg for opt, arg in zip(run_opt_corr_input_strings, run_opt_corr_input_variables) if arg is not None}

    ## Calling run_atm_corr and unpacking the arguments using **args_dict

    if (filetype == True):
        run_atm_corr(Level1_MERIS(dirname, **level1_args_dict), Level2_NETCDF(**level2_args_dict),
                     **run_opt_corr_args_dict)
    elif (filetype == False):
        run_atm_corr(Level1_MERIS(dirname, **level1_args_dict), Level2_HDF(**level2_args_dict),
                     **run_opt_corr_args_dict)