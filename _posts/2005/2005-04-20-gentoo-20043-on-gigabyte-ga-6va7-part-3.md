---
layout: post
title: 'Gentoo 2004.3 on Gigabyte GA-6VA7+ (part 3)'
date: '2005-04-20T19:42:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---



<b>Note: These directions are works-in-progress... in fact, they might not even work at all until I find out why I'm ending up with non-bootable systems (looks like a bug in the 2.6 kernel).</b>

([previous step](/blog/2005-04-19-gentoo-20043-on-gigabyte-ga-6va7-part-1/))

Time to configure the timezone and setup the kernel, this is [chapter 7 in the Gentoo handbook](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&chap=7).

Timezone for me is EST5EDT, so here's how to set that up.

```
# ls /usr/share/zoneinfo
# ln -sf /usr/share/zoneinfo/EST5EDT /etc/localtime
# date
# zdump GMT
# zdump EST5EDT
```

Last year, I went with development-sources for the kernel in order to get 2.6.  This is no longer necessary (and development-sources has been rolled into vanilla-sources).  So I'm going to go with the default gentoo-sources.

```
# emerge gentoo-sources
# ls -l /usr/src
```

This takes a while to run (maybe an hour or two).

(next step)
