"""
File: config.py
Author: Aidan McEnaney
Date: 2023-08-14

Description: Config file for the project.

Notes:
    - This code is distributed under the MIT License. See LICENSE.txt for more details.
"""

import os
import pathlib


project_root_path = pathlib.Path(__file__).parent.resolve()
polymer_path = os.path.join(project_root_path, 'polymer-v4.16.1')
script_path = 'scripts'
conda_source_path = "/Users/aidan/mambaforge/etc/profile.d/conda.sh"

file_path = os.path.join(project_root_path, 'text_files', 'project_directory.txt')
if not os.path.exists(file_path): # Writing polymer root name to file for outside use
    with open(file_path, "w") as file:
        file.write(polymer_path + '/')
        print("File 'project_directory.txt' created and data written.")

file_path = os.path.join(project_root_path, 'text_files', 'polymer_root_name.txt')
if not os.path.exists(file_path): # Writing polymer root name to file for outside use
    with open(file_path, "w") as file:
        file.write(polymer_path + '/')
        print("File 'polymer_root_name.txt' created and data written.")

file_path = os.path.join(project_root_path, 'text_files', 'conda_source_path.txt')
if not os.path.exists(file_path): # Writing polymer root name to file for outside use
    with open(file_path, "w") as file:
        file.write(conda_source_path)
        print("File 'conda_source_path.txt' created and data written.")