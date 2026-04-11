---
layout: post
title: 'More handy Linux console tools'
date: '2005-12-20T19:48:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


A few more tools that I've found useful for console-only Linux server administration.  All of these have Gentoo ebuilds so they can simply be emerge'd into your system.

[atop](http://www.atcomputing.nl/Tools/atop) - Similar to the built-in "top" command in Linux/Unix, except that it gives additional details about what is going on with the system.  Of particular use is that it will show you individual disk utilization statistics so that you can locate spindles that are in heavy use.  (Which is much needed when tuning a database server.)

[tree](http://mama.indstate.edu/users/ice/tree/) - Allows you to output a hierachial display of all files and directories on your system in a "tree" view.  Which is useful for documenting the directory layout of your system.
