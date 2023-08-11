#!/bin/bash

# Bash script to call POLYMER via 'polymer_cli.py'

# Read the conda source path from the text file and remove leading/trailing whitespaces and newlines
CONDA_SOURCE_PATH=$(<conda_source_path.txt)

# Using 'echo' and 'tr' to remove newlines
CONDA_SOURCE_PATH=$(echo "$CONDA_SOURCE_PATH" | tr -d '[:space:]')

# Source the conda script from the specified path
source "$CONDA_SOURCE_PATH"

pol_dir=$(cat "polymer_root_name.txt")

cd "$pol_dir" # Move over to the polymer root directory

echo "Arguments: $@"

conda activate sentPoly # Activate environment for polymer

./poly_script_msi.py "$@"

conda deactivate