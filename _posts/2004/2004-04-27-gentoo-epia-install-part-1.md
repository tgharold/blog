---
layout: post
title: 'Gentoo EPIA Install (part 1)'
date: '2004-04-27T16:54:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


So... [time to install Gentoo](http://www.gentoo.org/doc/en/handbook/index.xml) (also see [epiawiki.org - Installing Gentoo on an EPIA system](http://www.alterself.com/~epia/wiki/tiki-index.php?page=EpiaInstallingGentoo)).  A good book to have handy during the install is "Linux in a Nutshell", especially for looking up option flags for the various commands.

Popped the boot CD ([Universal CD](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&chap=2) for 2004.0 Gentoo) in and let it boot up.  It reports my hardware as a "VIA Samuel 2 599MHz, 64KB cache".  It's now sitting at the '#' prompt (er, shell prompt).  When I was setting up the BIOS, I changed the shared memory for the video card from 128MB (default) to 32MB.  I also disabled things like the audio ports, serial ports, parallel port, leaving only ethernet, firewire and USB.

Looking at the content of /dev/ ("cd /dev", "ls -l hd*"), I see that I have (3) hard disk devices (DVD-ROM counts as a "hd" device) labeled hda, hdc and hdd.  "hda" is my primary IDE, master drive (the 7200rpm 80GB).  "hdc" is my secondary IDE, master drive (the 5400rpm 120GB).  "hdd" is my DVD-ROM.  Each of the two hard-drives have 1 partition each (hda1 and hdc1) which I'll be wiping out when I setup Gentoo.   Using the "hdparm -i /dev/hda" command will display a quick summary about hda.

[Verify networking](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&chap=3) using "/sbin/ifconfig".  My box automatically grabbed a DHCP address from my network's DHCP server so I'm good to go.

Time to partition the drive.  I actually planned this out [a few days ago](/2004-04-24-gentoo-partitioning-plans/), but I might make a few changes.  My plan is to use the primary disk for the operating system, and use the secondary disk for any temporary files and swap.  I also want to limit the amount of space set aside for the operating system and keep it all in a seperate area from any user-data to make backing up the config with Norton Ghost easier.  Things are a bit complicated as I plan on [using LVM to manage portions of the disk](http://www.gentoo.org/doc/en/lvm2.xml) instead of creating individual partitions for some things.  Basic steps that I did (have to exit out of fdisk using the 'w' command to switch drives):

1. Wipe out all partitions on /dev/hda and /dev/hdc
2. Create the boot partition on /dev/hda (primary, active, 64MB)
3. Create the swap partition on /dev/hdc (primary, 2048MB)
4. Create the root partition on /dev/hda (primary, 2048MB)
5. Create LVM partition #1 on /dev/hda (primary, 24576MB)
6. Create 2nd LVM partition on /dev/hda (primary, rest of disk)
7. Create backup root partition on /dev/hdc (primary, 2048MB)
8. Create 1st LVM partition on /dev/hdc (primary, 16384MB)
9. Create 2nd LVM partition on /dev/hdc (primary, rest of disk)

Basically, I have a 2GB root partition, a 2GB swap file, a 2GB backup root on the 2nd disk, 24GB of operating-system space on the primary disk, 16GB of temporary file space on the second disk.  User space on disk 1 is around 50GB and around 95GB on disk 2.  I plan on having (4) seperate LVM volume groups (vgos, vgtmp, vguser, vgmedia) rather then combining all (4) partitions into a single volume group.

Time to create the file systems, and setup the LVM volume groups.  Boot volume (/dev/hda1) is ext2, root (/dev/hda2) and root mirror (/dev/hdc2) are ext3.  Swap partition is /dev/hdc1, LVM partitions are vgos (/dev/hda3), vguser (/dev/hdd4), vgtmp (/dev/hdc3) and vgmedia (/dev/hdc4).

    mke2fs /dev/hda1
    mke2fs -j /dev/hda2
    mke2fs -j /dev/hdc2
    mkswap /dev/hdc1
    swapon /dev/hdc1
    pvcreate /dev/hda3 /dev/hda4 /dev/hdc3 /dev/hdc4
    vgcreate vgos /dev/hda3
    vgcreate vguser /dev/hda4
    vgcreate vgtmp /dev/hdc3
    vgcreate vgmedia /dev/hdc4

To create the logical volumes inside each volume group, I used the following commands.  "vgos" is going to hold /opt (2GB), /usr (4GB), and /var (4GB).  "vguser" is going to hold /home (32GB to start).  "vgtmp" is holding /tmp (4GB) and /var/tmp (4GB).

    lvcreate -L2G  -nopt vgos
    lvcreate -L4G  -nusr vgos
    lvcreate -L4G  -nvar vgos
    lvcreate -L32G  -nhome vguser
    lvcreate -L4G -ntmp vgtmp
    lvcreate -L4G -nvartmp vgtmp

    mke2fs -j /dev/vgos/opt
    mke2fs -j /dev/vgos/usr
    mke2fs -j /dev/vgos/var
    mke2fs -j /dev/vguser/home
    mke2fs /dev/vgtmp/tmp
    mke2fs /dev/vgtmp/vartmp

What fun!  Time to mount all of the volumes (no need to mkdir the "root" partition, which is why the first command here is a mount instead of a mkdir):

    mount /dev//hda2 /mnt/gentoo
    mkdir /mnt/gentoo/boot
    mount /dev/hda1 /mnt/gentoo/boot

Mount the LVM managed volumes:

    mkdir /mnt/gentoo/opt
    mount /dev/vgos/opt /mnt/gentoo/opt
    mkdir /mnt/gentoo/usr
    mount /dev/vgos/usr /mnt/gentoo/usr
    mkdir /mnt/gentoo/var
    mount /dev/vgos/var /mnt/gentoo/var
    mkdir /mnt/gentoo/home
    mount /dev/vguser/home /mnt/gentoo/home

Mounting the two temporary folders requires special permissions to be set (per chapter 4e of the handbook).

    mkdir /mnt/gentoo/tmp
    mount /dev/vgtmp/tmp /mnt/gentoo/tmp
    chmod 1777 /mnt/gentoo/tmp

    mkdir /mnt/gentoo/var/tmp
    mount /dev/vgtmp/vartmp /mnt/gentoo/var/tmp
    chmod 1777 /mnt/gentoo/var/tmp

And the "proc" file system (last bit of chapter 4e in the handbook)

    mkdir /mnt/gentoo/proc
    mount -t proc none /mnt/gentoo/proc

Taking a break for a bit. ([continued in next post](/blog/2004-04-27-gentoo-epia-install-part-2/))
