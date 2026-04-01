#!/bin/bash

# Create archive directory if it does not exist
if [ ! -d "archive" ]; then
    mkdir archive
fi

# Check if grades.csv exists
if [ ! -f "grades.csv" ]; then
    echo "Error: grades.csv not found."
    exit 1
fi

# Create timestamp
timestamp=$(date +"%Y%m%d-%H%M%S")

# Create new archived filename
new_filename="grades_$timestamp.csv"

# Move and rename the file into archive
mv grades.csv "archive/$new_filename"

# Create a new empty grades.csv file
touch grades.csv

# Log the action
echo "$timestamp | grades.csv | archive/$new_filename" >> organizer.log

echo "Archive completed successfully."