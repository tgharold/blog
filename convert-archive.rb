#!/usr/bin/env ruby

# Archive Post Conversion Script
# This script converts Blogger archive posts to Jekyll markdown format

require 'nokogiri'
require 'date'

# Check if archive file argument is provided
if ARGV.length != 1
  puts "Usage: #{$0} <archive_file.shtml>"
  exit 1
end

ARCHIVE_FILE = ARGV[0]

# Check if file exists
unless File.exist?(ARCHIVE_FILE)
  puts "Error: File #{ARCHIVE_FILE} not found"
  exit 1
end

# Parse HTML file
doc = Nokogiri::HTML(File.read(ARCHIVE_FILE))

# Extract elements
date_header = doc.css('.BlogDateHeader').first&.text
title = doc.css('.BlogItemTitle').first&.text
post_content = doc.css('.BlogPost').first

if date_header.nil? || title.nil? || post_content.nil?
  puts "Error: Could not extract required elements from #{ARCHIVE_FILE}"
  exit 1
end

# Extract date from BlogDateHeader
date_match = date_header.match(/(.*?), (.*?) (\d{1,2}), (\d{4})/)
if date_match
  day_name = date_match[1]
  month_name = date_match[2]
  day = date_match[3]
  year = date_match[4]

  # Convert month name to numeric
  months = {
    "January" => "01", "February" => "02", "March" => "03",
    "April" => "04", "May" => "05", "June" => "06",
    "July" => "07", "August" => "08", "September" => "09",
    "October" => "10", "November" => "11", "December" => "12"
  }

  month_num = months[month_name] || "01"

  # Extract time from byline
  time_element = doc.css('.Byline a[title="permanent link"]').first
  time = time_element ? time_element.text : "00:00"

  date_str = "#{year}-#{month_num}-#{day.rjust(2, '0')}T#{time}:00.000-05:00"
else
  puts "Warning: Could not parse date format, using fallback"
  date_str = "2003-01-01T00:00:00.000-05:00"
end

# Clean title for filename
clean_title = title.gsub(/[^\w\s-]/, '').gsub(/\s+/, ' ').strip
clean_title = clean_title.gsub(/\s/, '-').downcase

# Create target directory
year = date_str[0..3]
target_dir = "_posts/#{year}"
Dir.mkdir(target_dir) unless Dir.exist?(target_dir)

# Create target filename
filename = "#{date_str[0..9]}-#{clean_title}.md"
target_file = File.join(target_dir, filename)

# Extract content and process it
content = post_content.inner_html

# Basic cleanup - convert <br /> to \n
content.gsub!(/<br\s*\/?>/i, "\n")

# Convert links - convert <a href="url">text</a> to [text](url)
content.gsub!(/<a\s+href="([^"]*)"[^>]*>(.*?)<\/a>/i) do |match|
  href = $1
  text = $2
  # Remove any HTML tags from the text
  text.gsub!(/<[^>]*>/, '')
  "[#{text}](#{href})"
end

# Clean up paragraph tags
content.gsub!(/<p[^>]*>(.*?)<\/p>/i, '\1')
content.gsub!(/\n\s*\n/, "\n\n")

# Create the markdown file with frontmatter
frontmatter = <<~FRONTMATTER
---
layout: post
title: '#{title}'
date: '#{date_str}'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---
FRONTMATTER

File.write(target_file, frontmatter + "\n\n" + content.strip)

puts "Successfully converted #{ARCHIVE_FILE} to #{target_file}"