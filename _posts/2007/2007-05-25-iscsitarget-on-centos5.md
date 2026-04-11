---
layout: post
title: 'iSCSITarget on CentOS5'
date: '2007-05-25T00:00:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Setting up our test iSCSI SAN box this week.  The original plans were to run this on top of Gentoo (which is very powerful and flexible) but after 3 years, I'm not very pleased with Gentoo as a server OS.  Which is a whole different topic.  So we've migrated over to using CentOS5, which is derived from Red Hat Enterprise Linux 5, a distro that is more suited for corporate use.

There's not much to talk about in terms of the base system.  It's a pretty vanilla 64bit CentOS5 install (from DVD) running on top of a dual-CPU dual-core pair of Socket F Opterons.  The primary packages that I've installed so far are "Yum Extender" (from stock repositories) and "rdiff-backup" (downloaded as an RPM).  The OS runs on top of a 3-disk RAID1 (mirror, all drives active) Software RAID for safety.

I use a semi-customized partition layout on the (3) operating system disks.  I have:

a) /boot
b) / (root, the primary OS install area)
c) swap
d) a backup root partition (which is basically a clone of the primary, except for a small change in /etc/fstab) designed for quick recovery from a situation that would hose the primary root partition
e) /var/log (broken out to its own area)
f) /backup/system (a place to store system backups)
g) LVM area (no allocated areas yet)

I mention all that because the first step before installing iscsitarget is to make sure I can recover if things go awry.  Since installing iscsitarget involves mucking with the running kernel, I want a good backup of /boot along with making sure GRUB offers me options to boot an older kernel.  I'll also freshen my root backup partition.

<b>Step 1 - Backing up /, /boot, and the existing kernel</b>

Simplicity is often best when dealing with the base OS.  My methods are crude, but designed to get me back up and running without needing much in the way of software.  The primary requirement is a bootable USB pen drive or bootable LiveCD (such as [RIPLinuX](http://www.tux.org/pub/people/kent-robotti/looplinux/rip/)) with the necessary tools.  You could also use the CentOS5 boot DVD.

I'll run with the CentOS install DVD since that's what I have sitting in the optical drive at the moment.  When CentOS boots up, enter "<b>linux rescue</b>" at the boot prompt.  Note, if you have multiple NICs installed, it's probably better to not start networking (because the CentOS rescue mode takes forever to initialize unconnected NICs).  

Select "Skip" when asked about mounting the existing install at /mnt/sysimage.  We'll be doing things our own way instead.

Start up Software RAID on the key partitions (/boot, /, the backup /, and the backup partition). The following commands will (usually) startup your existing RAID devices automatically.

    # mdadm --examine --scan >> /etc/mdadm.conf
    # mdadm --assemble --scan

In my case "md0" is /boot, "md2" is my base CentOS install, "md3" is the backup root partition, and "md5" is where I can store image files.  So let's double-check that.

    # mkdir /mnt/root ; mount /dev/md3 /mnt/root
    # mkdir /mnt/backuproot ; mount /dev/md3 /mnt/backuproot

If we then examine the output of "df -h" or by using "ls" on the mounted volumes we can verify that we know which is which.  Let's mount our backup area and create image files.  I prefer to kick off the "dd" commands in the background so that I can monitor progress and keep multiple CPUs busy.

    # mkdir /mnt/backup ; mount /dev/md5 /mnt/backup
    # cd /mnt/backup ; mkdir images ; cd images
    # dd if=/dev/md0 | gzip > dd-md0-boot-20070525.img.gz &
    # dd if=/dev/md2 | gzip > dd-md2-root-20070525.img.gz &
    # dd if=/dev/md3 | gzip > dd-md3-bkproot-20070525.img.gz &

We should also backup the master boot records on each of the hard drives in the unit.

    # for i in a b c; do dd if=/dev/sd$i count=1 bs=512 of=dd-sd$i-mbr-20070525.img; done

Unfortunately, the CentOS5 DVD doesn't include tools like "G4L" (Ghost for Linux) or I'd make a second set of backup files using that.  I may boot my RIPLinuX CD and see what tools are there.  (Because you can never have too many backups.)

Now I can dump the contents of "md2" (the original root) to "md3" (our backup root).  

    # dd if=/dev/md2 of=/dev/md3

Now for some cleanup stuff...

    # mount /dev/md3 /mnt/backuproot
    # vi /mnt/backuproot/etc/fstab

We'll need to change any references of "md2" to "md3".  Basically flip them around so that "md3" is the official root when /etc/fstab gets processed.  I also like to change the prompt and system name to remind myself that I'm using the emergency system.  Again, our primary goal is to be able to get a box back up and operational in the case where the primary root partition is hosed.  Get it up quickly, then schedule some downtime to deal with it properly.

Now would also be a good time to tune the ext3 file system on your partitions.

The last thing we need to do is edit GRUB's configuration so that we can select our backup root OS from the selection menu.

    # mkdir /mnt/boot
    # mount /dev/md0 /mnt/boot
    # vi /mnt/boot/grub/grub.conf

Things that we'll want to do here (you could also accomplish this by booting the server in normal mode and editing grub.conf there using a more comfortable text editor):

a) Change the timeout=5 value to timeout=15 (or 30 or 60).  By default, CentOS doesn't give you very long to pick an alternate boot.  I find 5 seconds to be too short of a window, especially on a unit where the storage controller takes a minute or two to scan and setup the drives.

b) Copy the latest "title" section and change "root=/dev/md2" to "root=/dev/md3".  I always make the "EMERGENCY" boot option the 2nd one in the list.

    # mkdir /mnt/backuproot
    # mount /dev/md3 /mnt/backuproot
    # vi /mnt/backuproot/etc/sysconfig/network

I like to change the hostname to have "-emergency" tacked onto the end.  Which should make it fairly obvious that we are booting up in emergency mode using the backup root partition.  I also edit root's .bash_profile to set PS1.

Okay, that was a lot of setup work just to prepare for implementing iSCSITarget (or any other kernel rebuild), but it's always worth it.

Final notes:

- When I test booted the emergency root partition, things didn't work as planned.  So while my concept is sound, I may have screwed something up.  I think it's an error with /etc/fstab in the emergency partition, so I'll troubleshoot that later.

- It's also possible that you'll need to do a GRUB install on all (3) of the primary mirror disks.

<b>Step 2 - Downloading and compiling the iSCSITarget software</b>

So far, I've found (2) links to be useful here.  One is [Moving on....](http://jackshck.livejournal.com/108860.html) and the other is [iSCSI Enterprise Target ](http://mkozo.sakuraweb.com/article/3728638.html)