---
layout: post
title: 'Gentoo EPIA Install (part 4)'
date: '2004-04-28T14:38:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


([previous blog entry](/blog/2004-04-28-gentoo-epia-install-part-3/))

Stage 2 compile is finished ([step 6d in the handbook](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=6)).  Not bad, emerge system took about 5.5 hours to run on my little VIA EPIA ME6000.  Now for [step 7, configuring the kernel](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=7)

Oh heck, I was trying to see what is in the various timezone files and now my screen fonts are screwed.  So now I guess I get to find out what happens if I reboot at this point!  First thing I did was "passwd" and set the root password to something that I know, then I do a "shutdown -h now" to take the box down immediately.  I also changed memory modules (to use an older 512MB ECC PC2100 stick).  The motherboard seems to be okay with the ECC memory, not sure if it actually supports the ECC functionality or not.

Well, I got the error message, "Boot failer: Error loading operating system" on the reboot.  Guess I still need to boot from the LiveCD in order to get a functional system.  Upon reboot, nothing in the /mnt/gentoo tree, which means that I need to remount those folders:

mount /dev//hda2 /mnt/gentoo
mount /dev/hda1 /mnt/gentoo/boot 
mount -t proc none /mnt/gentoo/proc 

All of the LVM stuff doesn't show up right off the bat when booting from the LiveCD, have to start LVM and then get it running.  (Helpful link [about activating a LVM set](http://tldp.org/HOWTO/LVM-HOWTO/activatevgs.html).)  The "vgscan" command is more of a FYI command then a required command, the real deal is the "vgchange -ay" command (which loads all available volume groups).  The "vg*" items should now show up in the /dev/ directory.

modprobe dm-mod
vgscan
vgchange -ay

mount /dev/vgos/opt /mnt/gentoo/opt
mount /dev/vgos/usr /mnt/gentoo/usr
mount /dev/vgos/var /mnt/gentoo/var
mount /dev/vguser/home /mnt/gentoo/home 
mount /dev/vgtmp/tmp /mnt/gentoo/tmp
mount /dev/vgtmp/vartmp /mnt/gentoo/var/tmp

Have to chroot again (I think)

chroot /mnt/gentoo /bin/bash
env-update
source /etc/profile

Now I should be good to go in order to pickup again with chapter 7.  Not sure if I need EST or EST5EDT timezone file (which is what I was attempting to look at the contents of those files for).  Ah, "zdump" to the rescue.  First off, do a "zdump GMT" to find out what GMT the system thinks it is (e.g. mine says 15:23 at the moment).  "zdump EST" reports 10:23 while "zdump EST5EDT" reports a time of 11:23.  So... according to [time.gov](http://www.time.gov/), the eastern seaboard is currently 4 hours behind GMT.  Which means I should use EST5EDT to account for daylight savings time.  Use "zdump GMT" to verify that your GMT time is still correct after you set the local date.

ln -sf /usr/share/zoneinfo/EST5EDT /etc/localtime
date 04281528
zdump GMT

Picking a kernel is tough... (make sure to read [gentoo kernel guide](http://www.gentoo.org/doc/en/gentoo-kernel.xml)).   I could try the [epia kernal over at epiawiki.org](http://www.epiawiki.org/wiki/tiki-index.php?page=EpiaTheEpiaKernel), but they only have the 2.4 available and 2.6 has been out for a while.  I also need to remember to configure the kernel with [LVM support (step 13)](http://www.gentoo.org/doc/en/lvm2.xml).  Initial thinking is that I'm either going to go with development-sources or gs-sources (this is a development server, not a multimedia box).  You can get a list of sources by doing "emerge -s sources | less".  Also see [building an mp3 server](http://www.ath0.com/meta/prose/mp3-server/part3.html) for a discussion of some things.

"development-sources" is at 2.6.3 currently.  "gentoo-sources" is at 2.4.22-r7.  "gs-sources" is at 2.4.25_pre7-r2.  "hardened-sources" is at 2.4.24-r1.  "selinux-sources" is at 2.4.24-r2.

(flips a coin and goes with "development-sources")

# emerge development-sources

([next entry](/blog/2004-04-28-gentoo-epia-install-part-3/))
