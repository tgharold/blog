---
layout: post
title: 'Sluggish linux box (losing some ticks)'
date: '2005-11-09T10:33:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>Messages seen in my "# dmesg" output.

<code>Losing some ticks... checking if CPU frequency changed.
kjournald starting.  Commit interval 5 seconds
EXT3 FS on dm-2, internal journal
EXT3-fs: mounted filesystem with ordered data mode.
kjournald starting.  Commit interval 5 seconds
EXT3 FS on dm-3, internal journal
EXT3-fs: mounted filesystem with ordered data mode.
kjournald starting.  Commit interval 5 seconds
EXT3 FS on dm-4, internal journal
EXT3-fs: mounted filesystem with ordered data mode.
kjournald starting.  Commit interval 5 seconds
EXT3 FS on dm-5, internal journal
EXT3-fs: mounted filesystem with ordered data mode.
skge eth0: enabling interface
skge eth0: Link is up at 1000 Mbps, full duplex, flow control tx and rx
eth0: no IPv6 routers present
warning: many lost ticks.
Your time source seems to be instable or some driver is hogging interupts
rip __do_softirq+0x48/0xb0</code>

The system is very sluggish, even at the console.  In addition, the rebuild of my one mirror set is only proceeding at a sedate 3MB/s rather then 10-20MB/s.  Looking at "top -n1" shows CPU utilization issues.  Compare the first example here (a normal working system) with my trouble system (2nd example):

Cpu(s):  0.2% us,  0.0% sy,  0.0% ni, 99.7% id,  0.0% wa,  0.0% hi,  0.0% si

Cpu(s):  0.9% us, 39.8% sy,  0.0% ni,  6.0% id,  0.3% wa,  1.0% hi, 52.0% si

Key (also see kernel_stat.h):
us = user
sy = system
ni = nice
id = idle (CPU not doing any work)
wa = iowait (time spent waiting for IO to complete)
hi = hardware interrupts (time spent within hardware interrupt handlers)
si = softirq (time spent within other critical sections within the kernel)

You can see the 40% "sy" (system) and 52% "si" (softirq) utilizations on the problem box, with only 6% idle.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2005.shtml">2005</a>
		<div class="Byline">
			posted by Thomas at 
			[10:33](http://www.tgharold.com/techblog/2005/11/sluggish-linux-box-losing-some-ticks.shtml)

		</div>