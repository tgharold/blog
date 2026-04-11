---
layout: post
title: 'Methods ofr remote GUI control of Linux servers'
date: '2008-04-15T18:53:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


There are currently (3) basic methods for getting a remote control GUI on a Linux server (like we do with Remote Desktop for Windows servers):

1) X-Windows over TCP/IP

All GUI operations on Unix/Linux are handled by the X-Windows sub-system.  Window interfaces like KDE, Gnome, and others are merely layered on top of the X sub-system.  One of the useful things about X is that any window can be forwarded over TCP/IP to any other X server.  So you could run an application on the linux server, but display the output window on your PC (as long as you run a local X server program).

The downside of all this is that accessing remote servers requires the use of SSH port forwarding, and a bit of arcane magic.  It's nowhere near as clean of a solution as RDP (Terminal Services).  But it can be ultra-secure (by using SSH keys) and it works fairly well across the WAN.

2) VNC

VNC is a screen-scraper solution for GUI desktops, very similar to the old pcAnywhere and e/pop solutions that we used to use.

The downsides of VNC are:
- security is non-existent in the base spec
- different VNC server use different encryptions
- authentication tends to be done via plain text passwords
- rather slow across the WAN

3) NX/FreeNX

A company called NoMachines came out with a different solution called "NX".  NX is a protocol that is very similar to RDP and the client works rather similar to Remote Desktop.  You used to have to pay for the product, but over the years, they've opened up the source code.  So now there are (3) different server implementations (NX, FreeNX, and another) and you can download the NX client from NoMachines for free. 

The big advantage here is that security is better and performance is better over slow WAN links.
