#!/bin/bash

# Activate the Conda environment for sat.py
source /Users/aidan/mambaforge/etc/profile.d/conda.sh
conda activate sent

# Call the Python script and the function using the `python3` command
python3 sat.py -c "main()"

poly_dir=$(cat "shell_input.txt")
rm shell_input.txt

echo "Passed folder: $poly_dir"

# Add '/' character to the end of poly_dir
poly_dir+="/"

# Deactivate the Conda environment for sat.py
conda deactivate

pol_dir="polymer-v4.16.1/"
cd "$pol_dir"

pwd

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

conda activate sent

python3 sat.py -c "convert()"

conda deactivate