#!/usr/bin/env python3

import os
import re
from pathlib import Path

def remove_clearboth_divs():
    """Remove <div style="clear:both; padding-bottom:0.25em"></div> sections from blog posts"""

    # Find all markdown files in _posts directory
    posts_dir = Path("_posts")
    markdown_files = posts_dir.rglob("*.md")

    pattern = r'<div style="clear:both; padding-bottom:0.25em"></div>.*'

    modified_count = 0

    for file_path in markdown_files:
        try:
            # Read the file content
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Check if file contains the pattern
            if '<div style="clear:both; padding-bottom:0.25em"></div>' in content:
                # Remove the pattern and everything after it
                new_content = re.sub(pattern, '', content, flags=re.DOTALL)

                # Remove any trailing whitespace
                new_content = new_content.rstrip() + '\n'

                # Write back to file if changed
                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Modified: {file_path}")
                    modified_count += 1
                else:
                    print(f"No change needed: {file_path}")
            else:
                print(f"No pattern found: {file_path}")

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    print(f"Processed {modified_count} files.")

if __name__ == "__main__":
    remove_clearboth_divs()