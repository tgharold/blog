---
layout: post
title: 'Brute force disaster recovery for CentOS5'
date: '2007-05-07T10:52:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Today's trick is moving a CentOS5 system from an old set of disks over to a new set of disks.  Along the way, I'll create an image of the system to allow me to restore it later on.

The CentOS5 system is a fresh install running RAID-1 across (3) disks using Linux Software RAID (mdadm).  There are (4) primary partitions (boot, root, swap, LVM) with no data on the LVM partition.

(Why 3 active disks?  The normal setup for this server was RAID-1 across 2 disks with a hot-spare.  Rather then have a risky window of time where one disk has failed and the hot-spare is synchronizing with the remaining good disk, I prefer to have all 3 disks running.  That way, when a disk dies, we still have 2 disks in action.  The mdadm / Software RAID doesn't seem to care and it doesn't seem to affect performance at all.)

Because this is RAID-1, capturing the disk layout and migrating over to the new disks will be very easy.  It's also a very fresh install, so I'm just going to grab the disk contents using "dd" (most of the partition's sectors are still zeroed out from the original install).  Once I've backed up the (3) partitions on the first drive, I'm going to pull the (3) drives and replace them with the new ones.

I'll get the machine up and running with the first replacement drive, then configure the blank 2nd and 3rd drives and add them to the RAID set.  That is, if mdadm doesn't beat me to the punch and start the sync on the 2nd/3rd disks automatically.

If things go bad, I can always drop the original disks back in the unit and power it back up.  I plan on keeping them around for a few days, just in case.  I'll have to recreate the LVM volumes, but there aren't any yet (just a PV and a VG).

One advantage of pulling the old drives out completely and rebuilding using fresh drives - I'll end up with a tested disaster recovery process. 

Now for the nitty gritty.  I'm using a USB pocket drive formatted with ext3 for the rescue work.  Make sure that you plug this in before booting the rescue CD.
<ol>

<li>Login to the system and power it down.

</li>
<li>Boot the CentOS5 install DVD

</li>
<li>At the "boot:" enter "<b>linux rescue</b>"

</li>
<li>Work your way through the startup dialogs

</li>
<li>When prompted whether to mount your linux install, choose "Skip"

</li>
</ol>

This should give you a command shell with useful tools.  So let's poke around and check on our system.
<ol>

<li>Looking at "<b>cat /proc/mdstat</b>" shows that while the mdadm software is running, it has not assembled any RAID arrays.

</li>
<li>The "<b>fdisk -l</b>" command shows us that the (3) existing disks are named sda, sdb, sdc.  Each has (4) partitions (boot, root, swap, LVM).

</li>
<li>My USB drive showed up as "/dev/sdd" so I'll create a "/backup" folder and mount it using "mkdir /backup ; mount /dev/sdd1 /backup ; df -h"

</li>
</ol>

Naturally, we should create a sub-folder under /backup for each machine and possibly create another folder underneath it using today's date.  We should grab information about the current disk layout and store it in a text file (fdisk.txt).
<ol>

<li># cd /backup ; mkdir <i>machinename</i> ; cd <i>machinename</i>

</li>
<li># mkdir <i>todaysdate</i> ; cd <i>todaysdate</i>

</li>
<li># fdisk -l &gt; fdisk.txt

</li>
</ol>

Now to grab the boot loader and image the two critical partitions (boot and root).  We'll grab the boot loader off of all (3) drives because it's so small (and it may not be properly synchronized).
<ol>

<li>dd if=/dev/sda bs=512 count=1 of=machinename-date-sda.mbr

</li>
<li>dd if=/dev/sdb bs=512 count=1 of=machinename-date-sdb.mbr

</li>
<li>dd if=/dev/sdb bs=512 count=1 of=machinename-date-sdc.mbr

</li>
<li>dd if=/dev/sda1 | gzip &gt; machinename-date-ddcopy-sda1.img.gz

</li>
<li>dd if=/dev/sda2 | gzip &gt; machinename-date-ddcopy-sda2.img.gz

</li>
</ol>

Total disk space for my system was around 1.75GB worth of compressed files (8GB root, 250MB boot).  You could also use bzip2 if you need more compression.  Unfortunately, the CentOS5 DVD does not include the "split" command, which could cause issues if you're trying to write to a filesystem that can't handle files over 2GB in size.

Now you should shut the box back down, burn those files to DVD-R, install the new (blank) disks, and boot from the install DVD again.  Again, mount the drive that holds the rescue image files to a suitable path.
<ol>

<li>dd of=/dev/sda bs=512 count=1 if=machinename-date-sda.mbr

</li>
<li>fdisk /dev/sda (fix the last partition)

</li>
<li>dd if=/dev/sda bs=512 count=1 of=/dev/sdb

</li>
<li>dd if=/dev/sda bs=512 count=1 of=/dev/sdc

</li>
</ol>

That will restore the MBR and partition table from the old drive to the new one.  If your new drive has a different size, then the last partition will be incorrectly sized for the disk.  Fire up "fdisk" and delete / recreate the last partition on the disk.

Restore the two partition images:
<ol>

<li># gzip -dc machinename-date-ddcopy-sda1.img.gz | dd of=/dev/sda1

</li>
<li># gzip -dc machinename-date-ddcopy-sda2.img.gz | dd of=/dev/sda2

</li>
</ol>

At this point, we should be able to boot the system on the primary drive and have Software RAID come up in degraded mode for the arrays.  Things that will need to be done once the unit boots:
<ol>

<li>Tell mdadm about the 2nd (and 3rd) disks and tell it to bring those partitions into the arrays and synchronize them.

</li>
<li>Create a new swap area

</li>
<li>Recreate the LVM physical volume (PV) and volume group (VG)

</li>
<li>Restore any data from the LVM area (we had none in this example)

</li>
</ol>

Getting the Software RAID back up and happy is the trickiest of the steps.
<ol>

<li>Login as root, open up a terminal window

</li>
<li># cat /proc/mdstat

</li>
<li># fdisk -l

</li>
<li>Notice that the swap area on our system is sda3, sdb3, sdc3 and will need to be loaded as /dev/md1.

</li>
<li># mdadm --create /dev/md1 -v --level=raid1 --raid-devices=3 /dev/sda3 /dev/sdb3 /dev/sdc3

</li>
<li># mkswap /dev/md1 ; swapon /dev/md1

</li>
<li>Now we're ready to recreate the LVM area

</li>
<li># mknod /dev/md3 b 9 3

</li>
<li># mdadm --create /dev/md3 -v --level=raid1 --raid-devices=3 /dev/sda4 /dev/sdb4 /dev/sdc4

</li>
<li># pvcreate /dev/md3 ; vgcreate vg /dev/md3

</li>
<li>Finally, we should add the 2nd and 3rd drive to md0 and md2.

</li>
<li>mdadm --add /dev/md0 /dev/sdc1

</li>
<li>mdadm --add /dev/md0 /dev/sdb1

</li>
</ol>

Note: If your triple mirror RAID array puts the additional disks in as spares, make sure that you have (a) grown the number of raid devices to 3 for the RAID1 set and (b) make sure that there are no other arrays synchronizing as the same time.  It's also best to add the elements one at a time, rather then adding both at the same time.  I'm not sure if it's a bug in mdadm or just the way it works, but it took me two tries to get my triple mirror back up with all disks marked as "active" instead of (2) active and (1) hot-spare.
