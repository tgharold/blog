---
layout: post
title: 'Gentoo EPIA Install (part 6)'
date: '2004-04-28T22:28:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


([previous entry](/techblog/2004/04/gentoo-epia-install-part-5.shtml))

Now to start with [chapter 7e, installing extra kernel modules](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=7).  I didn't see any extra modules that needed to be emerge'd, so I skipped straight to the editing of the autoload file.  Actually I lie, I have to add in LVM2 module support.  So I need to follow the steps in [step 13 of the LVM install guide](http://www.gentoo.org/doc/en/lvm2.xml) and add LVM to the auto-load listing.

nano -w /etc/modules.autoload.d/kernel-2.6

Oh boy, a big empty file.  I know I need to add LVM here ("dm-mod"), plus building the LVM package ("emerge lvm2") and configuring lvm to not auto-probe the CD-ROM ("echo 'devices { filter=["r/cdrom/"] }' &gt;&gt; /etc/lvm/lvm.conf").  For now, I added the "dm-mod" line, exited out and did the emerge for LVM2.  (FYI, I didn't have an lvm directory under /etc so I had to mkdir /etc/lvm before I could run the echo command.)

Looking at the contents of my /lib/modules/2.6.3/kernel folder using the find command shows the following modules:

crypt modules: aes.ko, blowfish.ko, cast5.ko, cast6.ko, crypto_null.ko, deflate.ko, des.ko, md4.ko, md5.ko, serpent.ko, sha1,ko, sha256.ko, sha512.ko, tcrypt.ko, twofish.ko

drivers/md/dm-mod.ko
drivers/net/dummy.ko
lib/zlib_deflate/zlib_deflate.ko
lib/zlib_inflate/zlib_inflate.ko

Not sure why modules like mii, via-rhine, and the like aren't in the /lib/modules tree, could be a goof-up.

Following the [sample autoload file from the MP3 server article](http://www.ath0.com/meta/prose/mp3-server/kernel-2.6), I ended up with the following lines in my config file:

#LVM2
dm-mod

#ethernet
mii
via-rhine

#firewire
ieee1394    
ohci1394 

#usb
usbcore     
uhci        
ehci-hcd    
usb-storage

Don't forget to run "modules-update" when done.  Onward to [chapter 8, configuring your system](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=8).  First up is editing the "/etc/fstab" table, which controls what gets mounted at startup.  I'm using a rather complex partitioning system, plus LVM2, so this will look a bit wild.  It also helps to [refer back to the mount commands used earlier](/techblog/2004/04/gentoo-epia-install-part-4.shtml).

/dev/hda1 /boot ext2 noauto,noatime 1 2
/dev/hda2 / ext3 natime 0 1
/dev/hdc1 none swap sw 0 0
/dev/cdroms/cdrom0 /mnt/cdrom auto noauto,user 0 0

/dev/vgos/opt /opt ext3 noatime 0 3
/dev/vgos/usr /usr ext3 noatime 0 3
/dev/vgos/var /var ext3 noatime 0 3
/dev/vguser/home /home ext3 noatime 0 0
/dev/vgtmp/tmp /tmp ext2 noatime 0 3
/dev/vgtmp/vartmp /var/tmp ext2 noatime 0 3

none /proc proc defaults 0 0
none /dev/shm tmpfs defaults 0 0

Next, do your hostname and dnsdomainname settings (/etc/hostname and /etc/dnsdomainname) and run the "rc-update add domainname default" command.  Edit your networking ("nano -w /etc/conf.d/net").  Most folks probably use DHCP, but I configured a static address (the iface_eth0 line) as well as uncommenting and configuring the gateway line.  Save and exit, then use "rc-update add net.eth0 default" to add networking to the default runlevel.  Also "cat /etc/resolv.conf" and see if your DNS servers are properly listed (only do this if you used a static IP address like I did, if you're using DHCP those will be automatically set).

The next big task is to edit the local configuration ("nano -w /etc/rc.conf").  I'll only list the changes that I made:

CLOCK="local"

Yeah... big changes!  Er, yah, um onward to [chapter 9, configuring the bootloader](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=9).

I'm 99% sure I didn't turn on frame-buffer support, so skip the first section.  I'm also going to use GRUB instead of LILO (personal preference and I've heard that GRUB isn't as fragile as LILO, but on a single-boot system that might be a moot point).

emerge --usepkg grub
(wait a few minutes)
grub

grub&gt; root (hd0,0)
grub&gt; setup (hd0)
grub&gt; quit

The above assumes that your /boot partition is on /dev/hda1 (convert the 'hda' to 'hd0' and subtract 1 from '1' to get '0').  Edit your grub config file using "nano -w /boot/grub/grub.conf" and follow along in the [second half of 9b, configuring grub](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=9).  Here's what mine ended up looking like:

default 0
timeout 30
title=Gentoo Linux 2.6.3
root (hd0,0)
kernel /kernel-2.6.3-gentoo root=/dev/hda2

Save, exit, on to [chapter 10, installing the system tools](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=10).  I went with a lot of defaults here, just going to short-list the commands.  (Info on [dcron](http://www.linuxfromscratch.org/hints/downloads/files/dcron.txt).)

emerge syslog-ng
rc-update add syslog-ng default
emerge dcron
rc-update add dcron default
crontab /etc/crontab

Okay, looks like getting close to the end.  [Chapter 11, finalizing the install](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=11).

passwd
useradd john -m -G users,wheel,audio -s /bin/bash
passwd john

exit
cd /
umount ... (insert list of mounted file systems)
reboot

Reboot, go into the BIOS and change the boot order to bypass the CD-ROM (or simply remove the LiveCD), and refer to [chapter 12, where do I go from here](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=12) in the gentoo handbook.  I might jot down some additional notes in the future, but we'll have to see.
