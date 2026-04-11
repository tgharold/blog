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



[Time is off by an hour in my XEN vm](http://www.nabble.com/Time-is-off-by-an-hour-in-my-XEN-vm-td16027741.html)

Quote:

There is a RealTimeIsUniversal registry flag hidden in the windows registry that can be set (its not in by default) to let Windows interpret the RTC as UTC as well.
[HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\TimeZoneInformation] "RealTimeIsUniversal"=dword:00000001 

Summary:

The ultimate solution is to probably run an NTP client under the Windows environment to force the software clock to slave properly.
