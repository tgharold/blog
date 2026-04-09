# Building This Blog on macOS

This blog is built with Jekyll. Follow these steps to build it locally on macOS.

## Prerequisites

### 1. Install Homebrew (if not already installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. Install Ruby via rbenv

Building Ruby from source on macOS can be problematic, especially on Apple Silicon. The recommended approach is to use rbenv with a pre-built Ruby version.

```bash
# Install rbenv and ruby-build
brew install rbenv ruby-build

# Initialize rbenv in your shell (add to ~/.zshrc)
echo 'eval "$(rbenv init - zsh)"' >> ~/.zshrc
source ~/.zshrc

# Install Ruby 3.2.x (compatible with this project's dependencies)
rbenv install 3.2.11

# Set as global default for this project
cd /Users/tgh/projects/tgharold/blog
rbenv local 3.2.11
```

### Alternative: Use portable-ruby (if rbenv build fails)

If building Ruby with rbenv fails, you can use the pre-built portable-ruby:

```bash
brew install portable-ruby
export PATH="/usr/local/opt/portable-ruby/bin:$PATH"
```

Note: portable-ruby 4.0.x may have compatibility issues with older bundler versions.

### 3. Install Dependencies

```bash
# Install Bundler if not present
gem install bundler

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

### Ruby Build Failures

If `rbenv install 3.2.11` fails with "BUILD FAILED":
- This is common on macOS, especially Apple Silicon
- Try installing Xcode command line tools: `xcode-select --install`
- Consider using portable-ruby as an alternative

### Permission Errors

If you see "Bundler requires sudo access":
- You're trying to install gems system-wide
- Make sure rbenv is properly initialized and active
- Check with `rbenv version` - it should show the local Ruby

### Bundler Version Mismatches

If you see errors about bundler versions:
```bash
bundle _1.16.2_ install
```

## Dependencies

This project uses the following Jekyll plugins:
- jekyll
- jekyll-sitemap
- jekyll-gist
- jekyll-feed

See `Gemfile` and `Gemfile.lock` for exact versions.
