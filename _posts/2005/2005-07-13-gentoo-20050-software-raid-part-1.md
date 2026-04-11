---
layout: post
title: 'Gentoo 2005.0 Software RAID (part 1)'
date: '2005-07-13T12:37:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---



<i>Note: As always, these are works-in-progress.  They might work, or they might not and are mostly here so that I can keep track of what I did or didn't do during an install.</i>

Gentoo 2005.0 Software RAID (part 1) - Going to try again with Gentoo 2005.0 in a software RAID with LVM configuration.  There's a [post](http://forums.gentoo.org/viewtopic-t-358713.html) on the Gentoo forums that indicates it may now be possible to get it up and running (seems to indicate there was a bug with kernels prior to 2.6.12).

The hardware that I'm using is a [VIA EPIA ME6000](/blog/2005-03-29-gentoo-epia-install-part-1/) (full details).  Basically 2x160GB drives, which will be mirrored.  

Start with the usual first steps (I prefer to ssh into my box during the build, it allows me to keep a log file of all commands, errors, etc.).

1) Boot the system using the Universal CD
2) ifconfig - find out the IP address of the box
3) passwd - change the root password to something you know
4) Start the SSH daemon - /etc/init.d/sshd start

Then I SSH in using SecureCRT and start my install.

As always, I start by blowing away any existing partitions by using "fdisk" or Derik's Boot and Nuke (a bootable CD which you can use to erase hard drives).  Then I'll re-create my partitions and start in on the installation.

<code># fdisk /dev/hda

Command: n
Command action: p
Partition number: 1
First cylinder: 1
Last cylinder: +128M
Command: a
Partition number: 1
Command: t
Hex code: fd

Command: n
Command action: p
Partition number: 2
First cylinder: [enter]
Last cylinder: +2048M
Command: t
Partition number: 2
Hex code: fd

Command: n
Command action: p
Partition number: 3
First cylinder: [enter]
Last cylinder: +2048M
Command: t
Partition number: 3
Hex code: fd

Command: n
Command action: p
First cylinder: [enter]
Last cylinder: [enter]
Command: t
Partition number: 4
Hex code: fd

Command: p

Command: w</code>

This gives me a 128MB boot area, a 2GB swap area, a 2GB root area, with the rest of the disk set aside for my LVM partitions. Repeat the above commands to configure the 2nd disk in the same fashion. Note that I'm using a different partition type then that shown in chapter 4.c. The 'fd' partition type is what I need to use since all 4 partitions on hda/hdc are going to be put into a software RAID1 set.

<i>(Eventually ran out of time to get this working due to other projects, now waiting on 2005.1 release.)</i>
