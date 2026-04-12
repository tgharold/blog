# .devcontainer

I'm running Claude Code against a local LLM, not Anthropic's servers.  That LLM is listening on port 0.0.0.0:1234 in the macOS host.  We have to use Docker's networking to connect back to it.  Probably.

> To pipe a macOS host service (e.g., MySQL, Redis) into a VS Code Dev Container, use host.docker.internal as the hostname within the container to map network traffic. Configure the service on macOS to listen on 0.0.0.0 (not just 127.0.0.1), and reference this host address in your app configuration within the devcontainer.json environment variables or application settings. 

I've gone into the firewall and blocked python3 (since I'm using oMLX) from accepting inbound connections.
