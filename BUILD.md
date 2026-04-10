# Building This Blog on macOS

This blog is built with Jekyll. Follow these steps to build it locally on macOS.

## Prerequisites

### 1. Install Homebrew (if not already installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Ruby via Homebrew

```bash
# Install Ruby (includes bundler)
brew install ruby@3.2

# Verify installation
ruby --version
gem --version
```

### 3. Install Dependencies

```bash
# Install project dependencies
bundle install
```

## Building the Site

### Development Server

```bash
bundle exec jekyll serve
```

The site will be available at `http://localhost:4000/blog/`

### Production Build

```bash
bundle exec jekyll build
```

The built site will be in the `_site` directory.

## Troubleshooting

### Permission Errors

If you see "Bundler requires sudo access":
- You're trying to install gems system-wide
- Use `bundle config set path 'vendor/bundle'` to install locally

### Bundler Version Mismatches

If you see errors about bundler versions:
```bash
bundle config set path 'vendor/bundle'
bundle install
```

## Dependencies

This project uses the following Jekyll plugins:
- jekyll
- jekyll-sitemap
- jekyll-gist
- jekyll-feed

See `Gemfile` and `Gemfile.lock` for exact versions.
