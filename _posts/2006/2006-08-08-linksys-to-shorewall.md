---
layout: post
title: 'Linksys to Shorewall'
date: '2006-08-08T06:46:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>Over the past week, I've been encountering slowdowns on my DSL connection.  Normally, I can get 1.5Mbps download speeds, which is what I'm provisioned for and what the line is capable of.  But over the past week or so, my top download speed has gradually fallen to around 300-500Kbps (1/5 to 1/3 of the usual bandwidth).  It didn't seem to matter what protocol I was using at the time either.

So I did some testing.  With the LinkSys router involved, I was seeing download rates of 300-500Kbps.  But if I hooked a laptop directly to the DLS modem, I could get 1.5Mbps again.  Ah ha!  That shows clearly that the issue is not any sort of bandwidth shaping or traffic limiting by the ISP but rather something strange going on with my Linksys BEFW11S4 router.

Since the router is a few years old (circa 2001), it could simply be age related.  Maybe a heatsink has come loose (making the CPU throttle back) or a capacitor has failed or something else.  

Rather then adding a new hardware-based router to the mix, I decided to press my old VIA C3 box into service as the new firewall/NAT.  It's something I had been considering doing for a while, but kept putting it off due to the complexities involved.  Mostly, I worry about my misconfiguring the box, allowing it to get hacked and turned into someone else's playtoy.

It took me around 2 hours to configure Shorewall for Gentoo on my C3 box.  So far it seems to be working fine and provides me with some new diagnostic tools (such as "nettop").  According to the ShieldsUp! portscan service, everything is stealthed except for the tcp/113 ident port which is simply closed.

Now I can go read up on my Linux security books and figure out if I want to continue using Shorewall or not.

Follow-up note: Unfortunately, I was never able to get PPTP pass-through working.  I was trying to use Shorewall in a SOHO environment where I create a VPN connection from my laptop out through the Shorewall NAT to a PPTP VPN server on the public internet.  But something in either the Linux kernel or the Shorewall / IPTables configuration is blocking all or some of the PPTP traffic.  So I had to drop the Linksys hardware router back in so that I could get work done.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2006.shtml">2006</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/IPTables.shtml">IPTables</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/NAT.shtml">NAT</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/PPTP.shtml">PPTP</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Shorewall.shtml">Shorewall</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/VPN.shtml">VPN</a>
		<div class="Byline">
			posted by Thomas at 
			[06:46](http://www.tgharold.com/techblog/2006/08/linksys-to-shorewall.shtml)

		</div>