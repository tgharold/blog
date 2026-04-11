---
layout: post
title: 'Gentoo LVM2 stuff'
date: '2004-04-30T15:28:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---



<b>vgscan</b> - displays the list of volume groups allocated on the system (for my box, I have vgos, vguser, vgtmp and vgmedia)
<b>lvscan</b> - displays the list of virtual partitions inside of the volume groups (for my box, I have 6)
<b>vgdisplay</b> - displays a lot of data bout the volume groups, a good place to find out how much space is free within a particular volume group (vgos has 12GB free, vguser 19GB free, vgtmp 7GB free, vgmedia 92GB free).

Back when I setup the box, I never created any partitions (volumes?) inside the vgmedia volume group.  So now I want to think about what sort of media I'm going to be storing, and how to seperate it.  Since most audio/video files are larger, I may consider using a larger block size (if that makes sense?).  I'm also going to leave a small amount of space for backup files to be written to from the primary drive.  So for now, I'll only allocate 32GB out of the 92GB.

lvcreate -L32G -nmedia vgmedia
mke2fs -j -c /dev/vgmedia/media
(then use an editor to add an entry to the /etc/fstab table)
mkdir /media
mount /dev/vgmedia/media /media

Now I'm ready to configure Samba.  See the [gentoo documentation about Samba](http://www.gentoo.org/doc/en/desktop.xml#doc_chap7).
