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

To install you can start by cloning the repository

```shell
git clone https://github.com/AMcEnaney1/OceanSatelliteImages.git
```

Then using the provided environment.yml file

```shell
conda env create -f environment.yml
conda activate your-environment-name
```

To use the various models later on it will likely be required to install code
from additional places, such as Hygeos for the POLYMER algorithm code.


## Usage

Before running the code there are a few things that must be done:
* Your api keys must be entered into the 'keys.py' file or otherwise configured.
* the 'sat.py' file must be modified in several ways:
  * The coordinates list must be updated to include all the boundary boxes that
  are desired.
  * The projectName list must be updated to have a name for every bbox.
  * the createImages list must be updated to include a boolean value for each
  bbox/project.
  * The start, end and n_chunks variables must be changed to what is desired.

Once these are done you can simply run the main function in 'sat.py'.


