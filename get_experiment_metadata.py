#!/usr/bin/env python3

"""
Script to extract ENCODE experiments metadata from JSON files.

Json files are pre-downloaded.

Use the 'Experiment accession' in the metadata to map Experiments to individual tracks
"""

import os
import json
import sys

def extract_info(file):
    with open(file, 'r') as f:
        data = json.load(f)
        lab = data.get("lab", {}).get("title", "")
        bio = data.get("biosample_summary", "")
        system = ",".join(data.get("biosample_ontology", {}).get("system_slims", []))
        life_stage_ages = ",".join([control.get("life_stage_age", "") for control in data.get("possible_controls", [])])
        return lab, bio, system, life_stage_ages

def main(directory):
    output_file = "experiment_metadata.txt"
    with open(output_file, 'w') as out_f:
        for file in os.listdir(directory):
            if file.endswith('.json'):
                file_path = os.path.join(directory, file)
                lab, bio, system, life_stage_ages = extract_info(file_path)

                # Process file name to remove extension
                file_base = os.path.splitext(file)[0]

                # Constructing key-value pairs for the second column
                key_value_pairs = ""
                if bio:
                    key_value_pairs += f"Biosample_summary={bio};"
                if lab:
                    key_value_pairs += f"Lab={lab};"
                if system:
                    key_value_pairs += f"System={system};"

                # Output key-value pairs if there's any non-empty value
                if key_value_pairs or life_stage_ages:
                    out_f.write(f"{file_base}\t{key_value_pairs}\t{life_stage_ages}\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <directory>")
        sys.exit(1)

    directory = sys.argv[1]
    main(directory)
