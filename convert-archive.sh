#!/bin/bash
# Archive Post Conversion Script
# This script converts Blogger archive posts to Jekyll markdown format

# Check if archive file argument is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <archive_file.shtml>"
    exit 1
fi

ARCHIVE_FILE="$1"

# Check if file exists
if [ ! -f "$ARCHIVE_FILE" ]; then
    echo "Error: File $ARCHIVE_FILE not found"
    exit 1
fi

# Use the Ruby conversion script
ruby "$(dirname "$0")/convert-archive.rb" "$ARCHIVE_FILE"