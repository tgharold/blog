---
layout: post
title: 'Hard Drive Power Requirements'
date: '2004-05-07T23:29:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Jottting down some of the V/A power-requirements for some hard-drives.  IBM is nice because they print it on the drive, the Maxtors (usually) aren't as helpful.  I'm also trying to make sure that the little 200W power-supplies in the light-weight servers like the VIA EPIA can handle the load. 

[Hitachi Deskstar 180GXP](http://www.hitachigst.com/hdd/support/d180gxp/d180gxp.htm) (07N9685) 82.3GB
7200rpm 8MB cache
5V 500mA 12V 700mA (10.9W)
- startup current is 2.0 (+12V) & 0.83A (+5V) 28W, idle is 5.0W

IBM Deskstar (not sure of model)
7200rpm 8MB cache
5V 300mA 12V 500mA (7.5W)
- this is the one that I tossed in the EPIA box, the 180GXP drew too much power (probably a startup-current issue?)

[Maxtor DiamondMax 16 160GB](http://www.maxtor.com/_files/maxtor/en_us/documentation/data_sheets/diamondmax_16_data_sheet.pdf)
5400rpm 2MB cache ATA/133
5V 585mA 12V 690mA (11.2W)
- label info is diff then data sheet on website (5V 628mA 12V 587mA 10.2W, idle 5.6W)

[Maxtor DiamondMax Plus 9](http://www.maxtor.com/_files/maxtor/en_us/documentation/data_sheets/diamondmax_plus_9_data_sheet.pdf) 60GB-200GB
7200rpm 2MB or 8MB cache, ATA/133 or SATA/150
5V 858mA 12V 662mA (12.2W)

[Western Digital Caviar SE 250GB](http://www.scsi4me.com/index.php?menu=menu_sata&pid=3190) ([WD site](http://www.westerndigital.com/en/products/current/drives.asp?Model=WD2500JD))
7200rpm 8MB cache SATA/150
5V 850 mA 12V 530mA (10.6 W), no startup current listed, idle is 10.0W

[Maxtor MaxLine II](http://www.maxtor.com/_files/maxtor/en_us/documentation/data_sheets/maxline_data_sheet.pdf) 250GB/300GB
5400rpm 2MB cache ATA/133
5V 593mA 12V 594mA (10.1W)

[Maxtor MaxLine II Plus](http://www.maxtor.com/_files/maxtor/en_us/documentation/data_sheets/maxline_data_sheet.pdf) 250GB
7200rpm 8MB cache PATA/133 or SATA/150
5V 921mA  12V 666mA (12.6W)

[Western Digital Caviar 200GB](http://www.westerndigital.com/en/products/current/drives.asp?Model=WD2000BB)
- roughly 12W seeking, 19.0W spin-up, 7.5W idle

[Western Digital Caviar 250GB](http://www.westerndigital.com/en/products/current/drives.asp?Model=WD2500JB)
- roughly 12.5W seeking, 21.4W spin-up, 8.3W idle

[Hitachi Deskstar 7K400](http://www.hitachigst.com/hdd/support/7k400/7k400.htm) 400GB
7200rpm 8MB PATA or SATA
- tough guess, only lists startup (29.5W) and idle (9.5W)

[Hitachi Deskstar 7K250](http://www.hitachigst.com/hdd/support/d7k250/d7k250.htm) 250GB
7200rpm 8MB PATA or SATA
- again, no info, startup is 24W, idle is 7.0W

I'm a bit surprised... the 5400rpm drives really don't require that much less power then the 7200rpm drives.  10W vs 12.5W isn't as a big a difference as I had thought it would be.  Maxtor doesn't list start-up currents, so it's tough to compare against the IBM/Hitachi drive that I used in the EPIA box that I had the problem with.  Still, I suspect that I could indeed drop a pair of the Maxline II 250/300GB drives in an EPIA box without problems.

I'm also looking to start cutting some power-usage as my power bill has crept up from 500KWH per month to 1000KWH per month due to computer equipment.  Instead of using a bunch of small disks, I can save power by using fewer larger disks.  Combined with using lower-power CPUs and I can probably cut that back to 750KWH without sacrificing large amounts of storage space.  

Of course, my 19" monitor eats up 140W... a comparable LCD would probably only eat 40W.  I pay 8.3 cents/KWH, so in a 30.4 day month (730 hours), 100W costs me $6.06.  Using 667 KWH in a month is roughly 914W per hour (to check my math).  A newer ViewSonic p90f 19" ($210) only uses 120W.

So every 10W that I can shave off of power usage saves me $0.61/month ($7.27/yr).  Yeah, not a lot, but every little bit does add up.  At least LCD displays have fallen enough that they're worth buying just for the power-savings instead of a regular CRT.  LCD 17" displays are down to $360 (comparable to a 19" monitor), LCD 15" screens are $275.  Power savings is roughly 60-100W, which works out then to $43-$72/yr.  Cost difference pays for itself after about 2-3 years.
