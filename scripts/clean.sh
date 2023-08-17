#!/bin/bash

# Function to delete files recursively in a folder
delete_files_in_folder() {
    local folder="$1"
    if [ -d "$folder" ]; then
        find "$folder" -type f -exec rm -f {} +
    fi
}

# Check if a folder is provided as an argument
if [ $# -eq 0 ]; then
    echo "Usage: $0 <folder_path>"
    exit 1
fi

# Get the absolute path of the provided folder
folder_path=$(realpath "$1")

# Check if the provided folder exists
if [ ! -d "$folder_path" ]; then
    echo "Error: The specified folder does not exist."
    exit 1
fi

# Confirm with the user before proceeding
read -p "Are you sure you want to delete all files in \"$folder_path\" and its subfolders? (y/n): " confirm
if [[ $confirm =~ ^[Yy]$ ]]; then
    # Call the function to delete files in the specified folder
    delete_files_in_folder "$folder_path"
    echo "All files in \"$folder_path\" and its subfolders have been deleted."
else
    echo "Operation canceled."
fi
