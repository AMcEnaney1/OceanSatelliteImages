#!/bin/bash

bash delete_files.sh

# Source conda, without this environment activation may not work
CONDA_PATH="/Users/aidan/mambaforge/etc/profile.d/conda.sh"
source "$CONDA_PATH"

# Write the conda source path to a text file
echo "$CONDA_PATH" > conda_source_path.txt

# Activate the Conda environment for sat.py
conda activate sent

# Call the Python script and the function using the `python3` command
python3 -c "import sat; sat.main()"

# Deactivate the Conda environment for sat.py
conda deactivate