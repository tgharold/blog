---
layout: post
title: 'Gentoo 2004.3 on Gigabyte GA-6VA7+ (part 2)'
date: '2005-04-19T18:58:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


([Continuation of part 1](/blog/2005-04-20-gentoo-20043-on-gigabyte-ga-6va7-part-3/))

```
# ls -l /etc/make.profile
```

As far as I can tell the 2004.3 already uses the 2.6 kernel, so there's nothing to do here.  I also configured my USE flags in my last post, so that's already done as well.

```
# cd /usr/portage
# scripts/bootstrap.sh
```

This will take a while to run (I estimate a few hours, maybe even overnight).  Once that finishes, you move from stage2 to stage3.

```
# emerge --emptytree system
```

Which will also take a few hours.

([next step](/blog/2005-04-19-gentoo-20043-on-gigabyte-ga-6va7-part-2/))
