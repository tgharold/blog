---
layout: post
title: 'Gentoo 2005.1 Software RAID (part 1)'
date: '2005-09-07T13:03:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---



<b>Note: These directions are works-in-progress... in fact, they might not even work at all.  The big change that I'm trying this time around is using the 2005.1 release.  I'm also going to skip LVM2 on the initial installation.  I'm now in the process of updating this to include instructions for both with and without LVM2.</b>

Now that the 2005.1 release is out, I'm going to take yet another swing at getting a software RAID configuration up and running on a pair of ATA disks. I'm working on two different systems.

<b>System A:</b> This is an older motherboard (AT power, 2 ISA slots, 3 PCI slots) running on a Celeron processor ([system details](/2005-03-31-gentoo-20050-on-gigabyte-ga-6va7-part-1/)).  But in the meantime, I've upgraded the disks to (3) 120GB 5400rpm drives (these run cooler then the old 7200rpm drives and will have less issues with heat).

<b>System B:</b> The second system is [VIA EPIA ME6000](/2005-03-29-gentoo-epia-install-part-1/) (EPIA M series), 600Mhz fanless CPU with a pair of 300GB PATA drives and a DVD-ROM.

Derik's Boot and Nuke (DBaN) seems like a good first step to make sure that any old data is wiped off of the 3 drives.  Data rates on the wipe process (running all 3 drives at the same time) is around 7.5MB/s per drive.  After having issues with an older configuration, I now always run DBaN for 2-3 passes with verification on all passes.  It drastically increases the amount of time required for the initial wipe but allows me to discover errors before I get into installing Gentoo.

Once that finishes running, I will have:

<b>System A:</b>
/dev/hda - 120GB primary IDE drive (Primary IDE channel, Master)
/dev/hdc - CD-ROM (Secondary IDE channel, Master)
/dev/hde - 120GB attached to Promise controller (PDC20262)
/dev/hdg - 120GB attached to Promise controller (PDC20262)

/dev/hda and /dev/hde will be mirrored together.  The /dev/hdeg disk will be used as a backup/scratch disk.

<b>System B:</b>
/dev/hda - 300GB IDE drive (Primary IDE channel, Master)
/dev/hdc - 300GB IDE drive (Secondary IDE channel, Master)
/dev/hdd - CD-ROM (Secondary IDE channel, Slave)

/dev/hda and /dev/hdc will be mirrored together.

Starting with the usual tricks:

1) Boot the system using the Universal CD
2) ifconfig - find out the IP address of the box
3) passwd - change the root password to something you know
4) Start the SSH daemon - /etc/init.d/sshd start

Since these drives were nuked since my last attempt, I have to re-configure the partitions.

```
# fdisk /dev/hda

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

(note that partition #3 can be different sizes based on needs)

Command: n
Command action: p
Partition number: 3
First cylinder: [enter]
Last cylinder: +16384M or +2048M
Command: t
Partition number: 3
Hex code: fd

Command: n
Command action: p
First cylinder: [enter]
Last cylinder: (use 99% of what's available)
Command: t
Partition number: 4
Hex code: fd

Command: p

Command: w
```

This gives me a 128MB boot area, a 2GB swap area, a root area, with the rest of the disk set aside for my LVM2 partitions. Repeat the above commands to configure the 2nd disk in the same fashion (/dev/hdc or /dev/hde for my 2 systems).

If you are not using LVM2 on the initial installation, I tend to use a 16GB root partition.  Otherwise if you are going to use LVM2 you can get away with a smaller 2GB root partition.

I always use a slightly smaller size for the 4th partition then the maximum available on the disk.  That will hopefully protect me if I would have to replace one of the drives with another one that is slightly smaller then expected.  (Not all 250GB drives are identical in the number of cylinders.)  A fudge-factor of around 1% of the total # of cylinders should be adequate.

Key resource: [HOWTO Gentoo Install on Software RAID](http://gentoo-wiki.com/HOWTO_Gentoo_Install_on_Software_RAID)

Now I need to configure software RAID. This is a bit easier then last year since I don't need to muck with the /etc/raidtab file (instead, I'm going to use mdadm).  This is based on research that I did while [using the 2004.3 CDs](/blog/2005-04-19-gentoo-and-software-raid-20043/)

The following loads the 'md' module and creates the nodes (/dev/md*).

