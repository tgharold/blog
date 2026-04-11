---
layout: post
title: 'Gentoo Kernel Rebuild (samba support)'
date: '2004-05-01T04:15:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Trying to compile a new kernel with samba support built in... I'll install this one as a different kernel image in the /boot folder.  (See the [Gentoo handbook](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=7) for details on what is going on here.)

# cd /usr/src/linux 
# make menuconfig

Go to File Systems, Network File Systems, and turn ON the SMB file system support.  Exit and save.

# make &amp;&amp; make modules_install

# mount /dev/hda1 /boot

# cp arch/i386/boot/bzImage /boot/kernel-2.6.3-20040501-samba
# cp System.map /boot/System.map-2.6.3-20040501-samba
# cp .config /boot/config-2.6.3-20040501-samba

Now, [edit the grub configuration file](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=9) (/boot/grub/grub.conf), and add the new kernel to the list.  Here's what my new grub config file looks like:

default 0
timeout 30

title=Gentoo Linux 2.6.3 (Samba Support, May 1 2004)
root (hd0,0)
kernel /kernel-2.6.3-20040501-samba root=/dev/hda2

title=Gentoo Linux 2.6.3
root (hd0,0)
kernel /kernel-2.6.3-gentoo root=/dev/hda2

By leaving a 30 second timeout and leaving the old kernel information in the config file, I have a bit of a window to flip back to the previous kernel if needed.  (Not my idea, saw it somewhere else on the web.)
