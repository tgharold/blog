---
layout: post
title: 'Identifying bandwidth abusers in Linux'
date: '2007-06-21T11:45:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---



<b># /sbin/ip link</b>

This Linux command will display information about your interfaces.  When doing network analysis, the primary information that we're interested in is whether the interface is running in promiscuous mode.  An adapter that is running in promiscuous mode can capture any packets that pass by on the wire, not just the ones destined for its MAC address.  Here's an example of a ethernet adapter that is in promiscuous mode:

3: eth0: <BROADCAST,MULTICAST,<b>PROMISC</b>,UP> mtu 1500 qdisc pfifo_fast qlen 1000
    link/ether 00:16:ff:ff:ff:25 brd ff:ff:ff:ff:ff:ff

If you're in a situation where there are multiple hosts on the WAN side and you want to monitor traffic for them, you'll need to use an interface in promiscuous mode.  You'll also need to be connected to the same hub as those units, or connected to the same switch where your port is configured in monitoring mode.

<b># /sbin/ifconfig</b>

Use this command to find out which interface is your WAN link and which interface is your LAN link (in the case of multi-homed systems).

<b>/usr/bin/nload -t 10000 -u H -U H -i 1750 -o 1750 eth0</b>

The nload utility is a console application that will graph the inbound and outbound activity on your network interface.  You'll have to download and install this software yourself as it is not included in most distributions.  If you have "rpmforge" configured on your CentOS5 installation, this is as simple as "yum install nload".  Some key arguments are shown above.  "-t 10000" sets the update time to every 10 seconds, "-i" and "-o" set the graph maximum height in kilobits per second (1750 works well for a 1.5Mbit T1).

<b>/usr/sbin/nettop -d 5 -i eth0</b>

This is another console utility that you can add to a Linux firewall.  Nettop displays a tree-like listing of all activity on a particular interface, with the packets grouped by protocol and then port/service.  This gives you a quick idea of what services are abusing your bandwidth.