```
# modprobe md
# ls /dev/md*
ls: /dev/md*: No such file or directory
# for i in 0 1 2 3; do mknod /dev/md$i b 9 $i; done
# ls /dev/md*
/dev/md0 /dev/md1 /dev/md2 /dev/md3
```

Now, we create our RAID1 sets.

<b>System A:</b>
```
# modprobe raid1
# mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/hda1 /dev/hde1
# mdadm --create /dev/md1 --level=1 --raid-devices=2 /dev/hda2 /dev/hde2
# mdadm --create /dev/md2 --level=1 --raid-devices=2 /dev/hda3 /dev/hde3
# mdadm --create /dev/md3 --level=1 --raid-devices=2 /dev/hda4 /dev/hde4
# cat /proc/mdstat
```

<b>System B:</b>
```
# modprobe raid1
# mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/hda1 /dev/hdc1
# mdadm --create /dev/md1 --level=1 --raid-devices=2 /dev/hda2 /dev/hdc2
# mdadm --create /dev/md2 --level=1 --raid-devices=2 /dev/hda3 /dev/hdc3
# mdadm --create /dev/md3 --level=1 --raid-devices=2 /dev/hda4 /dev/hdc4
# cat /proc/mdstat
```

Seems to be working fine. You can choose to wait until all of the RAID arrays finish processing (recommended) or press onward.

