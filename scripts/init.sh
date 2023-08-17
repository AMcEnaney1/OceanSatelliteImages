#!/bin/bash

# Check if the user provided a project directory as an argument
if [ $# -ne 1 ]; then
    echo "Usage: $0 <project_directory>"
    exit 1
fi

project_directory="$1"

# Check if the provided project directory exists
if [ ! -d "$project_directory" ]; then
    echo "Error: Project directory '$project_directory' not found."
    exit 1
fi

# Function to set permissions for .py and .sh files recursively
set_permissions_recursive() {
    for file in "$1"/*; do
        if [ -d "$file" ]; then
            set_permissions_recursive "$file"
        elif [ -f "$file" ]; then
            if [[ "$file" == *.py || "$file" == *.sh ]]; then
                chmod +x "$file"
            fi
        fi
    done
}

# Change to the project directory
cd "$project_directory" || exit 1

# Start setting permissions from the current directory
set_permissions_recursive .

# Prompt the user for the Conda file path
read -p "Enter the Conda file path (e.g., '/Users/aidan/mambaforge/etc/profile.d/conda.sh'): " conda_file_path

# Determine the path for the text file
text_file_path="$project_directory/text_files/conda_source_path.txt"

# Check if the Conda file path is not the same as the content of the text file
if [ "$(cat "$text_file_path")" != "$conda_file_path" ]; then
    echo "$conda_file_path" > "$text_file_path"
    echo "Conda file path saved to '$text_file_path'."
else
    echo "Conda file path is already up to date."
fi

echo "Permissions set for .py and .sh files in all folders and subfolders of '$project_directory'."