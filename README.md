# Satellite Shellfish Modeling

Downloads and analyzes data from satellite images, for use in creating a 
shellfish growth model.

## Table of Contents

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)

## About

As of now this code allows the user to specify N bounding boxes and a time 
range, and then satellite images over that time range and over the specified 
bounding boxes are downloaded and some statistics generated before being 
saved to a csv. Code exists to create plots of data as well. Eventually this 
code will contain several models from various papers that serve to get 
useful data for the modeling of shellfish growth.

## Installation

### My Code

To install you can start by cloning the repository

```shell
git clone https://github.com/AMcEnaney1/OceanSatelliteImages.git
```

Then using the provided environment.yml file

```shell
conda env create -f environment.yml
conda activate your-environment-name
```

### POLYMER

The POLYMER algorithm called be downloaded from 
[Hygeos](https://www.hygeos.com/polymer). Once downloaded move the 
polymer folder into the directory of this project and merge the 
conda environments. Then to make the files navigate back to the polymer 
directory and run the following commands:

```shell
make auxdata_all
make
```

Then, as above create the conda environment included with POLYMER.

## Usage

### Bash Script

To run the bash script, 'manage.py' first make sure your bash environment
is set up to run conda commands, do this with the following command:

```shell
conda init
```

Then go into the bash script and change the conda environment names to 
their actual names. You then need to give permission to the bash script
and run it:

```shell
chmod +x manage.sh
./manage.py
```

### First Run

Before running the code there are a few things that must be done:
* Your api keys must be entered into the 'keys.py' file or otherwise configured.
* the 'sat.py' file must be modified in several ways:
  * The coordinates list must be updated to include all the boundary boxes that
  are desired.
  * The projectName list must be updated to have a name for every bbox.
  * the createImages list must be updated to include a boolean value for each
  bbox/project.
  * The start, end and n_chunks variables must be changed to what is desired.

Once these are done you can simply run the main function in 'sat.py', or
if using models run using the bash script.

### Following Runs

The program is written in such a way such that for subsequent runs of
the code, after the first, so long as the log file remains needless
api calls will not be made. What this means is if for example you 
accidentally entered the wrong end date the code could simply be run
again with the end date moved back, though you may want to delete 
generated figures first. If you do not want this behavior simply
delete the log file.

### Modifying requests

If you wish to request new or different bands than what is currently set
you can add an evalscript to the 'evalscripts.py' file and then add a new 
request to the 'requestFunctions.py' file. Once this is done make sure to
add or remove paths set in 'sat.py' as you need before setting the
resolution and adding the function call. 
