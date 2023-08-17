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

echo "Permissions set for .py and .sh files in all folders and subfolders of '$project_directory'."
