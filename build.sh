#!/bin/bash

# Build script for Tech Blog (Jekyll)
# Usage: ./build.sh [serve|build]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Set bundle path for local gems
export BUNDLE_PATH="${BUNDLE_PATH:-vendor/bundle}"

# Function to install dependencies
install_deps() {
    echo "Installing dependencies..."
    bundle install --path "$BUNDLE_PATH"
}

# Function to build the site
build() {
    echo "Building site..."
    bundle exec jekyll build
}

# Function to serve the site locally
serve() {
    echo "Starting development server..."
    bundle exec jekyll serve --watch --force_polling
}

# Main logic
case "${1:-build}" in
    build)
        install_deps
        build
        echo "Build complete! Site is in _site/"
        ;;
    serve)
        install_deps
        serve
        ;;
    clean)
        echo "Cleaning build artifacts..."
        rm -rf _site vendor/bundle
        ;;
    *)
        echo "Usage: $0 [build|serve|clean]"
        echo ""
        echo "Commands:"
        echo "  build   - Build the site (default)"
        echo "  serve   - Start development server with auto-reload"
        echo "  clean   - Remove build artifacts and vendor directory"
        exit 1
        ;;
esac
