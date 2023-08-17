"""
File: polymer_functions.py
Author: Aidan McEnaney
Date: 2023-08-11

Description: This module contains the functions that interface with POLYMER.

Contents:

    - call_polymer: Function to run polymer on a singular folder.

Notes:
    - This code is distributed under the MIT License. See LICENSE.txt for more details.
"""

# Standard library imports
import os
import subprocess

# Third-party library imports


# Local module imports
import utils.misc_functions as mf
from config import *

def run_polymer_on_folder(poly_dir, satellite_type=0, filetype=True, sline=None, eline=None, scol=None, ecol=None,
                          blocksize=None, resolution=None, ancillary=0, landmask=None, altitude=None, add_noise=None,
                          srf_file=None, use_srf=None, filename=None, ext=None, tmpdir=None, outdir=None, overwrite=None,
                          datasets=None, compress=None, format=None, multiprocessing=None, dir_base=None, calib=None,
                          normalize=None):
    """
    Calls the POLYMER algorithm on an entire folder of snapshots by calling a bash script in a subprocess that
    then calls a python script, which parses arguments before finally passing them to POLYMER.

    Args:
        poly_dir (str): Directory containing folders with snapshots for POLYMER processing.
        satellite_type (int): Select the satellite that the data came from:
                - 0: OLCI
                - 1: MSI
            Default is 0.
        filetype (bool): If True, output is .nc file; if False, .hdf file. Default is True.
        sline (int): Start line for data processing. Default is None.
        eline (int): End line for data processing. Default is None.
        scol (int): Start column for data processing. Default is None.
        ecol (int): End column for data processing. Default is None.
        blocksize (int): Block size for processing. Default is None.
        resolution (str): Resolution of data, either '60', '20' or '10' (in m). Default is None.
        ancillary (int): Ancillary data option. If 0, use NASA data; if None, no ancillary data. Default is 0.
        landmask (Union[str, None, GSW object]): Landmask information. Can be a string, None, or a GSW object.
            Default is None.
        altitude (Union[float, DEM object]): Altitude parameter. Can be a float, or a DEM object.
            Default is None.
        add_noise (bool):
            Whether to add simulated noise to the radiance data. When set to True,
            random noise is added to the radiance values to simulate measurement
            uncertainty or sensor noise.
            Default is None.
        srf_file (str): Spectral response function. By default, it will use:
            auxdata/msi/S2-SRF_COPE-GSEG-EOPG-TN-15-0007_3.0_S2A.csv for S2A
            auxdata/msi/S2-SRF_COPE-GSEG-EOPG-TN-15-0007_3.0_S2B.csv for S2B
        use_srf (bool): Whether to calculate the bands central wavelengths from the SRF or to use fixed ones.
            Default is None.
        filename (str):
            Output filename. If None, determine filename from level1 by using output directory.
            Default is None.
        ext (str): Output file extension, such as '.nc'. Default is None.
        tmpdir (str): Path of temporary directory. Default is None.
        outdir (str): Output directory. Default is None.
        overwrite (bool): Overwrite existing file. Default is None.
        datasets (list): List of datasets to include in level 2. Default is None.
        compress (bool): Activate compression. Default is None.
        format (str):
            Underlying file format as specified in netcdf's Dataset:
                one of 'NETCDF4', 'NETCDF4_CLASSIC', 'NETCDF3_CLASSIC' or 'NETCDF3_64BIT'
            Default is None.
        multiprocessing (int):
            Number of threads to use for processing
                - 0: Single thread (multiprocessing disactivated)
                - 1 or greater: Use as many threads as there are CPUs on local machine
            Default is None.
        dir_base (str): Location of base directory to locate auxiliary data. Default is None, will use
            'ANCILLARY/METEO'.
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

    for folder in os.listdir(poly_dir):
        folder_path = os.path.join(poly_dir, folder)
        if os.path.isdir(folder_path):
            folder_name = os.path.basename(folder_path)
            folder_name = os.path.join(poly_dir, folder_name)

            call_polymer(folder_name, filetype=filetype, sline=sline, eline=eline, scol=scol, ecol=ecol, blocksize=blocksize,
                            ancillary=ancillary, landmask=landmask, altitude=altitude, add_noise=add_noise, filename=filename,
                            ext=ext, tmpdir=tmpdir, outdir=outdir, overwrite=overwrite, datasets=datasets, compress=compress,
                            format=format, multiprocessing=multiprocessing, dir_base=dir_base, calib=calib, normalize=normalize)


def call_polymer(dirname, satellite_type=0, filetype=True, sline=None, eline=None, scol=None, ecol=None,
                          blocksize=None, resolution=None, ancillary=0, landmask=None, altitude=None, add_noise=None,
                          srf_file=None, use_srf=None, filename=None, ext=None, tmpdir=None, outdir=None, overwrite=None,
                          datasets=None, compress=None, format=None, multiprocessing=None, dir_base=None, calib=None,
                          normalize=None):
    """
    Calls the POLYMER algorithm on a single snapshot using subprocess.

    Args:
        dirname (str): Directory name containing input data for POLYMER.
        satellite_type (int): Select the satellite that the data came from:
                - 0: OLCI
                - 1: MSI
            Default is 0.
        filetype (bool): If True, output is .nc file; if False, .hdf file. Default is True.
        sline (int): Start line for data processing. Default is None.
        eline (int): End line for data processing. Default is None.
        scol (int): Start column for data processing. Default is None.
        ecol (int): End column for data processing. Default is None.
        blocksize (int): Block size for processing. Default is None.
        resolution (str): Resolution of data, either '60', '20' or '10' (in m). Default is None.
        ancillary (int): Ancillary data option. If 0, use NASA data; if None, no ancillary data. Default is 0.
        landmask (Union[str, None, GSW object]): Landmask information. Can be a string, None, or a GSW object.
            Default is None.
        altitude (Union[float, DEM object]): Altitude parameter. Can be a float, or a DEM object.
            Default is None.
        add_noise (bool):
            Whether to add simulated noise to the radiance data. When set to True,
            random noise is added to the radiance values to simulate measurement
            uncertainty or sensor noise.
            Default is None.
        srf_file (str): Spectral response function. By default, it will use:
            auxdata/msi/S2-SRF_COPE-GSEG-EOPG-TN-15-0007_3.0_S2A.csv for S2A
            auxdata/msi/S2-SRF_COPE-GSEG-EOPG-TN-15-0007_3.0_S2B.csv for S2B
        use_srf (bool): Whether to calculate the bands central wavelengths from the SRF or to use fixed ones.
            Default is None.
        filename (str):
            Output filename. If None, determine filename from level1 by using output directory.
            Default is None.
        ext (str): Output file extension, such as '.nc'. Default is None.
        tmpdir (str): Path of temporary directory. Default is None.
        outdir (str): Output directory. Default is None.
        overwrite (bool): Overwrite existing file. Default is None.
        datasets (list): List of datasets to include in level 2. Default is None.
        compress (bool): Activate compression. Default is None.
        format (str):
            Underlying file format as specified in netcdf's Dataset:
                one of 'NETCDF4', 'NETCDF4_CLASSIC', 'NETCDF3_CLASSIC' or 'NETCDF3_64BIT'
            Default is None.
        multiprocessing (int):
            Number of threads to use for processing
                - 0: Single thread (multiprocessing disactivated)
                - 1 or greater: Use as many threads as there are CPUs on local machine
            Default is None.
        dir_base (str): Location of base directory to locate auxiliary data. Default is None, will use
            'ANCILLARY/METEO'.
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

    file_path = os.path.join(project_root_path, script_path)

    if (satellite_type == 0):
        command = os.path.join(file_path, 'run_polymer.sh')
        args = [command, "run_polymer", dirname] # Initialize with required arguments
    elif (satellite_type == 1):
        command = os.path.join(file_path, 'run_polymer_msi.sh')
        args = [command, "run_polymer", dirname]  # Initialize with required arguments

    # Append optional arguments only if they are not None
    if filetype is not None:
        args.extend(["--filetype", str(filetype)])
    if sline is not None:
        args.extend(["--sline", str(sline)])
    if eline is not None:
        args.extend(["--eline", str(eline)])
    if scol is not None:
        args.extend(["--scol", str(scol)])
    if ecol is not None:
        args.extend(["--ecol", str(ecol)])
    if blocksize is not None:
        args.extend(["--blocksize", str(blocksize)])
    if resolution is not None:
        args.extend(["--resolution", str(resolution)])
    if ancillary is not None:
        args.extend(["--ancillary", str(ancillary)])
    if landmask is not None:
        args.extend(["--landmask", landmask])
    if altitude is not None:
        args.extend(["--altitude", str(altitude)])
    if add_noise is not None:
        args.extend(["--add_noise", str(add_noise)])
    if srf_file is not None:
        args.extend(["--srf_file", str(srf_file)])
    if use_srf is not None:
        args.extend(["--use_srf", str(use_srf)])
    if filename is not None:
        args.extend(["--filename", filename])
    if ext is not None:
        args.extend(["--ext", ext])
    if tmpdir is not None:
        args.extend(["--tmpdir", tmpdir])
    if outdir is not None:
        args.extend(["--outdir", outdir])
    if overwrite is not None:
        args.extend(["--overwrite", str(overwrite)])
    if datasets is not None:
        args.extend(["--datasets", datasets])
    if compress is not None:
        args.extend(["--compress", str(compress)])
    if format is not None:
        args.extend(["--format", format])
    if multiprocessing is not None:
        args.extend(["--multiprocessing", str(multiprocessing)])
    if dir_base is not None:
        args.extend(["--dir_base", dir_base])
    if calib is not None:
        args.extend(["--calib", calib])
    if normalize is not None:
        args.extend(["--normalize", str(normalize)])

    try:
        subprocess.run(args, check=True) # Calls script
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")