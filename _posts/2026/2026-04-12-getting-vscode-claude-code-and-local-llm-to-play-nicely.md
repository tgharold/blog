---
layout: post
title: 'Getting VSCode, Claude Code and a local LLM to play nicely'
date: '2026-04-12T15:38:00.000-04:00'
author: Thomas Harold
category:
- Tech
tags:
- LLM
- ClaudeCode
- DevContainers
- VSCode
---

(Qwen wrote this, I trimmed it back)

As part of my ongoing experimentation with local LLMs and AI-assisted development, I've been working on setting up a seamless development environment for my Jekyll-based blog that allows me to leverage Claude Code inside a devcontainer while communicating with a local LLM running on my host machine.

## The Challenge

My main goal was to create a development environment that combines:

1. A Jekyll-based blog in a Docker devcontainer for consistent builds
2. VSCode's Claude Code extension for AI assistance 
3. Communication with a local LLM running on my host machine

This combination would let me write and edit blog posts while having Claude Code leverage my local LLM for responses, providing a more privacy-focused development experience without sacrificing functionality.

This also paves the way for me to switch to [OpenCode](https://opencode.ai/).  That has fewer guardrails than Claude Code making it more important to run inside an isolated environment.

## The Setup Process

I'm going to use the `mcr.microsoft.com/devcontainers/jekyll:bookworm` image as the foundation for the devcontainer.  On top of that I'm going to add:

- Node.js for JavaScript tooling
- Python for various scripts and utilities
- Claude Code feature for AI assistance

In addition, it's recommended that the following mounts are in place:

- Mounting of local Claude configuration files

Some environment variables are being passed in from the host, some are being overriden.

## The Current Working State

While some aspects of the integration are still a bit in flux (as I noted in the commit messages), the core functionality is working:

- VSCode Claude Code extension is properly set up in the devcontainer
- The `ANTHROPIC_BASE_URL` is correctly configured to point to `http://host.docker.internal:1234`
- The `ANTHROPIC_AUTH_TOKEN` is available through environment variables
- Local LLM communication is functional

## Looking Forward

This is just a starting point.  But I have a branch to consider:

If I continue to use Claude Code with a local LLM, I need to come up with a solution for the broken WebSearch tooling.  Claude Code uses server-side tools on Anthropic's servers which the local LLM does not support.  That probably means running an MCP search proxy in Docker Desktop on the host and wiring up Claude to use it.  Getting that working today has escaped my abilities.

The other fork is to switch to OpenCode which doesn't make the assumptions that Claude Code does about some tools at the `ANTHROPIC_BASE_URL` LLM.  Now that I have devcontainers working, it's worth considering the switch.

## devcontainer.json

I could probably drop the 'node' feature without issue.  It's in there because I was trying to get the MCP server working.

```JSON
{
	"name": "Jekyll",
	"image": "mcr.microsoft.com/devcontainers/jekyll:bookworm",
	"features": {
		"ghcr.io/devcontainers/features/node:1": {},
		"ghcr.io/devcontainers/features/python:1": {},
		"ghcr.io/anthropics/devcontainer-features/claude-code:1.0": {}
	},
	"mounts": [
		"source=${localEnv:HOME}/.claude,target=/home/vscode/.claude,type=bind"
	],
	"remoteEnv": {
		"ANTHROPIC_AUTH_TOKEN": "${localEnv:ANTHROPIC_AUTH_TOKEN}",
		"ANTHROPIC_BASE_URL": "http://host.docker.internal:1234",
		"ANTHROPIC_MODEL": "${localEnv:ANTHROPIC_MODEL}"
	},
	"customizations": {
		"vscode": {
			"extensions": [
				"Anthropic.claude-code"
			]
		}
	}
}
```
