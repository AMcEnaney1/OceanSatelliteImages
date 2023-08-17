#!/bin/bash
#
# File: run.sh
# Author: Aidan McEnaney
# Date: 2023-08-17
#
# Description: This is an example Bash script to run various tasks.
#
# Usage: ./run.sh <absolute_folder_path> [options]
#   Options:
#     -h, --help: Display this help message and exit.
#
# Dependencies: This script requires 'some_tool' to be installed.
#
# Notes:
#   - This script is distributed under the MIT License. See LICENSE.txt for details.

show_help() {
    echo "Usage: $0 <absolute_folder_path> [options]"
    echo "Options:"
    echo "  -h, --help: Display this help message and exit."
}

# Parse command-line options
while getopts ":h" opt; do
    case $opt in
        h)
            show_help
            exit 0
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            show_help
            exit 1
            ;;
    esac
done

# Shift the option arguments
shift "$((OPTIND - 1))"

# Check if the required absolute folder path argument is provided
if [ $# -eq 0 ]; then
    echo "Error: Absolute folder path is required."
    show_help
    exit 1
fi

# Get the absolute folder path argument
absolute_folder_path="$1"

# Get the package name and function name from user input
read -p "Enter the package name (e.g., 'examples'): " package_name
read -p "Enter the function name (e.g., 'example_for_script'): " file_name
read -p "Enter the function name (e.g., 'main'): " function_name


# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Build the path to conda_path.txt
CONDA_PATH_FILE="$SCRIPT_DIR/../text_files/conda_source_path.txt"

# Read the conda path from the text file
CONDA_PATH=$(<"$CONDA_PATH_FILE")

# Source conda using the read path
source "$CONDA_PATH"

# Activate the Conda environment for sat.py
conda activate sent

# Move to folder package folder is in
cd $absolute_folder_path

python3 -c "import $package_name.$file_name; $package_name.$file_name.$function_name()"

# Deactivate the Conda environment for sat.py
conda deactivate