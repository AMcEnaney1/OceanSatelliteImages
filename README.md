# Satellite Shellfish Modeling

---

Downloads and analyzes data from satellite images, for use in creating a 
shellfish growth model.

---

## Table of Contents

---

- [About](#about)
- [Installation](#installation)
- [Usage](#usage)
- [TODO](#todo)

---

## 1. About

---

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

---

## 2. Installation

---

### 2.1 My Code

To install you can start by cloning the repository

```shell
git clone https://github.com/AMcEnaney1/OceanSatelliteImages.git
```

Then using the provided environment.yaml file

```shell
conda env create -f environment.yaml
conda activate your-environment-name
```

### 2.2 POLYMER

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

As of v4.16.1 it is also necessary to make the changes outlined in this 
[forum post](https://forum.hygeos.com/viewtopic.php?f=7&t=218).

---

## 3. Usage

---

### 3.1 First Run

#### 3.1.1 API Keys

API keys must be entered into the 'keys.py' file or otherwise configured. 
For SentinelHub information on API keys can be found [here](https://docs.sentinel-hub.com/api/latest/api/overview/authentication/)
and for Sentinelsat your API the keys are your username and password used 
[here](https://scihub.copernicus.eu/dhus/#/home).

#### 3.1.2 API Config

After setting your API keys you can set up the API confifgs in 'configg.py'.
If you are not using one of the APIs you need to comment out the lines 
containing its config, if you have added an API you can add its config here,
and if you have changed any variable names in 'keys.py' you need to make
the change here as well.

#### 3.1.3 Global Variables

All the variables subject to change that are needed for the regular
function of the code are contained in 'GlobalVars.py' and can be set there.
This includes farm bounding boxes and names, time frames, data points, and
folder/file names, as well as several others. If you wish to get the bands
already specified in 'sat.py' you only need change bounding box locations, 
farm names, start and end time and the number of data points.

### 3.2 Running

There are two ways to run the code as of now, with bash script or through
the main function in sat.py. They are almost identical right now, however 
arguments will be able to passed to the bash script in the future.

#### 3.2.1 Bash Script

To run the bash script, 'manage.sh' first make sure your bash environment
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
chmod +x run_polymer.sh
./manage.sh
```

### 3.3 Following Runs

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

### 3.4 Modifying requests

#### 3.4.1 Adding SentinelHub requests

As is this code allows for both individual and bulk requests of satellite
bands from all [supported satellites](https://docs.sentinel-hub.com/api/latest/data/).

If you are adding a request of a singular band you need to first add an
evalscript to the 'evalscripts.py' file, then add the corresponding
request function to the 'requestFunctions.py' file. Once you have done
this you can define the relevant file and folder paths in 'globalVars.py',
these would be a string representing the preface and a string representing
a suffix for the related csv files. Then move down to the computations
section and set up a csv path using the current paths as examples. You
are now ready to call this request in the main function of 'sat.py'.

If you are adding a request of multiple bands you can do the same steps
as done for the singular band, only this time when moving to the computations
section be sure to create a new for loop as directed at the top of 
'globalVars.py'.

#### 3.4.2 Removing SentinelHub requests

To remove requests you can just remove the code calling them from
the main function in 'sat.py'.

#### 3.4.3 Adding Sentinelsat requests

This is currently not as easy as adding SentinelHub requests, however, can 
still be done. To do so you can create a function in 'models.py' similar to
'chlor()' before calling it through the 'model_routine()' function in
'sat.py''.

#### 3.4.3 Removing Sentinelsat requests

See above.

---

## TODO

---

### POLYMER

* Need to get Ancillary data.
* Need to call POLYMER's 'run_atm_corr()' directly in python script instead
of calling 'polymer_cli.py'.

### Models (Not all Possible)

* POM (Particulate Organic Matter)
* POC (Particulate Organic Carbon)
* Ocean Salinity
* Dissolved Oxygen
* Aerial Exposure (fraction of days exposed to air)
* TPM (Total Particulate Mass)
* PIM (Particulate Inorganic Mass)

---
