---
layout: post
title: 'Gentoo AMD64 on Asus M2N32-SLI Deluxe (part 2)'
date: '2006-08-25T20:35:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


As I said [last time](/blog/2006-08-25-gentoo-amd64-on-asus-m2n32-sli-deluxe-part-2/), I'm setting this unit up with the following partitions on the 2-disk RAID1 set (sda and sdb):

sda1 (md0) - 128MB for /boot
sda2 (md1) - 8GB for the root partition (primary)
sda3 (md2) - 8GB for a root partition (backup operating system)
sda4 - place-holder for extended partition
sda5 (md3) - 4GB swap file partition
sda6 (md4) - 679GB in LVM2 volume group (vgmirror)

Since I already created the RAID arrays last time, this time I only need to start up the RAID sets.

```
# modprobe md
# modprobe raid1
# for i in 0 1 2 3 4; do mknod /dev/md$i b 9 $i; done
# mdadm --assemble /dev/md0 /dev/sda1 /dev/sdb1
# mdadm --assemble /dev/md1 /dev/sda2 /dev/sdb2
# mdadm --assemble /dev/md2 /dev/sda3 /dev/sdb3
# mdadm --assemble /dev/md3 /dev/sda5 /dev/sdb5
# mdadm --assemble /dev/md4 /dev/sda6 /dev/sdb6
```

The LVM2 area on /dev/md4 is already created as well:

```
# modprobe dm-mod
# pvscan
  PV /dev/md4   VG vgmirror   lvm2 [679.39 GB / 679.39 GB free]
  Total: 1 [679.39 GB] / in use: 1 [679.39 GB] / in no VG: 0 [0   ]
# vgscan
  Reading all physical volumes.  This may take a while...
  Found volume group "vgmirror" using metadata type lvm2
```

Create the basic mdadm configuration file.  While mdadm is able to figure out most things automatically, it's useful to give it hints.

```
# mdadm --detail --scan &gt;&gt; /etc/mdadm.conf
# vi /etc/mdadm.conf
```

Here's my mdadm.conf file.  Notice the use of UUIDs by mdadm to ensure that it always matches up the correct partitions with the mdadm device numbers.  This also should ensure that the mdadm device numbers never change.

```
ARRAY /dev/md4 level=raid1 num-devices=2 UUID=9b76e544:c3775946:1458656b:c78ce692
ARRAY /dev/md3 level=raid1 num-devices=2 UUID=a441836c:a3801fed:a6e616da:dd829ebc
ARRAY /dev/md2 level=raid1 num-devices=2 UUID=84c2076e:edd3ceaf:595ae236:381044ca
ARRAY /dev/md1 level=raid1 num-devices=2 UUID=b4da9f10:265c3868:db128369:583c900e
ARRAY /dev/md0 level=raid1 num-devices=2 UUID=ada9bc71:2044d255:74204255:b1ba5cd1
```

Next we create the file systems:

```
livecd / # mke2fs /dev/md0
livecd / # mke2fs -j /dev/md1
livecd / # mke2fs -j /dev/md2
livecd / # mkswap /dev/md3 ; swapon /dev/md3
livecd / # mount /dev/md1 /mnt/gentoo
livecd / # mkdir /mnt/gentoo/boot ; mount /dev/md0 /mnt/gentoo/boot
```

For the LVM2 volumes, things are a bit more complex.  The majority of the action is going to take place inside of the root volumes since we are only doing a minimal build on order to prep for a Xen Domain0 kernel.  However, there are a few volumes that are worthwhile placing in LVM so that they are available to both the primary and the backup operating system.  (Mostly /home and /usr/portage along with the temporary volumes.)

```
# lvcreate -L2G -ntmp vgmirror
# lvcreate -L2G -nvartmp vgmirror
# lvcreate -L2G -nhome vgmirror
# lvcreate -L4G -nportage vgmirror
# ls -l /dev/vgmirror
# lvscan
# mke2fs /dev/vgmirror/tmp
# mke2fs /dev/vgmirror/vartmp
# mke2fs -j /dev/vgmirror/home
# mke2fs -j /dev/vgmirror/portage
# mkdir /mnt/gentoo/tmp ; mount /dev/vgmirror/tmp /mnt/gentoo/tmp
# chmod 1777 /mnt/gentoo/tmp
# mkdir /mnt/gentoo/var 
# mkdir /mnt/gentoo/var/tmp ; mount /dev/vgmirror/vartmp /mnt/gentoo/var/tmp
# chmod 1777 /mnt/gentoo/var/tmp
# mkdir /mnt/gentoo/home ; mount /dev/vgmirror/home /mnt/gentoo/home
# mkdir /mnt/gentoo/usr
# mkdir /mnt/gentoo/usr/portage ; mount /dev/vgmirror/portage /mnt/gentoo/usr/portage
```

Now for the supplementary volumes (logs, subversion and system backup).  I'm using separate volumes for the log files of the primary vs secondary operating system.  The secondary (backup) O/S only gets 1GB of space for its log files.

```
# lvcreate -L4G -nlog1 vgmirror
# lvcreate -L1G -nlog2 vgmirror
# lvcreate -L2G -nsvn vgmirror
# lvcreate -L16G -nbackupsys vgmirror
# mke2fs -j /dev/vgmirror/log1
# mke2fs -j /dev/vgmirror/log2
# mke2fs -j /dev/vgmirror/svn
# mke2fs -j /dev/vgmirror/backupsys
# mkdir /mnt/gentoo/var/log ; mount /dev/vgmirror/log1 /mnt/gentoo/var/log
# mkdir /mnt/gentoo/var/svn ; mount /dev/vgmirror/svn /mnt/gentoo/var/svn
# mkdir /mnt/gentoo/backup
# mkdir /mnt/gentoo/backup/system ; mount /dev/vgmirror/backupsys /mnt/gentoo/backup/system
```

Whew, that's a big packet of LVM partitions.  But it prevents problems down the road.

At this point, everything is setup and ready for the initial install (or a chroot into an existing system for repairs).
