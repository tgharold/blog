---
layout: post
title: 'SVK for system management'
date: '2007-05-29T13:37:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


I'm a big fan of using a version control system in conjunction with system administration.  There's a great feeling to know that even if I screw up a configuration file, I have an easily accessible way to revert or track changes.  To accomplish this, I was using [SubVersion (SVN) as an administration tool](/blog/2006-06-14-subversion-for-linux-administrators).

However, SVN comes with some downsides, primarily the issue that it creates ".svn" folders in the directory tree.  Which can cause issues and maybe even lead to security holes (yes/no? unsure about this).

So, maybe SVK is better suited.  

<b>Installing SVK on CentOS5</b>

(See [SVK - Distributed Version Control - Part I (Ron Bieber, 2004) for a good tutorial.](http://www.bieberlabs.com/wordpress/archives/2004/11/30/using-svk))

1. Open up the package manager and make sure you have installed the following packages:

        "subversion" (possibly not required)
        "subversion-perl" (Perl bindings)

Or, using the command-line (for x86_64):

    # yum install subversion.x86_64 subversion-perl.x86_64

At least... I think the above command works.  I used the GUI package manager for this step.

2. Use Perl and CPAN to install the SVK system.

        # perl -MCPAN -e 'install SVK'

You'll be presented with about a dozen questions, and you'll need to install all sorts of modules if this is your first time running that command.  It's all pretty self-explanatory (and I was on the phone while doing that, so I wasn't able to jot everything down).

...

Well, after mucking with this for a few hours and getting self-test errors, I'm going to shelve this for now and go look at FSVS insteadk.
