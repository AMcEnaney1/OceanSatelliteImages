#!/bin/bash

# Bash script to call POLYMER via 'polymer_cli.py'

# Source conda, without this environment activation may not work
source /Users/aidan/mambaforge/etc/profile.d/conda.sh

# Read in contents of file and save as variable
poly_dir=$(cat "shell_input.txt")
pol_dir=$(cat "polymer_root_name.txt")

cd "$pol_dir" # Move over to the polymer root directory

# Function to get the deepest folder name with '.nc' attached
get_output_file_name() {
    local path="$1"
    local deepest_folder=$(basename "$path")
    echo "${deepest_folder}.nc"
}

conda activate sentPoly

for folder in $poly_dir*; do
    folder_name=$(basename "$folder")  # Get the folder name from the path
    output_file_name=$(get_output_file_name "$folder_name")
    folder_name="${poly_dir}${folder_name}"
    echo "Processing folder: $folder_name"
    ./polymer_cli.py "$folder_name" "$output_file_name" # Execute the script with folder name and output file name
done
conda deactivate