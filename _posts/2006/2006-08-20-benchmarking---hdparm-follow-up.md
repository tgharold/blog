---
layout: post
title: 'Benchmarking - hdparm (follow-up)'
date: '2006-08-20T15:44:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


If you recall, the [last time I tested hdparm on my Celeron 566MHz system](http://www.tgharold.com/techblog/2006/08/benchmarking-hdparm.shtml), I was getting very poor read performance on /dev/hda.  

So I added in a HTP302 (HighPoint Rocket133) 2-port PCI card and moved hda over to the new card.

I now get 20MB/s buffered reads from both the primary and secondary disk in the RAID1 array and 30MB/s buffered reads from the mirror set.  Which is a lot better then the 3.1MB/s for hda and 3.5MB/s for the overall RAID1 array.

That should make the system feel a lot more snappy.  Now the bottleneck will probably be the CPU or the 100Mbit ethernet card.
