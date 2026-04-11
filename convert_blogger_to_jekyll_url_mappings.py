#!/usr/bin/env python3
import os
import csv
import re

def find_markdown_files_with_blogger_links(search_dir):
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

    for data in unique_old_urls_data:
        old_url = data['old_url']
        url_parts = old_url.strip('/').split('/')
        if len(url_parts) >= 4 and url_parts[0] == 'techblog':
            year = url_parts[1]
            month = url_parts[2]
            filename_with_ext = url_parts[3]
            filename = filename_with_ext.rsplit('.', 1)[0] if '.' in filename_with_ext else filename_with_ext

            print(f"Processing old_url: {old_url}")
            print(f"  Year: {year}")
            print(f"  Month: {month}")
            print(f"  Filename (without extension): {filename}")

            search_pattern = f"_posts/{year}/{year}-{month}-*.md"

            matching_files = glob.glob(search_pattern)

            found_files = matching_files
            print(f"  Found {len(found_files)} matching markdown files")

            exactly_matched_file = None
            for file_path in found_files:
                file_basename = os.path.basename(file_path)
                file_base_without_ext = file_basename.rsplit('.', 1)[0] if '.' in file_basename else file_basename

                if filename in file_base_without_ext:
                    exactly_matched_file = file_path
                    break

            if exactly_matched_file:
                data['path_to_new_markdown_file'] = exactly_matched_file
                print(f"  Match found: {filename} -> {exactly_matched_file}")
            else:
                print(f"  No exact match found for {filename}")
                # Try fuzzy matching
                if found_files:
                    import difflib
                    print(f"  Attempting fuzzy matching with {len(found_files)} candidates...")
                    # Get the base names for comparison
                    base_names = [os.path.splitext(os.path.basename(f))[0] for f in found_files]
                    # Get the best fuzzy matches with scores
                    matcher = difflib.SequenceMatcher(isjunk=None, a=filename, b=None)
                    matches_and_scores = []
                    for base_name in base_names:
                        matcher.set_seq2(base_name)
                        ratio = matcher.ratio()
                        if ratio >= 0.3:  # Only include matches above cutoff
                            matches_and_scores.append((base_name, ratio))

                    # Sort by score (descending)
                    matches_and_scores.sort(key=lambda x: x[1], reverse=True)

                    if matches_and_scores:
                        print(f"  {len(matches_and_scores)} fuzzy matches found (with scores):")
                        for base_name, score in matches_and_scores[:5]:  # Show top 5
                            print(f"    Fuzzy match: {base_name} (score: {score:.2f})")

                        # If there's exactly one high-quality match, use it
                        if len(matches_and_scores) == 1 and matches_and_scores[0][1] >= 0.5:
                            matched_file = matches_and_scores[0][0]
                            # Find the actual file path for this match
                            for file_path in found_files:
                                if os.path.splitext(os.path.basename(file_path))[0] == matched_file:
                                    data['path_to_new_markdown_file'] = file_path
                                    print(f"  Single high-quality fuzzy match used: {filename} -> {file_path}")
                                    break
                        # For multiple matches, implement enhanced logic
                        elif len(matches_and_scores) > 1:
                            # If there's at least one high-quality match (score >= 0.8), use the best one
                            high_quality_matches = [match for match in matches_and_scores if match[1] >= 0.65]
                            if high_quality_matches:
                                # Use the highest scoring match among high-quality matches
                                best_match = max(high_quality_matches, key=lambda x: x[1])
                                matched_file = best_match[0]
                                # Find the actual file path for this match
                                for file_path in found_files:
                                    if os.path.splitext(os.path.basename(file_path))[0] == matched_file:
                                        data['path_to_new_markdown_file'] = file_path
                                        print(f"  High-quality fuzzy match used (score: {best_match[1]:.2f}): {filename} -> {file_path}")
                                        break
                    else:
                        print(f"  No fuzzy matches found for {filename}")

        else:
            print(f"Warning: Unable to parse old_url format: {old_url}")


def update_new_urls(unique_old_urls_data):
    """Process unique_old_urls_data to create new_url values based on permalink style."""
    import os

    for data in unique_old_urls_data:
        # Check if path_to_new_markdown_file exists
        if data['path_to_new_markdown_file']:
            # Extract the date and filename from the path
            file_path = data['path_to_new_markdown_file']
            file_basename = os.path.basename(file_path)

            # Parse the date from the filename (format: YYYY-MM-DD-*)
            if '-' in file_basename:
                # Split by hyphens to get components
                parts = file_basename.split('-')
                if len(parts) >= 4:
                    try:
                        year, month, day = parts[0], parts[1], parts[2]
                        # Extract the title part (everything after YYYY-MM-DD-)
                        title_parts = parts[3:]
                        # Join title parts and remove extension
                        filename_only = '-'.join(title_parts).split('.', 1)[0]
                        data['new_url'] = f"/blog/{year}-{month}-{day}-{filename_only}/"
                        print(f"  New URL created: {data['new_url']}")
                    except Exception as e:
                        print(f"  Warning: Could not parse date from filename {file_basename}: {e}")
        else:
            # If no path found, we'll leave new_url as empty
            data['new_url'] = ""
            print(f"  No path found for {data['old_url']}, leaving new_url empty")

def update_markdown_files_with_new_urls(markdown_files_with_blogger_links, unique_old_urls_data):
    """Update markdown files by replacing old_url with new_url based on unique_old_urls_data."""
    for file_path, old_url in markdown_files_with_blogger_links:
        # Find the corresponding new_url for this old_url
        new_url = ""
        for data in unique_old_urls_data:
            if data['old_url'] == old_url:
                new_url = data['new_url']
                break

        if new_url:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                # Replace all occurrences of the old URL with the new URL
                updated_content = content.replace(f"]({old_url})", f"]({new_url})")

                # Write the updated content back to the file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)

                print(f"Updated {file_path}: {old_url} -> {new_url}")
            except Exception as e:
                print(f"Error updating {file_path}: {e}")
        else:
            print(f"No new URL found for {old_url} in {file_path}, skipping update.")

def main():
    search_dir = '_posts'
    output_file = 'convert_blogger_to_jekyll_url_mappings_results.csv'
    unique_output_file = 'convert_blogger_to_jekyll_url_mappings.csv'

    if not os.path.exists(search_dir):
        print(f"Error: Directory '{search_dir}' does not exist.")
        return

    print(f"Searching for files containing markdown links to '/techblog/' in '{search_dir}'...")

    markdown_files_with_blogger_links = find_markdown_files_with_blogger_links(search_dir)

    print(f"Found {len(markdown_files_with_blogger_links)} URL mappings in files containing the pattern.")

    # Write the original CSV with file_path and old_url
    write_csv(markdown_files_with_blogger_links, output_file)
    print(f"Results written to '{output_file}'")

    # Extract all unique old_url values
    unique_old_urls_data = []
    seen_old_urls = set()

    for path, old_url in markdown_files_with_blogger_links:
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

    # Process the data to create new_url values
    update_new_urls(unique_old_urls_data)

    write_unique_old_urls_csv(unique_old_urls_data, unique_output_file)
    print(f"Unique old_url values written to '{unique_output_file}'")

    update_markdown_files_with_new_urls(markdown_files_with_blogger_links, unique_old_urls_data)

if __name__ == '__main__':
    main()