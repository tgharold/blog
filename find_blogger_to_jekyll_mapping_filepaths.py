#!/usr/bin/env python3
"""
Script to extract markdown files containing the exact pattern '](' followed by '/techblog/'
and output their relative paths to a CSV file.
"""

import os
import csv
import re

def find_files_with_pattern(search_dir):
    """Find all markdown files containing links to /techblog/."""
    matching_files = []

    # Walk through all files in the directory
    for root, dirs, files in os.walk(search_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        # Look for markdown links that contain /techblog/
                        # Pattern: ]( followed by /techblog/
                        if re.search(r'\]\(/techblog/', content):
                            # Get relative path from current directory
                            relative_path = os.path.relpath(file_path)
                            matching_files.append(relative_path)
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    return matching_files

def write_csv(file_paths, output_file):
    """Write file paths to a CSV file."""
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # Write header
        writer.writerow(['file_path'])
        # Write each file path
        for path in file_paths:
            writer.writerow([path])

def main():
    search_dir = '_posts'
    output_file = 'blogger_to_jekyll_mapping_filepaths.csv'

    # Check if search directory exists
    if not os.path.exists(search_dir):
        print(f"Error: Directory '{search_dir}' does not exist.")
        return

    print(f"Searching for files containing markdown links to '/techblog/' in '{search_dir}'...")

    # Find matching files
    matching_files = find_files_with_pattern(search_dir)

    print(f"Found {len(matching_files)} files containing the pattern.")

    # Write to CSV
    write_csv(matching_files, output_file)

    print(f"Results written to '{output_file}'")

if __name__ == '__main__':
    main()