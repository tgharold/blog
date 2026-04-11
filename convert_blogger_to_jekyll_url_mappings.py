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

def write_unique_old_urls_csv(unique_old_urls_data, output_file):
    """Write unique old_url values with additional properties to a separate CSV file."""
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['old_url', 'path_to_new_markdown_file', 'new_url'])
        for data in unique_old_urls_data:
            writer.writerow([data['old_url'], data['path_to_new_markdown_file'], data['new_url']])


def find_new_markdown_paths(unique_old_urls_data):
    """Iterate over unique_old_urls_data to find new markdown file paths based on old_url data."""
    import glob
    import os

    # This method will be used to find the new markdown file path based on the old_url data
    # For now, we'll just iterate over the records
    for data in unique_old_urls_data:
        old_url = data['old_url']
        # Extract year, month, and base filename from old_url
        # Expected format: /techblog/YYYY/MM/filename.shtml
        url_parts = old_url.strip('/').split('/')
        if len(url_parts) >= 4 and url_parts[0] == 'techblog':
            year = url_parts[1]
            month = url_parts[2]
            filename_with_ext = url_parts[3]
            # Remove the .shtml extension from filename
            filename = filename_with_ext.rsplit('.', 1)[0] if '.' in filename_with_ext else filename_with_ext

            # Build search pattern for markdown files in _posts/(year)/(year)-(month)-*
            search_pattern = f"_posts/{year}/{year}-{month}-*.md"

            # Find matching files
            matching_files = glob.glob(search_pattern)

            # Create a variable with the search results
            found_files = matching_files

            # Look for exact matches between the base filename and found files
            matched_file = None
            for file_path in found_files:
                # Extract just the filename without path and extension
                file_basename = os.path.basename(file_path)
                file_base_without_ext = file_basename.rsplit('.', 1)[0] if '.' in file_basename else file_basename

                # If there's an exact match, update the data element
                if file_base_without_ext == filename:
                    matched_file = file_path
                    break

            # Update path_to_new_markdown_file if we found a match
            if matched_file:
                data['path_to_new_markdown_file'] = matched_file
                print(f"Match found: {filename} -> {matched_file}")
            else:
                print(f"No exact match found for {filename}")

            # TODO: Implement the logic to find the new markdown file path
            # For now, we just iterate through the data and print the components
            print(f"Processing old_url: {old_url}")
            print(f"  Year: {year}")
            print(f"  Month: {month}")
            print(f"  Filename (without extension): {filename}")
            print(f"  Found {len(found_files)} matching markdown files: {found_files}")
        else:
            print(f"Warning: Unable to parse old_url format: {old_url}")

def main():
    search_dir = '_posts'
    output_file = 'convert_blogger_to_jekyll_url_mappings_results.csv'
    unique_output_file = 'convert_blogger_to_jekyll_url_mappings.csv'

    if not os.path.exists(search_dir):
        print(f"Error: Directory '{search_dir}' does not exist.")
        return

    print(f"Searching for files containing markdown links to '/techblog/' in '{search_dir}'...")

    url_mappings = find_blogger_to_jekyll_mappings(search_dir)

    print(f"Found {len(url_mappings)} URL mappings in files containing the pattern.")

    # Write the original CSV with file_path and old_url
    write_csv(url_mappings, output_file)
    print(f"Results written to '{output_file}'")

    # Extract all unique old_url values
    unique_old_urls_data = []
    seen_old_urls = set()

    for path, old_url in url_mappings:
        if old_url not in seen_old_urls:
            # Initialize path_to_new_markdown_file and new_url as empty for now
            unique_old_urls_data.append({
                'old_url': old_url,
                'path_to_new_markdown_file': '',
                'new_url': ''
            })
            seen_old_urls.add(old_url)

    # Iterate over unique_old_urls_data to find new markdown file paths
    find_new_markdown_paths(unique_old_urls_data)

    write_unique_old_urls_csv(unique_old_urls_data, unique_output_file)
    print(f"Unique old_url values written to '{unique_output_file}'")

if __name__ == '__main__':
    main()