# Resolving GitHub Pages Gem Dependency Issue

## Problem
The warning you're seeing:
> Warning: The github-pages gem can't satisfy your Gemfile's dependencies

Occurs because GitHub Pages has its own set of pinned gem versions, and the versions specified in your Gemfile conflict with those built-in versions.

## Solution

I've made the following changes to fix this issue:

1. **Updated your Gemfile** to remove the problematic github-pages gem dependency that was causing conflicts
2. **Created a GitHub Actions workflow** to build your site properly on GitHub

### Why this works:

1. GitHub Pages uses a specific set of gems that are compatible with each other. When you explicitly include gems that don't match those versions, conflicts occur.

2. By using GitHub Actions (which I've set up as `.github/workflows/jekyll.yml`), your site will be built with the exact dependencies specified in your Gemfile, which gives you more control.

3. This approach maintains compatibility with GitHub Pages' requirements while allowing you to use the gems you need for your Skinny Bones theme.

## Verification steps:
1. Commit these changes to your repository
2. Push the changes to GitHub 
3. The GitHub Actions workflow should run automatically
4. The build should complete without the dependency warning

## Alternative approach (if you want to stick with GitHub Pages' built-in build):
If you prefer to keep using GitHub Pages' automatic build system instead of GitHub Actions, you can:

1. Remove the `.github/workflows/jekyll.yml` file I created
2. Remove any `github-pages` gem entries from your Gemfile
3. The site will then build with GitHub's built-in gem versions (but may lack some dependencies)

The first approach (GitHub Actions) is recommended as it gives you full control over your build process.