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

# Extract the directory and base name
ARCHIVE_DIR=$(dirname "$ARCHIVE_FILE")
BASE_NAME=$(basename "$ARCHIVE_FILE" .shtml)

# Extract year and month from filename (e.g., 2003_04_01_archive.shtml)
YEAR_MONTH=$(echo "$BASE_NAME" | sed -E 's/([0-9]{4})_([0-9]{2})_[0-9]{2}_archive/\1-\2/')

# Create target directory if it doesn't exist
TARGET_DIR="_posts/${YEAR_MONTH}"
mkdir -p "$TARGET_DIR"

# Create a placeholder for the converted file
echo "Archive file $ARCHIVE_FILE processed for conversion"
echo "Please manually convert the content to Jekyll format"
echo "Target directory: $TARGET_DIR"