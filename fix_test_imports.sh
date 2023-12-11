#!/bin/bash

# Check if a directory is provided as a command-line argument
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

# Get the directory from the command-line argument
directory="$1"

import_lines='\nimport sys\nimport os\n\nsys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))\n'

# Iterate through each Python file in the specified directory
for file in "$directory"/*.py; do
    # Check if the file exists and is a regular file
    if [ -f "$file" ]; then
        # Use grep to find if file has docstring
        line_number=$(grep -n -e "'''" -e '"""' "$file" | awk -F ':' 'NR==2 {print $1}')

        if [ -n "$line_number" ]; then
            # Insert the after the docstring
            sed -i "$line_number a\\$import_lines" "$file"
        elif [ -n "$(grep -n -e "'''" -e '"""' "$file" | awk -F ':' 'NR==1 {print $1}')" ]; then
            first_occurrence_line=$(grep -n -e "'''" -e '"""' "$file" | awk -F ':' 'NR==1 {print $1}')
            # Insert the after the docstring
            sed -i "$first_occurrence_line a\\$import_lines" "$file"
        else
            # Insert the lines after the shebang
            sed -i "1 a\\$import_lines" "$file"
        fi
        echo "Fixed imports for $file"
    fi
done
