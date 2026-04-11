---
layout: post
title: 'Gentoo: Failed to load mii'
date: '2004-06-19T11:25:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


More self-inflicted pain (guarantee that I'm doing this to myself, not due to the Gentoo install guide...)

During boot-up after installing the 2.6.6 kernel, the following (2) modules fail to load:
<pre>Loading module mii...
Failed to load mii

Loading module via-rhine...
Failed to load via-rhine</pre>

The second error is because I had [configured the kernel](/blog/2004-06-16-gentoo-install-5-manual-kernel-configuration/) to load "via-rhine" as <b>built-in</b> and not as a <b>module</b>.  You can do one or the other, but not both.

Not sure about the "mii" error, I'll merely comment it out in the autoload config file for now and see what happens.
