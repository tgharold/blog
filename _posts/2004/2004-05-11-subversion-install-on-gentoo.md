---
layout: post
title: 'SubVersion install on Gentoo'
date: '2004-05-11T23:58:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Working on setting up subversion on the box.  I've already emerged in the apache and subversion ebuilds, now I'm working on some other configuration information.  My plan is to store my respository in /svn, in it's own logical volume.  (Very similar to when I [created my "media" logical volume in the vgmedia volume group](/techblog/2004/04/gentoo-lvm2-stuff.shtml).)

    # lvcreate -L4G -nsvn vguser 
    # mke2fs -j -c /dev/vguser/svn
    # mkdir /svn
    # mount /dev/vguser/svn /svn
    # nano -w /etc/fstab

[SubVersion book, chapter 6, section 4](http://svnbook.red-bean.com/svnbook/ch06s04.html) covers how to configure Apache2 for SVN.  One key thing that bit me is that if you already have apache2 installed, you need to <b>also set the apache2 USE flag</b> prior to emerging subversion.

More later... I have to wait for apache/subversion to re-emerge.
