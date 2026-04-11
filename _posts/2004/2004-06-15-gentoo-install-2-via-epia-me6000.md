---
layout: post
title: 'Gentoo Install 2 (VIA EPIA ME6000)'
date: '2004-06-15T15:53:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>([Previous post about fdisk and setting up the software RAID](/techblog/2004/06/gentoo-install-1-via-epia-me6000.shtml).)

At this point, we've partitioned the disk and setup the "/etc/raidtab" file.  It's a good idea to jot down everything in that file and put it in a safe place.  You should also "cat /proc/mdstat" and jot that information down too.

The following commands will format the boot and root partitions (/dev/md0 is /boot, /dev/md2 is /).  I'll also be setting up the swap on /dev/md1.  Since we're doing RAID1, there's no need to use the "-R stride=<i>n</i>" option of mke2fs (that's only useful for RAID0, RAID4 or RAID5).  Note that you must mount the "/" (root) partition <b>before</b> creating and mounting the boot folder within that tree.
<pre># mke2fs /dev/md0
# mke2fs -j /dev/md2
# mkswap /dev/md1
# swapon /dev/md1
# mount /dev/md2 /mnt/gentoo
# mkdir /mnt/gentoo/boot
# mount /dev/md0 /mnt/gentoo/boot</pre>

Next, initialize the 4th RAID set in preparation for LVM (pvcreate).  Create the "/etc/lvm/lvm.conf" file and create the volume group for the 4th RAID set (vgcreate).  Also see the [Gentoo LVM documentation](http://www.gentoo.org/doc/en/lvm2.xml).  If needed, use "<b>modprobe dm-mod</b>" to load the LVM module.
<pre># pvcreate /dev/md3
# echo 'devices { filter=["r/cdrom/"] }' &gt;/etc/lvm/lvm.conf
# vgcreate vgmirror /dev/md3
# vgscan</pre>

Now we need to create some logical volumes inside our "vgmirror" volume group.  Here's a list of my initial logical volumes:

4GB /tmp (ext2)
4GB /var/tmp (ext2)
2GB /opt (ext3)
4GB /usr (ext3)
4GB /var (ext3)
8GB /home (ext3)

Create the logical volumes using "lvcreate", then verify by looking in the "/dev/vgmirror" folder as well as "<b>lvscan</b>":
<pre># lvcreate -L4G -ntmp vgmirror
# lvcreate -L4G -nvartmp vgmirror
# lvcreate -L2G -nopt vgmirror
# lvcreate -L4G -nusr vgmirror
# lvcreate -L4G -nvar vgmirror
# lvcreate -L8G -nhome vgmirror
# ls /dev/vgmirror
# lvscan</pre>

Now, format the logical volumes with the desired filesystems.
<pre># mke2fs /dev/vgmirror/tmp

# mke2fs /dev/vgmirror/vartmp
# mke2fs -j /dev/vgmirror/opt
# mke2fs -j /dev/vgmirror/usr
# mke2fs -j /dev/vgmirror/var
# mke2fs -j /dev/vgmirror/home</pre>

Make the directories to hold your mounted volumes.  Mount your volumes.
<pre># mkdir /mnt/gentoo/opt
# mkdir /mnt/gentoo/usr
# mkdir /mnt/gentoo/var
# mkdir /mnt/gentoo/home
# mount /dev/vgmirror/opt /mnt/gentoo/opt
# mount /dev/vgmirror/usr /mnt/gentoo/usr
# mount /dev/vgmirror/var /mnt/gentoo/var
# mount /dev/vgmirror/home /mnt/gentoo/home</pre>

Make the special directories to hold your temp file volumes (these require special permissions).  Then mount your temp file volumes.  Also mount your proc folder.
<pre>
# mkdir /mnt/gentoo/tmp
# mount /dev/vgmirror/tmp /mnt/gentoo/tmp
# chmod 1777 /mnt/gentoo/tmp
# mkdir /mnt/gentoo/var/tmp
# mount /dev/vgmirror/vartmp /mnt/gentoo/var/tmp
# chmod 1777 /mnt/gentoo/var/tmp
# mkdir /mnt/gentoo/proc
# mount -t proc none /mnt/gentoo/proc</pre>

We are now ready to [start installing Gentoo](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=5) (chapter 5 in the handbook).  Also see my [previous post about CFLAGS](http://www.tgharold.com/techblog/2004/04/gentoo-epia-install-part-2.shtml), which might explain why I've chosen some particular settings.  First, we need to extract the stage 1 tarball.
<pre># date
# ls /mnt/cdrom/stages
# cd /mnt/gentoo
# tar -xvjpf /mnt/cdrom/stages/stage1-x86-20040218.tar.bz2
# ls /mnt/cdrom/snapshots
# tar -xvjf /mnt/cdrom/snapshots/portage-20040223.tar.bz2 -C /mnt/gentoo/usr
# mkdir /mnt/gentoo/usr/portage/distfiles
# cp /mnt/cdrom/distfiles/* /mnt/gentoo/usr/portage/distfiles/
# nano -w /mnt/gentoo/etc/make.conf</pre>

Now we need to configure the base compile options.  Here's the content of my make.conf file (<b>use at your own risk</b>).  Be sure to go look at [5.e. Configuring the Compile Options](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=5) in the Gentoo Handbook.  Also look at [Gentoo USE flags](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=2&amp;chap=1) and [Gentoo Linux USE Variable Descriptions](http://www.gentoo.org/dyn/use-index.xml).  I've set some very aggressive USE flags in my make.conf file (anything to do with graphics or multimedia since this is a headless file server) and I don't know whether it's proper to remove all of those USE flags yet.  Note that even though the USE= line shown here is spread across two lines, it should be all one line in the actual make.conf file (the line break here is for visual clarity only).
<pre>CFLAGS="-Os -march=i586 -m3dnow -fomit-frame-pointer"
CHOST="i586-pc-linux-gnu"
USE="apache2 kerberos ldap -apm -gif -gnome -gtk -jpeg -kde -mad -mikmod -mpeg 
-oggvorbis -opengl -oss -pdflib -png -qt -quicktime -sdl -truetype -xmms -xv"
CXXFLAGS="$(CFLAGS)"
MAKEOPTS="-j2"</pre>

Next we're ready to install the base system, see [6. Installing the Gentoo Base System](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=6) in the Gentoo Handbook.
<pre># mirrorselect -a -s4 -o | grep -ve '^Netselect' &gt;&gt; /mnt/gentoo/etc/make.conf
# cp -L /mnt/gentoo/etc/make.conf /mnt/gentoo/boot/make.conf-backupcopy
# cp -L /etc/resolv.conf /mnt/gentoo/etc/resolv.conf
# cp -L /etc/raidtab /mnt/gentoo/etc/raidtab
# cp -L /etc/raidtab /mnt/gentoo/boot/raidtab-backupcopy
# mkdir /mnt/gentoo/etc/lvm
# cp -L /etc/lvm/lvm.conf /mnt/gentoo/etc/lvm/lvm.conf
# cp -L /etc/lvm/lvm.conf /mnt/gentoo/boot/lvm.conf-backupcopy
# chroot /mnt/gentoo /bin/bash
# env-update
# source /etc/profile
# emerge sync</pre>

Synchronization of the portage tree will take a while (depending on the speed of your internet connection and how fast your system is).  My system downloaded 60MB or so worth of updates and took 30-60 minutes (at a guess).  Meanwhile, I'll continue this topic in [my next post](/techblog/2004/06/gentoo-install-3-bootstrapping.shtml).<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2004.shtml">2004</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Gentoo.shtml">Gentoo</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/VIAEPIA.shtml">VIAEPIA</a>
		<div class="Byline">
			posted by Thomas at 
			[15:53](http://www.tgharold.com/techblog/2004/06/gentoo-install-2-via-epia-me6000.shtml)

		</div>