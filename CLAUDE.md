# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a Jekyll-based blog hosted on GitHub Pages, originally migrated from Blogger.com. The site uses the Skinny Bones Jekyll template with modifications to work in a "/blog" subdirectory on GitHub Pages.

## Key Files and Structure

- `_config.yml` - Main Jekyll configuration
- `_posts/` - Blog post content in Jekyll format (YYYY-MM-DD-title.md)
- `.github/workflows/jekyll.yml` - GitHub Actions workflow for building and deploying the site
- `index.md` - Main index page
- `README.md` - Project documentation

## Development and Deployment

### Building Locally
To build the site locally for testing:
```bash
bundle install
bundle exec jekyll build
```

### GitHub Actions Workflow
The repository uses a GitHub Actions workflow in `.github/workflows/jekyll.yml` that:
- Builds the site using `actions/jekyll-build-pages@v1`
- Uploads the generated site as an artifact
- Deploys only when changes are pushed to the `master` branch
- Uses proper permissions for GitHub Pages deployment

The workflow is designed with a separation between build and deploy jobs, following GitHub's official documentation for Jekyll sites hosted on GitHub Pages.

### Deployment Details
- The site is deployed to GitHub Pages from the `master` branch
- The base URL is configured as "/blog" in `_config.yml`
- The deployment workflow uses official GitHub Actions for Jekyll site builds
- The deploy step is gated to only run on master branch pushes (`if: github.ref == 'refs/heads/master'`)

## Archive Conversion Process
When converting Blogger archive posts from `_archives/techblog/2003/06/` or similar directories:
1. Extract HTML content from `.shtml` files
2. Convert to Jekyll markdown format with proper frontmatter
3. Maintain original content while converting to markdown
4. Follow existing post structure and naming conventions
5. Place in appropriate `_posts/YYYY/` directory
6. Archive posts have been converted using the enhanced conversion script

## Using Conversion Tools
To convert archive posts, use the provided conversion scripts:
- Run `./convert-archive.sh <archive_file.shtml>` to convert a single archive file
- The script uses `convert-archive.rb` for the actual conversion process
- Conversion follows the skill documentation in `.claude/skills/convert-archive-posts.md`

## Base URL Handling Fix
**Problem**: Links in the post grid were not working correctly on GitHub Pages deployment due to improper base URL handling.
**Solution**: Modified `_includes/post-grid.html` to use Jekyll's `relative_url` filter instead of `{{ site.url }}{{ post.url }}` which properly handles the base URL context for both local development and GitHub Pages deployment.

## Commit Guidelines
When creating git commits for these conversions, please include the following co-authored by line:
Co-Authored-By: Qwen3-Coder-30B-A3B-Instruct-MLX-6bit <Claude Code>