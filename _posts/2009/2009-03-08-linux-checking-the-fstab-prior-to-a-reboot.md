---
layout: post
title: 'Linux: Checking the fstab prior to a reboot'
date: '2009-03-08T11:40:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


One of the joys of working on a server from a remote location is dealing with the issue caused by a broken /etc/fstab file.  Even the best admins make mistakes and mistakes in that file can lead to a server that won't boot.

Which is fine; if you have an IP-based KVM where you can get console access without actually being at the facility.  But not so great when a screwed up fstab file requires you to go physically visit the location.

So how do we verify that our fstab file makes sense prior to a reboot?  The answer lies in the <b>mount</b> command.  There are (3) useful options that can be passed to the mount command which will help us check the fstab file prior to a reboot.

<b>-f</b> - FAKE IT (Causes everything to be done except for the actual system call).  This tells mount to do everything, but don't actually change anything.

<b>-a</b> - Mount all filesystems mentioned in fstab.

<b>-v</b> - Be verbose about it.

Here's an example where everything is fine and dandy.

<code># mount -fav
mount: /dev/md0 already mounted on /boot
mount: devpts already mounted on /dev/pts
mount: tmpfs already mounted on /dev/shm
mount: proc already mounted on /proc
mount: sysfs already mounted on /sys
mount: /dev/md4 already mounted on /var/log
nothing was mounted</code>

Same example, except that I screwed up the name of /dev/md4 in the fstab file:

<code># mount -fav   
mount: /dev/md0 already mounted on /boot
mount: devpts already mounted on /dev/pts
mount: tmpfs already mounted on /dev/shm
mount: proc already mounted on /proc
mount: sysfs already mounted on /sys
/dev/md4x on /var/log type ext3 (rw,noatime)
nothing was mounted</code>

Now, there's probably a better way to do this, but this serves as at least a moderate check against shooting yourself in the foot.
