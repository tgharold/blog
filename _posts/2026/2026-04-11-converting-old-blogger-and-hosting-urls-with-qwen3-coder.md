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
draft: true
---

doing development with Claude Code, but using a local LLM to keep from spending my Claude.ai subscription tokens

technical specs:

macbook pro with the m3 max chip and 64GB of RAM
running omlx (insert link to omlx https://omlx.ai/) locally
running Qwen3-Coder-30B-A3B-Instruct-MLX-6bit LLM model
max context window is 200000
max tokens is 100000

overall token generation performance is around 22-25 tokens per second, prefill is 214-250 for non-cached prefill.  the cache efficiency is running at 97% for the prefill tokens, which is giving decent savings and speed.

