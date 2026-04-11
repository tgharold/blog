---
layout: post
title: 'NTP daemons for Gentoo'
date: '2005-11-23T09:18:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Looks like there are two basic choices (according to "emerge -s ntp"), [ntp](http://www.ntp.org/) and [openntpd](http://openntpd.org/).

<pre>*  net-misc/ntp
      Latest version available: 4.2.0.20040617-r3
      Latest version installed: [ Not Installed ]
      Size of downloaded files: 2,403 kB
      Homepage:    http://www.ntp.org/
      Description: Network Time Protocol suite/programs
      License:     as-is

*  net-misc/openntpd
      Latest version available: 3.7_p1
      Latest version installed: 3.7_p1
      Size of downloaded files: 133 kB
      Homepage:    http://www.openntpd.org/
      Description: Lightweight NTP server ported from OpenBSD
      License:     BSD</pre>

I decided to go with OpenNTPD because it seemed to be smaller and less troublesome then the official NTP daemon.  (As one of the lines on the OpenNTPD page says... I'm not after microsecond accuracy.)

If you want to use OpenNTPD, you should dig through the [presentations / papers](http://openntpd.org/papers.html) for a brief overview of the project (such as [matching time against random servers](http://unduli.bsws.de/papers/opencon04/ntpd/mgp00005.html)).

Note that if you're in North America, you'll probably want to change the "servers" line in /etc/ntpd.conf.  NTP.org has a [list of server pools that you can pick from](http://ntp.isc.org/bin/view/Servers/NTPPoolServers), divided by geography.  I chose to use "north-america.pool.ntp.org" as my servers pool.

(I am still evaluating OpenNTPD... and I may switch over to the official NTP server instead.)

Useful links:
[Gentoo Linux Localization Guide](http://www.gentoo.org/doc/en/guide-localization.xml)
[Jeff McCoy | Time](http://www.jeffmccoy.info/linux/config/time.php)

Useful commands:

```
# hwclock --show
# zdump GMT
# zdump EST5EDT
# date
```

These commands should show you a hardware clock that matches either GMT (if you have things set to UTC) or your local timezone.  I had a misconfigured hardware clock that was set to localtime, while my system was thinking it was UTC/GMT time.

Note that when you look at /var/log/messages, the OpenNTPD messages can be a bit confusing.  You will see lines like:

```
Dec 19 21:33:10 localhost ntpd[5673]: adjusting local clock by -11.800044s
Dec 19 21:36:23 localhost ntpd[5673]: adjusting local clock by -11.691234s
Dec 19 21:39:36 localhost ntpd[5673]: adjusting local clock by -11.621488s
```

What this actually means is that your clock is currently off by approximately 12 seconds.  Eventually, OpenNTPD will adjust your clock to be as close as possible to the official time, but it won't make that adjustment suddenly (all at once).  Instead, it will slowly reduce the error amount to the minimum possible for your system.

If you want your server to synchronize at a faster rate, you should manually set the time using the 'date' command to as close to proper time as you can.  Otherwise, it may take a few days for OpenNTPD to finish synchronizing your machine's local clock.

You should also look up the "hwclock" command, especially the --hctosys and --systohc options.  Also look at "nano -w /etc/conf.d/clock", you should probably set the CLOCK_SYSTOHC flag to "yes" so that your system time gets written to the hardware clock during shutdown.
