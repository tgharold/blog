---
layout: post
title: 'VIA EPIA Gentoo Build'
date: '2004-04-27T16:53:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>Got the VIA EPIA ME6000 system today.  Only gltich off the bat was that the first 7200rpm drive that I used draws slightly too much power which resulted in the system refusing to power-up.  (Hooking up an external 300W ATX power-supply proved that the components work fine.)  Fortunately, I had another 7200rpm laying around with lower power requirements.  (The problem drive was 500mA 3V 700mA 5V, the replacement drive is only 300mA 3V 500mA 5V.  Oddly, both drives are 80GB IBM DeskStars.)  A 5400rpm drive would've probably drawn even less power.  So my config at the moment (unless I change drives again):

IDE0/PRI: 80GB IBM DeskStar 7200rpm
IDE0/SEC: (nothing)
IDE1/PRI: 120GB Western Digital 5400rpm
IDE1/SEC: DVD-ROM

No PCI card installed, and a 3.5" floppy-drive up front.

Now, the 120GB Western Digital has a nasty bearing whine at the moment, so I think I'll be swapping that out pretty quick for a better drive.  It's definitely the loudest thing in the case, and very annoying.  Haven't decided if I'll replace the 7200rpm drive with a 5400 as well (probably will, if only for power/heat reasons).  The new 160GB 5400rpm drive isn't slated to arrive until Thursday, which is why things are as they are for the moment.

The Morex Venus 668 case isn't a bad little case, a bit larger then I expected.  Hold a pair of paperback books up, spine-to-spine and you'll get an idea of how big the front of it is.  Installing the components wasn't too bad, but it's best if you remove the power-supply during the initial installation and work from the bottom-up.  A short (4") phillips-head screwdriver might have been easier to use then the regular sized ratchet screwdriver that I use.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2004.shtml">2004</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Gentoo.shtml">Gentoo</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/VIAEPIA.shtml">VIAEPIA</a>
		<div class="Byline">
			posted by Thomas at 
			[16:53](http://www.tgharold.com/techblog/2004/04/via-epia-gentoo-build.shtml)

		</div>