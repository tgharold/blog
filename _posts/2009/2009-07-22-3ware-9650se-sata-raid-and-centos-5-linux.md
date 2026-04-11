---
layout: post
title: '3ware 9650SE SATA RAID and CentOS 5 Linux'
date: '2009-07-22T08:47:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


A few months ago, I picked up a 3ware 9650SE 16-port controller for use in my primary office server which runs CentOS 5.  So far, it's been an up and down ride.

Problem #1 - The boot process could not find the array disks.

I have a triple-mirror set that I use for my primary operating system drive.  On the old system, they were hooked up directly to the SATA ports on the motherboard.  

(Triple-mirror means that I created the elements in mdadm, a.k.a. Software RAID, where all 3 drives are active mirror copies of each other.  This offers a slight speed-up for reads, allows you to survive 2 drive failures, and puts what would otherwise be an idle hot-swap disk to use.)

On the new system, I decided to attach them to the 3ware card and configure them as JBOD.  However, the kernel initrd file (2.6.18-92.1.22.el5) that I was using for the old motherboard did not have drivers installed for the 3ware card.

So I had to create a custom initrd file by using gzip and cpio to unpack the contents into a directory.  Then I copied the 3ware kernel driver binary from the 2.6.18-92.1.22.el5 folder, added it to the list of modules to be loaded.  Finally, I repacked the initrd file, added a grub.conf entry to point at it, and booted cleanly.

Unfortunately, this was all done using the CentOS 5.3 install CD, so I was unable to log the session or keep careful track of what I did.

Problem #2 - JBOD is not really supported on the 9650SE

In the BIOS interface, you *can* setup disks as JBOD and tell the controller to export JBOD disks (see controller options).  Setting a drive as JBOD does not currently overwrite/erase data on the drive, so it is a fairly safe operation and a good way to hook up a drive with existing data.

Note that if you have "export JBOD" set in the controller options, you can simply hook the drives up, rescan (using the BIOS or 3ware command-line utility called "tw_cli"), and the drives should show up as /dev/sd? in your list.

The major downside of JBOD mode is that write caching is always disabled by default.  This means that your drives are going to have a much higher utilization percentage (as seen by "atop") then if you had enabled write caching.

Now, you can enable write caching for JBOD drives, but the unit has to be told to do that after every reboot.  The command (assuming that your controller is "c0" and the unit is "u12") is:

# tw_cli /c0/u12 set cache=on

A final note.  If you're going to use write caching, you should spring for the BBU (Battery Backup Unit).

Problem #3 - Controlling the RAID

Download and install the "tw_cli" tarball from 3ware.  Since you have to have the 3ware driver installed to talk to the card, and the 9650SE prefers "Single Disk" over "JBOD", you're probably going to want to use 3ware RAID instead of Software RAID.

The problem with "Single Disk" mode is that it overwrites the first few sectors on the disk with 3ware control information.  So all of the disks in "Single Disk" mode are going to slightly smaller then a JBOD disk.  Be aware that putting a disk into a 3ware array will cause the loss of anything at the start of the disk (such as the partition table) and the number of cylinders will be slightly smaller.

Of course, due to the strange geometry of a disk touched by the 3ware controller, you'll probably have to move the disk to another 3ware controller in order to read the data in the future.  Well, maybe, if you're using Software RAID1 mirroring on top of 3ware Single Disks, then the data is highly likely to be in an easy to read format, other then the odd starting point for the partitions.

Anyway, some key commands when using the tw_cli application:

# tw_cli show
- Displays the list of controllers installed.  Make note of the "c#" nomenclature as you will use those "c#" labels in later commands to refer to a specific controller.

# tw_cli /c0 show
- Displays units/ports for the *first* controller installed.

# tw_cli /c0 rescan
- Use this after inserting/removing a disk using a hot-swap enclosure.

# tw_cli /c0/ux show all
- Displays configuration information for whichever unit # you provided.  Replace the "x" with the unit # that you want to look at (such as /c0/u3 or /c0/u12).

Problem #4 - Performance (a.k.a. I/O wait hell)

Unfortunately, the 3ware Linux kernel driver in Red Hat / CentOS 2.6.18-92.1.22.el5, is not very good.  The symptoms are as follows:

1) Create multiple "single disk" units.

2) Make heavy writes to one or more of the units.  Such as using "dd" to overwrite the unit with zeros.

3) Attempt to access data on the other units.

What you will find is that:

- Performance of the system starts to feel extremely sluggish for any operations that touch drives on the 3ware controller.

- Looking at "atop", you will see that the other drives are now reporting seek times of 100-200ms instead of 1-10ms.  Their utilization numbers will be up around 90-100%, even though the number of reads/writes are only in the 2-3 digit range.

- Turning write caching on/off doesn't make a difference.

From my web searches, it seems like this may be a problem specific to kernel versions prior to 2.6.26.  Unfortunately, the stock kernel in Red Hat / CentOS is based off of 2.6.18 and I haven't found out yet whether Red Hat / CentOS have backported the fix.

Updates:

- Even the 2.6.18-128 RHEL/CentOS kernel displays sluggishness any time that we access units (a RAID 6, 8 drive unit that is the only thing on the array).  We have zero performance problems with drive attached to a different SATA controller running Software RAID.

- I can't recommend using the 9650SE controller with RHEL/CentOS currently.  Performance is absolutely horrid under load.
