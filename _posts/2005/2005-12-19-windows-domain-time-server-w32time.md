---
layout: post
title: 'Windows domain time server (W32Time)'
date: '2005-12-19T21:21:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


I'm not going to get into the full details of configuring a time server for your Windows 2000 or Windows 2003 domains, but the basic idea is that your PDC (Primary Domain Controller) at the root of your Active Directory forest should be synchronized with an external time source.  Microsoft includes a service to do this called "Windows Time" (a.k.a. W32Time).  It's not as nice as the official NTPD service that you can get from ntp.org, but it generally works.

By default, Windows client computers that are members of a domain should get their time from the domain controllers within the domain.  So once you get the domain controllers keeping time properly you won't have to deal with bad time on the desktops.

Microsoft Articles:
[Registry entries for the W32Time service](http://support.microsoft.com/support/kb/articles/q223/1/84.asp%20)
[Basic Operation of the Windows Time Service](http://support.microsoft.com/default.aspx?scid=kb;EN-US;224799)

An extremely good page that shows you [whether W32Time is configured properly to sync against an external server](http://www.anotherurl.com/library/network_time.htm).  The basic idea is that you <b>stop</b> the "Windows Time" service and the execute the following command at the prompt.

<pre>w32tm -once
... (content snipped for brevity) ...
W32Time: BEGIN:TimeSync
W32Time:    BEGIN:FGetType
W32Time:    END  Line 254
W32Time:    BEGIN:FDoTimeNTPType
W32Time:       BEGIN:ChooseNTPServer
W32Time:       END  Line 2178
W32Time:       BEGIN:GetSocketForSynch
W32Time:          NTP: ntpptrs[0] - US.POOL.NTP.ORG
W32Time:          rgbNTPServer US.POOL.NTP.ORG
W32Time:          BEGIN:TsUpTheThread
W32Time:          END  Line 1407
W32Time:          NTP(S): waiting for datagram...
W32Time:          Port Pinging to - 123
W32Time:          Connecting to "US.POOL.NTP.ORG" (216.52.237.152)
W32Time:       END:Line 1170
W32Time:       BEGIN:GetDefaultRid
W32Time:       END  Line 2359
W32Time:       BEGIN:ComputeDelay
W32Time:          BEGIN:NTPTry -- init
W32Time:          END  Line 1683
W32Time:          BEGIN:NTPTry -- try
W32Time:             BEGIN:ComputeInterval
W32Time:             END  Line 2479
W32Time:             Sending to server  48 bytes...
W32Time:             Recv'ed from server  48 Bytes...
W32Time:          END  Line 1885
W32Time:          BEGIN:NTPTry -- delay
W32Time:          END  Line 2012
W32Time:          Round trip was 90ms
W32Time:          BEGIN:NTPTry -- try
W32Time:             BEGIN:ComputeInterval
W32Time:             END  Line 2479
W32Time:             Sending to server  48 bytes...
W32Time:             Recv'ed from server  48 Bytes...
W32Time:          END  Line 1885
W32Time:          BEGIN:NTPTry -- delay
W32Time:          END  Line 2012
W32Time:          Round trip was 90ms
W32Time:          BEGIN:NTPTry -- gettime
W32Time:             BEGIN:Fgmtimetonttime
W32Time:             END  Line 2563
W32Time:          END  Line 1998
W32Time:          one-way delay is 45ms
W32Time:       END  Line 1645
W32Time:    END  Line 368
W32Time:    BEGIN:TimeDiff
W32Time:       ClockError --45702
W32Time:    END  Line 2542
W32Time:    BEGIN:FCheckTimeSanity
W32Time:       Adjusting time by 45702 ms. No eventlog messages since time diffe
rence is 0 &lt;1 minute
W32Time:    END  Line 570
W32Time:    BEGIN:SetTimeNow
W32Time:       Time 12/20/2005   2:20:53:970
W32Time:       *****SetSystemTime()*****
W32Time:    END  Line 1280
W32Time:    Time was 20min 08.268s
W32Time:    Time is  20min 53.970s
W32Time:    Error -45702ms
W32Time:    BEGIN:CheckLeapFlag
W32Time:    END:Line 606
W32Time:    BEGIN:ComputePostTimeData
W32Time:       BEGIN:ComputeInterval
W32Time:       END  Line 2479
W32Time:       BEGIN:ComputeSleepStuff
W32Time:          Computed stagger is 0ms, bias is 0ms
W32Time:          Time until next sync - 2699.960s
W32Time:       END:Line 816
W32Time:    END:Line 221
W32Time: END:Line 196</pre>

The key line in the above output is "Error -45702ms" which shows us how much the Windows server's clock is going to be adjusted by.  You should also look in your System Log (filter for W32Time events) for messages after using the above command (or after stopping/starting the time service).  Those messages in the system log will help you determine why you may not be able to synchronize to an external time server (via 123/udp).

In my opinion, W32Time is "good enough" for most purposes.  At least for small offices or home networks.  If you're going to be dealing with more then a dozen servers or 50 workstations, then you should definitely look into setting up a real "ntpd" server.  (In reality, you should have at least 4 ntpd servers in your infrastructure so that they can keep an eye on each other and alert you to ntpd servers that are not keeping time properly.)

Here's my previous posting dealing with time issues: [NTP daemons for Gentoo](http://www.tgharold.com/techblog/2005/11/ntp-daemons-for-gentoo.shtml)
