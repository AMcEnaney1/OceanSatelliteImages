#!/bin/bash

# Source conda, without this environment activation may not work
source /Users/aidan/mambaforge/etc/profile.d/conda.sh

# Activate the Conda environment for sat.py
conda activate sent

# Call the Python script and the function using the `python3` command
python3 -c "import sat; sat.main()"

# Deactivate the Conda environment for sat.py
conda deactivate