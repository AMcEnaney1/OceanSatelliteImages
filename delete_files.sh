#!/bin/bash

# List of text files to delete
files=("conda_source_path.txt" "polymer_root_name.txt")

for file in "${files[@]}"; do
  if [ -e "$file" ]; then
    rm "$file"
    echo "Deleted $file"
  else
    echo "$file does not exist. Skipping..."
  fi
done
