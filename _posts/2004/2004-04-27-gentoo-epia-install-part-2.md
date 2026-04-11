---
layout: post
title: 'Gentoo EPIA Install (part 2)'
date: '2004-04-27T18:31:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Picking up at [chapter 5c of the Gentoo Handbook, Using a Stage from the LiveCD](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=5).  (Also see my [previous post](/techblog/2004/04/gentoo-epia-install-part-1.shtml) where I configured the disks.)  Here is where it gets fun...  I'm going to try starting with the x86 stage1 file:

cd /mnt/gentoo
tar -xvjpf /mnt/cdrom/stages/stage1-x86-20040218.tar.bz2

That will extract a *whole* bunch of stuff onto your system, pickup with chapter 5d in the handbook.  Next, I grabbed the snapshot of the portage folder off the CD-ROM and stuck it in /mnt/gentoo/usr.

tar -xvjf /mnt/cdrom/snapshots/portage-20040223.tar.bz2 -C /mnt/gentoo/usr
mkdir /mnt/gentoo/usr/portage/distfiles
cp /mnt/cdrom/distfiles/* /mnt/gentoo/usr/portage/distfiles/

That populates the /mnt/gentoo/usr/portage tree, also copies all of the source code off of the CD-ROM.  Onward to chapter 5e (configuring the compiler).  Use "nano -w /mnt/gentoo/etc/make.conf" to pull up the make.conf file.  Here's what mine looked like by default:

CFLAGS="-O2 -mcpu=i686 -fomit-frame-pointer"
CHOST="i386-pc-linux-gnu"
USE=""
CXXFLAGS="$(CFLAGS)"

Now, [supposedly GCC 3.3 allows](http://www.epiawiki.org/wiki/tiki-index.php?page=EpiaInstallingGentoo) the use of "-march=C3".  You may also want to look at /mnt/gentoo/etc/make.conf.example and poke around the documentation in there.  Looks like you use <b>either</b> "-march=XXX" or "-mcpu=XXX", not both at the same time.  Doing a bit of googling, looks like the Gentoo 2004.0 universal CD does not come with GCC 3.3.2 so the "-march=C3" won't work.  The twiki also indicates a preference for "-Os" instead of the other optimization levels due to the small (64KB) cache on the C3 processor.  I'm going to try the following (notice that I changed CHOST as well):

CFLAGS="-Os -march=i586 -m3dnow -fomit-frame-pointer"
CHOST="i586-pc-linux-gnu"
USE=""
CXXFLAGS="$(CFLAGS)"

Onward to step 6, [Installing the Gentoo Base System](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=6).  The mirrorselect application chose "pair.com" as my mirror (which is fine, that's where I downloaded the ISOs from).  Alternate site is datapipe.net.  Not going to muck with the default USE flags at the moment, instead I'm going to step right into 6c (progressing from stage1 to stage2).  This will take a while (if it works!).
