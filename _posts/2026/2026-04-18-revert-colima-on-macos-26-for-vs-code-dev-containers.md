---
layout: post
title: 'Revert: Colima on macOS 26 for VS Code Dev Containers'
date: '2026-04-18T16:45:00.000-04:00'
author: Thomas Harold
category:
- Tech
tags:
- DevContainers
- VSCode
- macOS
- Colima
- Docker
---

I know I said I was going to use 'colima' for the VS Code Dev Containers.  But after getting constant crashes where the remote extension host would fail unexpectedly, I've gone back to Docker Desktop.

Seen in the VS Code console:

> Extension host (Remote) terminated unexpectedly with code null.

Or you would see errors like:

> Remote Extension host terminated unexpectedly 3 times within the last 5 minutes

So there's some subtle difference between Docker Desktop on macOS versus using 'colima' as the docker backend.

I even stripped down my vscode extensions to just "Dev Container" and still had issues.
