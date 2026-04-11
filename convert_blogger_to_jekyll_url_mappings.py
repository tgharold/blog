#!/usr/bin/env python3
import os
import csv
import re

def find_blogger_to_jekyll_mappings(search_dir):
    matching_files = []

    for root, dirs, files in os.walk(search_dir):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if re.search(r'\]\(/techblog/', content):
                            relative_path = os.path.relpath(file_path)
                            old_url_matches = re.findall(r'\]\((/techblog/.*?\.shtml)\)', content)
                            for old_url in old_url_matches:
                                matching_files.append((relative_path, old_url))
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

    return matching_files

def write_csv(file_data, output_file):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['file_path', 'old_url'])
        for path, old_url in file_data:
            writer.writerow([path, old_url])

def main():
    search_dir = '_posts'
    output_file = 'convert_blogger_to_jekyll_url_mappings_results.csv'

    if not os.path.exists(search_dir):
        print(f"Error: Directory '{search_dir}' does not exist.")
        return

    print(f"Searching for files containing markdown links to '/techblog/' in '{search_dir}'...")

    url_mappings = find_blogger_to_jekyll_mappings(search_dir)

    print(f"Found {len(url_mappings)} URL mappings in files containing the pattern.")

    write_csv(url_mappings, output_file)

    print(f"Results written to '{output_file}'")

if __name__ == '__main__':
    main()