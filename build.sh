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
    bundle config set path "$BUNDLE_PATH"

    # Fix Ruby 4.0/3.4+ compatibility: csv, yaml, base64, and bigdecimal were removed from default gems
    export RUBYOPT="-ruri -ryaml -rbase64"

    bundle install
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
