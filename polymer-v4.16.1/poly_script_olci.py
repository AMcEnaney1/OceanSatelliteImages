#!/usr/bin/env python
# -*- coding: utf-8 -*-

## Aidan McEnaney
## August 1st, 2023
## Script used to run the POLYMER algorithm

## Start of imports

from polymer_format_functions import *
from polymer.main import run_atm_corr
from polymer.level2_nc import Level2_NETCDF
from polymer.level2_hdf import Level2_HDF
from polymer.level1_olci import Level1_OLCI
from polymer.ancillary import Ancillary_NASA
import sys

## End of imports

## This script is meant to run POLYMER on images from the OLCI satellite, errors will occur if using on other images

def run_polymer(dirname, filetype=True, sline=None, eline=None, scol=None, ecol=None, blocksize=None, ancillary=0,
             landmask=None, altitude=None, add_noise=None, filename = None, ext=None, tmpdir=None, outdir=None, overwrite=None,
             datasets=None, compress=None, format=None, multiprocessing=None, dir_base=None, calib=None, normalize=None):

    """
    dirname: This is a string representing the name of the '.Sen3' folder algorithm will be run on
    filetype: This is a boolean to choose what filetype the output is in. True = nc file, False = hdf file
    """

    if (ancillary == 0):
        ancillary = Ancillary_NASA()
    else:
        ancillary=None

    ## Making sure passed variables are of the correct format

    if (not(dirname.endswith(".SEN3"))):
        print(f"Error, please enter a valid Sentinel3 directory for variable 'dirname'. Received: '{dirname}'")
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
    level1_input_strings = ['sline', 'eline', 'scol', 'ecol', 'blocksize', 'ancillary', 'landmask', 'altitude', 'add_noise']
    level1_input_variables = [sline, eline, scol, ecol, blocksize, ancillary, landmask, altitude, add_noise]

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
        run_atm_corr(Level1_OLCI(dirname, **level1_args_dict), Level2_NETCDF(**level2_args_dict),
                     **run_opt_corr_args_dict)
    elif (filetype == False):
        run_atm_corr(Level1_OLCI(dirname, **level1_args_dict), Level2_HDF(**level2_args_dict),
                     **run_opt_corr_args_dict)

if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "run_polymer":
        dirname = sys.argv[2]
        #filetype = sys.argv[3].lower() == "true"
        filetype = bool(sys.argv[sys.argv.index("--filetype") + 1]) if "--filetype" in sys.argv else None
        sline = int(sys.argv[sys.argv.index("--sline") + 1]) if "--sline" in sys.argv else None
        eline = int(sys.argv[sys.argv.index("--eline") + 1]) if "--eline" in sys.argv else None
        scol = int(sys.argv[sys.argv.index("--scol") + 1]) if "--scol" in sys.argv else None
        ecol = int(sys.argv[sys.argv.index("--ecol") + 1]) if "--ecol" in sys.argv else None
        blocksize = int(sys.argv[sys.argv.index("--blocksize") + 1]) if "--blocksize" in sys.argv else None
        ancillary = int(sys.argv[sys.argv.index("--ancillary") + 1]) if "--ancillary" in sys.argv else None
        landmask = sys.argv[sys.argv.index("--landmask") + 1] if "--landmask" in sys.argv else None
        altitude = float(sys.argv[sys.argv.index("--altitude") + 1]) if "--altitude" in sys.argv else None
        add_noise = bool(sys.argv[sys.argv.index("--add_noise") + 1]) if "--add_noise" in sys.argv else None
        filename = sys.argv[sys.argv.index("--filename") + 1] if "--filename" in sys.argv else None
        ext = sys.argv[sys.argv.index("--ext") + 1] if "--ext" in sys.argv else None
        tmpdir = sys.argv[sys.argv.index("--tmpdir") + 1] if "--tmpdir" in sys.argv else None
        outdir = sys.argv[sys.argv.index("--outdir") + 1] if "--outdir" in sys.argv else None
        overwrite = bool(sys.argv[sys.argv.index("--overwrite") + 1]) if "--overwrite" in sys.argv else None
        datasets = list(sys.argv[sys.argv.index("--datasets") + 1]) if "--datasets" in sys.argv else None
        compress = bool(sys.argv[sys.argv.index("--compress") + 1]) if "--compress" in sys.argv else None
        format = sys.argv[sys.argv.index("--format") + 1] if "--format" in sys.argv else None
        multiprocessing = int(
            sys.argv[sys.argv.index("--multiprocessing") + 1]) if "--multiprocessing" in sys.argv else None
        dir_base = sys.argv[sys.argv.index("--dir_base") + 1] if "--dir_base" in sys.argv else None
        calib = dict(sys.argv[sys.argv.index("--calib") + 1]) if "--calib" in sys.argv else None
        normalize = int(sys.argv[sys.argv.index("--normalize") + 1]) if "--normalize" in sys.argv else None

        run_polymer(dirname, filetype, sline=sline, eline=eline, scol=scol, ecol=ecol, blocksize=blocksize,
                    ancillary=ancillary, landmask=landmask, altitude=altitude, add_noise=add_noise,
                    filename=filename, ext=ext, tmpdir=tmpdir, outdir=outdir, overwrite=overwrite,
                    datasets=datasets, compress=compress, format=format, multiprocessing=multiprocessing,
                    dir_base=dir_base, calib=calib, normalize=normalize)