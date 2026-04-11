---
layout: post
title: 'Gentoo Install 3 (Bootstrapping)'
date: '2004-06-15T20:28:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


([previous post](/blog/2004-06-15-gentoo-install-2-via-epia-me6000/))

Time to bootstrap the system (See [moving from stage 1 to stage 2](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=6)).  If you have multiple machines on the network, all with the same version of gcc, now is the when you'll want to [configure your distcc configuration](http://www.gentoo.org/doc/en/distcc.xml).
```
# cd /usr/portage
# scripts/bootstrap.sh
```

This will take a while to run (update: took 8 hours to run).  If the bootstrap script fails, and you're re-using a portage tree (or possibly other files under /opt, /usr, /var, /home, /tmp or /var/tmp), then you may need to clean out the old files.  (Generally not an issue if you're doing a fresh install.)

Once that finishes, run the following command.
```
# emerge system
```

Which will also take a while to run (last time it took around 5.5 hours).  Update: Took around 4.5 hours this time.

([next post](/blog/2004-06-16-gentoo-install-4-installing-the-kernel-sources/))
