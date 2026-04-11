---
layout: post
title: 'Gentoo Install Troubleshooting'
date: '2004-04-29T00:24:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Spoke too soon in my [last post](/blog/2004-04-28-gentoo-epia-install-part-6/).  Got a few errors on boot up.  First off, a complaint that the kernel was compiled without DEVFS support (not sure what that means off-hand), and none of my LVM2 stuff loaded.  Too tired to poke at it tonight, so I'm going to take a break and do some searching tomorrow.

I don't expect it to be difficult to resolve, might have to rebuild the kernel and reinstall the kernel.  During bootup, it tells me details about what needs to be done to fix the issue, but that's since scrolled off the screen.  Since my LVM2 volumes didn't mount, I can't look at /var/log/messages to see the boot messages.  Had to hard-reset since shutdown/reboot commands are hosed.

Okay, specific error message notes as the boot screen flies by:

GRUB is working, I get the boot selection screen with the 30 sec timer.  Error message that DEVFS support is required to be built into the kernel.  Not much other details then that.  I then get a bunch of messages that various LVM2-hosted file systems did not mount properly (No such file or directory while trying to open /dev/.../ and complaints about missing superblocks).  According to [google for DEVFS](http://www.google.com/search?q=linux+kernel+DEVFS+support&btnG=Search&hl=en&lr=&ie=UTF-8&oe=UTF-8&c2coff=1), it stands for "device file system".  

So... time to put the LiveCD back in, walk through the commands to get me back to the building a kernel stage:

    mount /dev//hda2 /mnt/gentoo
    mount /dev/hda1 /mnt/gentoo/boot
    mount -t proc none /mnt/gentoo/proc 

    modprobe dm-mod
    vgchange -ay

    mount /dev/vgos/opt /mnt/gentoo/opt
    mount /dev/vgos/usr /mnt/gentoo/usr
    mount /dev/vgos/var /mnt/gentoo/var
    mount /dev/vguser/home /mnt/gentoo/home
    mount /dev/vgtmp/tmp /mnt/gentoo/tmp
    mount /dev/vgtmp/vartmp /mnt/gentoo/var/tmp 

    chroot /mnt/gentoo /bin/bash
    env-update
    source /etc/profile 

At this point, I'm back to where I'm ready to configure the kernel ([previous attempt](/blog/2004-04-28-gentoo-epia-install-part-5/)).  I don't need to emerge the kernel sources again (AFAIK), just reconfigure.  Flip back to [chapter 7c in the gentoo handbook](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&chap=7).  I think my old configuration should be in /usr/src/linux/.config (that's a hidden file).  First thing I did was make a copy of that file "cat .config >> my-first-config".  Then I did the "make menuconfig" command, which did load my existing settings from the .config file.

Under (F)ile systems, (P)seudo filesystems, I had to turn on "/dev file system suppport (OBSOLETE)".  Apparently, while obsolete, it's still required by 2.6.3.  I also turned on "Automatically mount at boot".  Exited, saved changes, re-make the kernel, re-install the kernel.

Then cross my fingers and reboot... and it boots!  Saw a few errors related to USB/Firewire devices - I may go back into the module autoload file and remove the USB/firewire stuff (don't need).  

Other things to do:

- Look at /var/run/shutdown.pid, figure out where to stick the umount commands for all of my volumes when I use the shutdown command.  Also mentioned is /dev/initctl.
