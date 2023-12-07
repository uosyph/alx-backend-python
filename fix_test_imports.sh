#!/bin/bash

# Check if a directory is provided as a command-line argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# Get the directory from the command-line argument
directory="$1"

# Iterate through each Python file in the specified directory
for file in "$directory"/*.py; do
    # Check if the file exists and is a regular file
    if [ -f "$file" ]; then
        # Insert the lines after the first line in the file
        sed -i '1 a\
\
import sys\
import os\
\
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))\
' "$file"
        echo "Fixed imports for $file"
    fi
done
