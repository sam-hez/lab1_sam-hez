#!/bin/bash

# Create archive directory if it does not exist
if [ ! -d "archive" ]; then
    mkdir archive
fi

# Check if grades.csv exists
if [ ! -f "grades.csv" ]; then
    echo "Error: grades.csv does not exist."
    exit 1
fi

# Generate timestamp
timestamp=$(date +"%Y%m%d-%H%M%S")

# Create archived filename
new_filename="grades_${timestamp}.csv"

# Move and rename the file into archive
mv grades.csv "archive/$new_filename"

# Create a new empty grades.csv
touch grades.csv

# Log the action
echo "$timestamp | original: grades.csv | archived as: archive/$new_filename" >> organizer.log

echo "Archive completed successfully."
echo "Moved grades.csv to archive/$new_filename"
echo "Created new empty grades.csv"