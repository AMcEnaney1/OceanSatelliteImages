#!/bin/bash

# List of bash script files to modify
script_files=(
    "delete_files.sh"
    "clean.sh"
    "run.sh"
    "run_polymer.sh"
    "polymer-v4.16.1/poly_script_olci.py"
    "polymer-v4.16.1/poly_script_ascii.py"
    "polymer-v4.16.1/poly_script_meris.py"
    "polymer-v4.16.1/poly_script_msi.py"
    # Add more paths as needed
)

# Function to set the permissions on the script files
set_permissions() {
    local script_path=$1
    local permission=$2

    if [ -f "$script_path" ]; then
        chmod "$permission" "$script_path"
        echo "Changed permissions of $script_path to $permission"
    else
        echo "Error: File not found - $script_path"
    fi
}

# Loop through the script_files array and set the desired permissions (replace '755' with your desired permission)
for script_file in "${script_files[@]}"; do
    set_permissions "$script_file" "755"
done
