---
layout: post
title: 'Gentoo and Software RAID (2004.3)'
date: '2005-04-19T11:04:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Going back to the 2004.3 Gentoo Universal boot CD.  Trying to get past my previous issue [bd_claim issues when setting up a software RAID](/blog/2005-03-31-installing-gentoo-on-software-raid/).  This is on my Gigabyte GA-6VA7+ motherboard ([notes on the Gigabyte GA-6VA7+ motherboard and other hardware](/blog/2005-03-31-gentoo-20050-on-gigabyte-ga-6va7-part-1/)).

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

Command: w
```

This gives me a 128MB boot area, a 2GB swap area, a 2GB root area, with the rest of the disk set aside for my LVM2 partitions. Repeat the above commands to configure the 2nd disk in the same fashion (/dev/hdc for me).

Now I need to configure software RAID.  This is a bit easier then last year since I don't need to muck with the /etc/raidtab file (instead, I'm going to use mdadm).

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

```
# modprobe raid1
# mdadm --create /dev/md0 --level=1 --raid-devices=2 /dev/hda1 /dev/hdc1 
mdadm: array /dev/md0 started.
# mdadm --create /dev/md1 --level=1 --raid-devices=2 /dev/hda2 /dev/hdc2
mdadm: array /dev/md1 started.
# cat /proc/mdstat
Personalities : [raid1] 
md1 : active raid1 hdc2[1] hda2[0]
      2000256 blocks [2/2] [UU]
      [==>..................]  resync = 13.8% (277760/2000256) finish=3.6min speed=7920K/sec
md0 : active raid1 hdc1[1] hda1[0]
      125376 blocks [2/2] [UU]

unused devices: <none>
```

Seems to be working fine.  Once each RAID set finishes initialization, I'll create the next one in the series using the following commands:

```
# mdadm --create /dev/md2 --level=1 --raid-devices=2 /dev/hda3  /dev/hdc3
# mdadm --create /dev/md3 --level=1 --raid-devices=2 /dev/hda4 /dev/hdc4
```

The last RAID set will take a while to initialize (2 hours?), so I'm going to go work on other things while it runs.  I also need to go back and review the documentation to see what else I need to do when doing software RAID.
