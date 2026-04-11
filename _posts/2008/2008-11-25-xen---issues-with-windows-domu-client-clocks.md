---
layout: post
title: 'Xen - Issues with Windows DomU client clocks'
date: '2008-11-25T23:10:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>
[Time is off by an hour in my XEN vm](http://www.nabble.com/Time-is-off-by-an-hour-in-my-XEN-vm-td16027741.html)

Quote:

There is a RealTimeIsUniversal registry flag hidden in the windows registry that can be set (its not in by default) to let Windows interpret the RTC as UTC as well.
[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\TimeZoneInformation] "RealTimeIsUniversal"=dword:00000001 

Summary:

The ultimate solution is to probably run an NTP client under the Windows environment to force the software clock to slave properly.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2008.shtml">2008</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Win2000.shtml">Win2000</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Xen.shtml">Xen</a>
		<div class="Byline">
			posted by Thomas at 
			[23:10](http://www.tgharold.com/techblog/2008/11/xen-issues-with-windows-domu-client.shtml)

		</div>