[LinuxDevCenter article on mdadm](http://www.linuxdevcenter.com/pub/a/linux/2002/12/05/RAID.html) explains mdadm in a bit more detail, and shows how to create the config file semi-automatically.  Be sure to change '/dev/hda' and 'dev/hde' to match the 2 disks that you are attempting to RAID.

```
# mdadm --detail --scan &gt;&gt; /etc/mdadm.conf
# nano -w /etc/mdadm.conf
```

Picking up again with [Chapter 4 of the installation handbook](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=4).  (This also matches what I did back in [June 2004 with Software RAID and LVM2](/blog/2004-06-15-gentoo-install-2-via-epia-me6000/) and [Gentoo 2004.3 on Gigabyte GA-6VA7+ (part 1)](/blog/2005-04-20-gentoo-20043-on-gigabyte-ga-6va7-part-3/).)

```
# mke2fs /dev/md0
# mkswap /dev/md1 ; swapon /dev/md1
# mke2fs -j /dev/md2
# mount /dev/md2 /mnt/gentoo
# mkdir /mnt/gentoo/boot ; mount /dev/md0 /mnt/gentoo/boot
```

If we're setting up LVM2, we need to now prep the 4th partition and setup the logical volumes inside of LVM2.

```
# modprobe dm-mod
# pvcreate /dev/md3
# echo 'devices { filter=["r/cdrom/"] }' &gt; /etc/lvm/lvm.conf
# vgcreate vgmirror /dev/md3
# vgscan
# lvcreate -L2G -ntmp vgmirror
# lvcreate -L2G -nvartmp vgmirror
# lvcreate -L2G -nopt vgmirror
# lvcreate -L4G -nusr vgmirror
# lvcreate -L2G -nvar vgmirror
# lvcreate -L2G -nhome vgmirror
# ls -l /dev/vgmirror
# lvscan
# mke2fs /dev/vgmirror/tmp
# mke2fs /dev/vgmirror/vartmp
# mke2fs -j /dev/vgmirror/opt
# mke2fs -j /dev/vgmirror/usr
# mke2fs -j /dev/vgmirror/var
# mke2fs -j /dev/vgmirror/home
# mkdir /mnt/gentoo/opt ; mount /dev/vgmirror/opt /mnt/gentoo/opt
# mkdir /mnt/gentoo/usr ; mount /dev/vgmirror/usr /mnt/gentoo/usr
# mkdir /mnt/gentoo/var ; mount /dev/vgmirror/var /mnt/gentoo/var
# mkdir /mnt/gentoo/home ; mount /dev/vgmirror/home /mnt/gentoo/home
# mkdir /mnt/gentoo/tmp ; mount /dev/vgmirror/tmp /mnt/gentoo/tmp
# chmod 1777 /mnt/gentoo/tmp
# mkdir /mnt/gentoo/var/tmp ; mount /dev/vgmirror/vartmp /mnt/gentoo/var/tmp
# chmod 1777 /mnt/gentoo/var/tmp
```

Now we move into [Installation (chapter 5)](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=5) in the handbook. Verify your system date and then start extracting the tarballs.  Notice that the only stage available on the Universal CD is now <b>stage3</b>.

```
# date
# ls -l /mnt/cdrom/stages
total 450586
-rw-r--r--  1 root root 92520704 Aug  7 04:45 stage3-athlon-xp-2005.1.tar.bz2
-rw-r--r--  1 root root 92413359 Aug  7 04:47 stage3-i686-2005.1.tar.bz2
-rw-r--r--  1 root root 92122771 Aug  7 04:46 stage3-pentium3-2005.1.tar.bz2
-rw-r--r--  1 root root 92475718 Aug  7 04:46 stage3-pentium4-2005.1.tar.bz2
-rw-r--r--  1 root root 91866585 Aug  7 04:46 stage3-x86-2005.1.tar.bz2
# cd /mnt/gentoo
# tar -xvjpf /mnt/cdrom/stages/stage3-x86-2005.1.tar.bz2
```

That takes a while to uncompress.  Now we pickup with 5D (Installing Portage).  I'm going to use the portage snapshot on the CD-ROM.

```
# cd /mnt/gentoo
# ls -l /mnt/cdrom/snapshot
# tar -xvjf /mnt/cdrom/snapshot/portage-2005.1.tar.bz2 -C /mnt/gentoo/usr
```

Before I configure the make.conf file, I should take a look at my system configuration.

```
# cat /proc/version
Linux version 2.6.12-gentoo-r6 (root@poseidon) (gcc version 3.3.5-20050130 (Gentoo 3.3.5.20050130-r1, ssp-3.3.5.20050130-1, pie-8.7.7.1)) #1 SMP Wed Aug 3 20:26:57 UTC 2005
# cat /proc/cpuinfo
processor       : 0
vendor_id       : GenuineIntel
cpu family      : 6
model           : 8
model name      : Celeron (Coppermine)
stepping        : 6
cpu MHz         : 568.141
cache size      : 128 KB
fdiv_bug        : no
hlt_bug         : no
f00f_bug        : no
coma_bug        : no
fpu             : yes
fpu_exception   : yes
cpuid level     : 2
wp              : yes
flags           : fpu vme de pse tsc msr pae mce cx8 sep mtrr pge mca cmov pat pse36 mmx fxsr sse
bogomips        : 1114.11
# cat /proc/meminfo
MemTotal:       320792 kB
MemFree:          7600 kB
Buffers:         57472 kB
Cached:         180320 kB
SwapCached:          4 kB
Active:          29596 kB
Inactive:       210948 kB
HighTotal:           0 kB
HighFree:            0 kB
LowTotal:       320792 kB
LowFree:          7600 kB
SwapTotal:     2007992 kB
SwapFree:      2000156 kB
Dirty:               0 kB
Writeback:           0 kB
Mapped:           5144 kB
Slab:            63636 kB
CommitLimit:   2168388 kB
Committed_AS:    15752 kB
PageTables:        172 kB
VmallocTotal:   704504 kB
VmallocUsed:      6856 kB
VmallocChunk:   696436 kB
```

Now to configure compile options (5E in the handbook).  Since we're using a stage3 installation, we'll need to be careful to not touch certain settings in the make.conf file.  I pretty much plan on using the defaults (except for optimizing for size due to the lower cache size in the Celeron and VIA CPUs, which is merely changing -O2 to -Os).  

```
# nano -w /mnt/gentoo/etc/make.conf
```

Contents of my make.conf file:

```
# These settings were set by the catalyst build script that automatically built this stage
# Please consult /etc/make.conf.example for a more detailed example
CFLAGS="-Os -mcpu=i686"
CHOST="i386-pc-linux-gnu"
CXXFLAGS="${CFLAGS}"
MAKEOPTS="-j2"
```

Now to [Chapter 6 - Installing the Gentoo Base System](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=6).  Time to "chroot".

```
# mirrorselect -i -o &gt;&gt; /mnt/gentoo/etc/make.conf
# mirrorselect -i -r -o &gt;&gt; /mnt/gentoo/etc/make.conf
# cat /mnt/gentoo/etc/make.conf
CFLAGS="-Os -mcpu=i686"
CHOST="i386-pc-linux-gnu"
CXXFLAGS="${CFLAGS}"
MAKEOPTS="-j2"

GENTOO_MIRRORS="http://gentoo.osuosl.org/"
SYNC="rsync://rsync.namerica.gentoo.org/gentoo-portage"
```

Looks good so far.

```
# cp -L /etc/resolv.conf /mnt/gentoo/etc/resolv.conf
# cp -L /etc/mdadm.conf /mnt/gentoo/etc/mdadm.conf
(do the next 2 commands if you are using LVM2)
# mkdir /mnt/gentoo/etc/lvm
# cp -L /etc/lvm/lvm.conf /mnt/gentoo/etc/lvm/lvm.conf
(end of optional LVM2 commands)
# mount -t proc none /mnt/gentoo/proc
# chroot /mnt/gentoo /bin/bash
# env-update
# source /etc/profile
# emerge --sync
```

The sync will take a while to run (I generally plan on doing something else for a few hours).

Time to choose a profile.  There shouldn't be much to do at this point since I plan on using the 2.6 kernel which is the default on the 2005.1 Gentoo CDs.

```
# ls -FGg /etc/make.profile
lrwxrwxrwx  1 48 Sep 21 10:22 /etc/make.profile -&gt; ../usr/portage/profiles/default-linux/x86/2005.1/
# ls -d /usr/portage/profiles/default-linux/x86/2005.1/2.4
/usr/portage/profiles/default-linux/x86/2005.1/2.4
```

Configuring the USE variable comes next in the handbook.  You'll see that I'm using a very aggressive set of USE flags that restrict a lot of options (since this is a headless server). You can see the [current list of USE flags](http://www.gentoo.org/dyn/use-index.xml) at the Gentoo.org site.  You can find the default set of USE flags via "cat /etc/make.profile/make.defaults".  The default listing in the 2005.1 profile is:

```
livecd / # ls -l /etc/make.profile
lrwxrwxrwx  1 root root 48 Oct 22 21:04 /etc/make.profile -&gt; ../usr/portage/profiles/default-linux/x86/2005.1
livecd / # cat /etc/make.profile/make.defaults
# Copyright 1999-2005 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: /var/cvsroot/gentoo-x86/profiles/default-linux/x86/2005.1/make.defaults,v 1.4 2005/08/29 22:20:25 wolf31o2 Exp $

USE="alsa apm arts avi berkdb bitmap-fonts crypt cups eds emboss encode fortran foomaticdb gdbm gif gnome gpm gstreamer gtk gtk2 imlib ipv6 jpeg kde libg++ libwww mad mikmod motif mp3 mpeg ncurses nls ogg oggvorbis opengl oss pam pdflib perl png python qt quicktime readline sdl spell ssl tcpd truetype truetype-fonts type1-fonts vorbis X xml2 xmms xv zlib"
livecd / # 
```

Here are my current customized USE flags (for a headless server with no GUI shell).

```
# less /usr/portage/profiles/use.desc
# echo 'USE="apache2 kerberos ldap postgres samba -alsa -apm -arts -bitmap-fonts -gnome -gtk -gtk2 -kde -mad -mikmod -motif -opengl -oss -qt -quicktime -sdl -truetype -truetype-fonts -type1-fonts -X -xmms -xv"' &gt;&gt; /etc/make.conf
# nano -w /etc/make.conf
```

The changes between this time and my last install are:

Added: postgres samba
Added: -alsa -arts -bitmap-fonts -gtk2 -mikmod -motif -truetype-fonts -type1-fonts -X
Removed: -gif -jpeg -mpeg -oggvorbis -pdflib -png 

Since I'm starting with a stage 3 tarball, I'm skipping directly to [7. Configuring the Kernel](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=7) in the handbook.

```
# ls /usr/share/zoneinfo
# ln -sf /usr/share/zoneinfo/EST5EDT /etc/localtime
# date
# zdump GMT
# zdump EST5EDT
```

Pick your kernel using the [kernel guide](http://www.gentoo.org/doc/en/gentoo-kernel.xml).  Last year, I went with development-sources for the kernel in order to get 2.6. This is no longer necessary (and development-sources has been rolled into vanilla-sources). So I'm going to go with the default gentoo-sources.

```
# emerge gentoo-sources
# ls -l /usr/src
```

Next up is configuring the kernel, which I'll cover in another post.
