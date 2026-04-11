# Convert Archive Posts Skill

This skill helps convert HTML archive posts from the Blogger backup into proper Jekyll markdown format for this repository.

## Process Overview

When converting archive posts from the `techblog/2003/06` directory (or similar), follow these steps:

1. **Identify the source files**: Look for `.shtml` files in archive directories like `_archives/techblog/2003/06/`
2. **Extract key information**:
   - Post title (from `<div class="BlogItemTitle">`)
   - Post date (from `<div class="BlogDateHeader">` or permalink)
   - Post content (from `<div class="BlogPost">`)
   - Author and other metadata
3. **Convert to Jekyll format**:
   - Create proper frontmatter with layout, title, date, author, category, and tags
   - Convert HTML content to markdown
   - Use proper date format: `YYYY-MM-DDTHH:MM:SS.000-05:00`
   - Place in correct directory: `_posts/YYYY/`
   - Use filename format: `YYYY-MM-DD-title.md`

## Example Conversion Pattern

From HTML like:
```html
<div class="BlogDateHeader">Wednesday, June 18, 2003</div>
<div class="BlogItemTitle">Encrypted File System (links)</div>
<div class="BlogPost">
  Various articles relating to Windows2000/XP/2003 Encrypted File System:
  <br><br>
  <a href="http://example.com">Link Title</a>
</div>
```

To Jekyll markdown:
```markdown
---
layout: post
title: 'Encrypted File System (links)'
date: '2003-06-18T13:10:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Windows
- Security
- Technology
---

Various articles relating to Windows2000/XP/2003 Encrypted File System:

- [Link Title](http://example.com)
```

## Best Practices

1. **Preserve content integrity**: Convert links but preserve their original URLs
2. **Format consistently**: Use the existing blog's format and structure
3. **Add appropriate tags**: Use existing tag categories from the blog
4. **Date accuracy**: Parse the date correctly from the HTML
5. **File naming**: Use proper format: `YYYY-MM-DD-title.md`
6. **Directory structure**: Place in `_posts/YYYY/` directory matching the year