---
layout: post
title: 'Colima on macOS 26 for VS Code Dev Containers'
date: '2026-04-12T15:38:00.000-04:00'
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

I'm switching away from Docker Desktop on macOS for my container server and I'm moving over to [Colima](https://colima.run/).  There were other choices like podman and reacher.  Getting this running wasn't too difficult, but still took a few tries.  

Unfortunately, I let this post lie fallow for a week and have forgotten some of the details.

Start with installing Colima, Docker, and the buildx plugin with `brew install colima docker docker-buildx`.

Make sure that `/opt/homebrew/bin` is in your `PATH`, usually by using `export PATH="/opt/homebrew/bin:$PATH"` in your `~/.zshrc` file.  Or use the `export PATH="$(brew --prefix)/bin:$PATH"` command in your `~/.zshrc` file.  This needs to insert the homebrew folder at the start of the path to take precendence over built-in Apple commands.

Another change that I had to make was to `~/.docker/config.json`

```JSON
{
	"auths": {},
	"currentContext": "colima",
	"cliPluginsExtraDirs": [
		"/opt/homebrew/lib/docker/cli-plugins"
	]
}
```

Looking at my `~/.zshrc` file, I also see the following

```shell
export DOCKER_HOST="unix://${HOME}/.colima/default/docker.sock"
```

Making colima autostart was done with a `brew` command.

```shell
brew services start colima
```

## Checklist

1. [Colima](https://colima.run/).
2. Docker CLI and Docker BuildX are still needed.
3. Configuration files for docker CLI.
4. DOCKER_HOST environment variable.
5. Autostart colima.

## docker: unknown command: docker buildx

The first attempt is likely to fail with an error like `docker: unknown command: docker buildx`.  This is because the `docker-buildx` package is not installed.  You can install it with `brew install docker-buildx`.  Note the caveat during the install about creating or updating your `~/.docker/config.json` file to include the `cliPluginsExtraDirs` entry.  This is necessary for Docker to find the plugin.  After installing `docker-buildx`, you should be able to use the `docker buildx` command without any issues.

```
% brew install docker-buildx
==> Fetching downloads for: docker-buildx
✔︎ Bottle Manifest docker-buildx (0.33.0)
✔︎ Bottle docker-buildx (0.33.0)
==> Pouring docker-buildx--0.33.0.arm64_tahoe.bottle.tar.gz
==> Caveats
docker-buildx is a Docker plugin. For Docker to find the plugin, add "cliPluginsExtraDirs" to ~/.docker/config.json:
  "cliPluginsExtraDirs": [
      "/opt/homebrew/lib/docker/cli-plugins"
  ]
==> Summary
🍺  /opt/homebrew/Cellar/docker-buildx/0.33.0: 46 files, 61.2MB
==> Running `brew cleanup docker-buildx`...
Disable this behaviour by setting `HOMEBREW_NO_INSTALL_CLEANUP=1`.
Hide these hints with `HOMEBREW_NO_ENV_HINTS=1` (see `man brew`).
==> Caveats
zsh completions have been installed to:
  /opt/homebrew/share/zsh/site-functions
```

Test whether docker can find the plugin with `docker buildx version`. 

## docker: error getting credentials

If you had Docker Desktop installed previously, your `~/.docker/config.json` will have an entry of `"credsStore": "desktop"` that is causing this error.  

After removing it, save and quit and retry a `docker pull` command.

