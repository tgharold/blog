---
layout: post
title: 'Converting old Blogger or old hosting URLs to the new style using Qwen3-Coder'
date: '2026-04-11T17:48:00.000-04:00'
author: Thomas Harold
category:
- Tech
tags:
- LLM
- Qwen3
---

Recently, I've been experimenting with using local LLMs through Claude Code to avoid consuming my Claude.ai subscription tokens. This involved setting up Qwen3-Coder-30B-A3B-Instruct-MLX-6bit on my MacBook Pro with an M3 Max chip and 64GB of RAM using [omlx](https://omlx.ai/).

Technical specifications:
- MacBook Pro with M3 Max chip and 64GB RAM
- Running omlx locally
- Using Qwen3-Coder-30B-A3B-Instruct-MLX-6bit LLM model
- Max context window: 200,000 tokens
- Max tokens: 100,000 tokens

Performance-wise, the model generates around 22-25 tokens per second, with a prefill of 214-250 for non-cached prefill. The cache efficiency is running at 97% for prefill tokens, which provides decent savings and speed.  That's the numbers reported after processing about 78 million prefill tokens per the dashboard.

While the model performs adequately, it's not quite as capable as Sonnet within Claude Code. I need to break down problems into smaller steps and be very explicit to get the desired results. It also tends to forget to reference CLAUDE.md and its memory files regarding my preferences. This is evident in many commits to my blog repository that are missing the co-author line, despite my explicit instructions in the CLAUDE.md file (https://github.com/tgharold/blog/blob/master/CLAUDE.md).

As part of this experimentation, I created the [convert_blogger_to_jekyll_url_mappings.py](https://github.com/tgharold/blog/blob/master/convert_blogger_to_jekyll_url_mappings.py) script using the Qwen3-Coder model. However, looking at the [various commits to that file](https://github.com/tgharold/blog/commits/master/convert_blogger_to_jekyll_url_mappings.py), I had to guide it through the process step-by-step. While it would have been faster for me to write the script myself, I was still learning Python and needed the model to demonstrate the implementation approach.
