# Satellite Shellfish Modeling

Downloads and analyzes data from satellite images, for use in creating a 
shellfish growth model.

## Table of Contents

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
- [TODO](#todo)

## About

As of now this code allows the user to specify N bounding boxes and a time 
range, and then satellite images over that time range and over the specified 
bounding boxes are downloaded and some statistics generated before being 
saved to a csv. Code exists to create plots of data as well. Eventually this 
code will contain several models from various papers that serve to get 
useful data for the modeling of shellfish growth.

This uses both the SentinelHub and the Sentinelsat API, the prior of which
is paid and the former of which is free. As of now the SentinelHub API is
the one primarily used and the Sentinelsat API is just used for bands for
which we want to apply POLYMER. However, I will work to move more over to
the free service, so users have the option. Note that using Sentinelsat
exclusively will increase runtime substantially, due to the long term 
archive causing wait times for data requests more than a few months old.


## Installation

### My Code

To install you can start by cloning the repository

```shell
git clone https://github.com/AMcEnaney1/OceanSatelliteImages.git
```

Then using the provided environment.yaml file

```shell
conda env create -f environment.yaml
conda activate your-environment-name
```

### POLYMER

The POLYMER algorithm called be downloaded from 
[Hygeos](https://www.hygeos.com/polymer), after making an account and 
accessing the forum. Once downloaded, unzip the downloaded folder and move
the contained polymer folder into the directory of this project and merge
the conda environments. Then to make the files navigate back to the polymer
directory and run the following commands:

```shell
make auxdata_all
make
```

Then, as above create the conda environment included with POLYMER.

## Usage

### Bash Script

To run the bash script, 'manage.py' first make sure your bash environment
is set up to run conda commands, do this with the following command: (This
may not work, in which case I suggest using mamba.)

```shell
conda init
```

Then go into the bash script and change the conda environment names to 
their actual names. You then need to give permission to the bash script
and run it:

```shell
chmod +x manage.sh
./manage.sh
```

### First Run

Before running the code there are a few things that must be done:
* Your API keys must be entered into the 'keys.py' file or otherwise 
configured.
* API config info must be added or removed from 'configg.py', depending on
your usage.
* the 'sat.py' file must be modified in several ways:
  * The coordinates list must be updated to include all the boundary boxes that
  are desired.
  * The projectName list must be updated to have a name for every bbox.
  * the createImages list must be updated to include a boolean value for each
  bbox/project.
  * The start, end and n_chunks variables must be changed to what is desired.

Once these are done you can simply run the main function in 'sat.py' or,
if using models run using the bash script, 'manage.sh'.

### Following Runs

The program is written in such a way such that for subsequent runs of
the code, after the first, so long as the log file remains needless
api calls will not be made. What this means is if for example you 
accidentally entered the wrong end date the code could simply be run
again with the end date moved back, though you may want to delete 
generated figures first. If you do not want this behavior simply
delete the log file. To delete all the output data you can run:
```shell
chmod +x clean.sh
./clean.sh out/
```
where here 'out' is root folder for our outputs from the SentinelHub API.
The same can be done for your outputs from the Sentinelsat API.

### Modifying requests

If you wish to request new or different bands than what is currently set
you can add an evalscript to the 'evalscripts.py' file and then add a new 
request to the 'requestFunctions.py' file. Once this is done make sure to
add or remove paths set in 'sat.py' as you need before setting the
resolution and adding the function call. 

## TODO

### POLYMER

* Need to get Ancillary data.

### Models (Not all Possible)

* POM (Particulate Organic Matter)
* POC (Particulate Organic Carbon)
* Ocean Salinity
* Dissolved Oxygen
* Aerial Exposure (fraction of days exposed to air)
* TPM (Total Particulate Mass)
* PIM (Particulate Inorganic Mass)

### Cleanup

* Move all inputs to one python file.
* Clean up io operations in bash script. (Can just read from new inputs.py)
* Create more bash scripts for various uses.
* Fix chlorPoly path, currently dependent on code in models.py, this should not be the case.
* Fix convert_nc_to_npy() so that save folders don't have to be exclusively deeper.
* Make script to run POLYMER aside from included polymer_cli.py
* remove_overlap() needs to be changed so order is fixed for any length,
not just length 1 or 2.
