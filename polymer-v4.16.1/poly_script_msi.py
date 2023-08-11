## Aidan McEnaney
## August 1st, 2023
## Script used to run the POLYMER algorithm

## Start of imports

from polymer_format_functions import *
from polymer.main import run_atm_corr
from polymer.level2_nc import Level2_NETCDF
from polymer.level2_hdf import Level2_HDF
from polymer.level1_msi import Level1_MSI
from polymer.ancillary import Ancillary_NASA
import sys

## End of imports

## This script is meant to run POLYMER on images from MSI, errors will occur if using on other images

def run_polymer(dirname, filetype=True, sline=None, eline=None, scol=None, ecol=None, blocksize=None, resolution=None,
             ancillary=None, landmask=None, altitude=None, add_noise=None, srf_file=None, use_srf=None, filename = None,
             ext=None, tmpdir=None, outdir=None, overwrite=None, datasets=None, compress=None, format=None,
             multiprocessing=None, dir_base=None, calib=None, normalize=None):
    """
    Run the POLYMER algorithm on a given directory.

    Args:
        dirname (str): Directory name containing input data for POLYMER.
        filetype (bool): If True, output is .nc file; if False, .hdf file. Default is True.
        sline (int): Start line for data processing. Default is 0.
        eline (int): End line for data processing. Default is -1.
        scol (int): Start column for data processing. Default is 0.
        ecol (int): End column for data processing. Default is -1.
        blocksize (int): Block size for processing. Default is 198.
        resolution (str): Resolution of data, either '60', '20' or '10' (in m). Default is '60'.
        ancillary (object): An ancillary data instance (Ancillary_NASA, Ancillary_ERA). Default is None.
        landmask (Union[str, None, GSW object]): Landmask information. Can be a string, None, or a GSW object.
            Default is None.
        altitude (Union[float, DEM object]): Altitude parameter. Can be a float, or a DEM object.
            Default is 0.
        add_noise (bool):
            Whether to add simulated noise to the radiance data. When set to True,
            random noise is added to the radiance values to simulate measurement
            uncertainty or sensor noise.
            Default is None.
        srf_file (str): Spectral response function.
            By default, it will use:
                auxdata/msi/S2-SRF_COPE-GSEG-EOPG-TN-15-0007_3.0_S2A.csv for S2A
                auxdata/msi/S2-SRF_COPE-GSEG-EOPG-TN-15-0007_3.0_S2B.csv for S2B
            Default is None.
        use_srf (bool): Whether to calculate the bands central wavelengths from the SRF or to use fixed ones.
            Default is True.
        filename (str):
            Output filename. If None, determine filename from level1 by using output directory.
            Default is None.
        ext (str): Output file extension. Default is '.nc'.
        tmpdir (str): Path of temporary directory. Default is None.
        outdir (str): Output directory. Default is None.
        overwrite (bool): Overwrite existing file. Default is False.
        datasets (list): List of datasets to include in level 2. Default is None.
        compress (bool): Activate compression. Default is True.
        format (str):
            Underlying file format as specified in netcdf's Dataset:
                one of 'NETCDF4', 'NETCDF4_CLASSIC', 'NETCDF3_CLASSIC' or 'NETCDF3_64BIT'
            Default is 'NETCDF4_CLASSIC'.
        multiprocessing (int):
            Number of threads to use for processing
                - 0: Single thread (multiprocessing disactivated)
                - 1 or greater: Use as many threads as there are CPUs on local machine
            Default is 0.
        dir_base (str): Location of base directory to locate auxiliary data. Default is 'ANCILLARY/METEO'.
        calib (dict):
            A dictionary for applying calibration coefficients.
            Default is None.
        normalize (int):
            Select water reflectance normalization:
                - 0: No geometry nor wavelength normalization
                - 1: Apply normalization of the water reflectance at nadir-nadir
                - 2: Apply wavelength normalization for MERIS and OLCI
                - 3: Apply both geometry and wavelength normalization
            Default is None.

    Returns:
        None
    """

    if (ancillary == 0):
        ancillary = Ancillary_NASA()
    else:
        ancillary=None

    ## Making sure passed variables are of the correct format

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
    level1_input_strings = ['sline', 'eline', 'scol', 'ecol', 'blocksize', 'resolution', 'ancillary', 'landmask',
                            'altitude', 'add_noise', 'srf_file', 'use_srf']
    level1_input_variables = [sline, eline, scol, ecol, blocksize, resolution, ancillary, landmask, altitude,
                              add_noise, srf_file, use_srf]

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
        run_atm_corr(Level1_MSI(dirname, **level1_args_dict), Level2_NETCDF(**level2_args_dict),
                     **run_opt_corr_args_dict)
    elif (filetype == False):
        run_atm_corr(Level1_MSI(dirname, **level1_args_dict), Level2_HDF(**level2_args_dict),
                     **run_opt_corr_args_dict)

if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "run_polymer":
        dirname = sys.argv[2]
        filetype = bool(sys.argv[sys.argv.index("--filetype") + 1]) if "--filetype" in sys.argv else None
        sline = int(sys.argv[sys.argv.index("--sline") + 1]) if "--sline" in sys.argv else None
        eline = int(sys.argv[sys.argv.index("--eline") + 1]) if "--eline" in sys.argv else None
        scol = int(sys.argv[sys.argv.index("--scol") + 1]) if "--scol" in sys.argv else None
        ecol = int(sys.argv[sys.argv.index("--ecol") + 1]) if "--ecol" in sys.argv else None
        blocksize = int(sys.argv[sys.argv.index("--blocksize") + 1]) if "--blocksize" in sys.argv else None
        resolution = int(sys.argv[sys.argv.index("--resolution") + 1]) if "--resolution" in sys.argv else None
        ancillary = int(sys.argv[sys.argv.index("--ancillary") + 1]) if "--ancillary" in sys.argv else None
        landmask = sys.argv[sys.argv.index("--landmask") + 1] if "--landmask" in sys.argv else None
        altitude = float(sys.argv[sys.argv.index("--altitude") + 1]) if "--altitude" in sys.argv else None
        add_noise = bool(sys.argv[sys.argv.index("--add_noise") + 1]) if "--add_noise" in sys.argv else None
        srf_file = bool(sys.argv[sys.argv.index("--srf_file") + 1]) if "--srf_file" in sys.argv else None
        use_srf = bool(sys.argv[sys.argv.index("--use_srf") + 1]) if "--use_srf" in sys.argv else None
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
                    resolution=resolution, ancillary=ancillary, landmask=landmask, altitude=altitude,
                    add_noise=add_noise, srf_file=srf_file, use_srf=use_srf, filename=filename, ext=ext, tmpdir=tmpdir,
                    outdir=outdir, overwrite=overwrite, datasets=datasets, compress=compress, format=format,
                    multiprocessing=multiprocessing, dir_base=dir_base, calib=calib, normalize=normalize)