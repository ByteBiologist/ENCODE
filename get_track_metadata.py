#!/usr/bin/env python3

"""
Script to extract ENCODE track metadata from JSON files.

Date_added in this refers to Individual track (bigBed files) release date; Release date column in GADB metadata.

Json files are pre-downloaded.
"""

import os
import json
import sys

def extract_info(file):
    with open(file, 'r') as f:
        data = json.load(f)
        submitted_file_name = data.get("submitted_file_name", "")
        name = os.path.basename(submitted_file_name)
        date = data.get("date_created", "").split("T")[0]
        return os.path.splitext(os.path.basename(file))[0], name, date

def main(directory):
    output_file = "bigBed_track_metadata.txt"
    with open(output_file, 'w') as out_f:
        for file in os.listdir(directory):
            if file.endswith('.json'):
                file_path = os.path.join(directory, file)
                file_base, name, date = extract_info(file_path)
                out_f.write(f"{file_base}\tSubmitted_track_name={name}\tRelease_date={date}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    main(directory)

