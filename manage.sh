#!/bin/bash


# Activate the Conda environment for sat.py
source /Users/aidan/mambaforge/etc/profile.d/conda.sh
conda activate sent

# Run main() in sat.py and store the returned directory in a variable
poly_dir=$(python3 -c 'from sat import main; print(main())')

# Add '/' character to the end of poly_dir
poly_dir+="/"

# Deactivate the Conda environment for sat.py
conda deactivate

pol_dir="polymer-v4.16.1/"
cd "$pol_dir"

# Check if the folder doesn't already exist
if [ ! -d "$poly_dir" ]; then
    # If the folder doesn't exist, create it
    mkdir "$poly_dir"
    echo "Folder '$poly_dir' created successfully!"
else
    echo "Folder '$poly_dir' already exists. Skipping folder creation."
fi

# Move into the polymer directory
#cd "$poly_dir"

pwd

conda activate sentPoly

# Loop through all subdirectories (input folders) in poly_dir
find "$poly_dir" -type d -print0 | while IFS= read -r -d '' input_folder; do
  # Trim the trailing slash from the folder name to get the basename
  input_folder_name=$(basename "$input_folder")

  # Output file name with .nc extension
  output_file="$input_folder_name.nc"

  # Call polymer_cli.py script from /polymer-v4.16.1 directory with input folder and output file as arguments
  ./polymer_cli.py "$input_folder" "$output_file"
done

conda deactivate


