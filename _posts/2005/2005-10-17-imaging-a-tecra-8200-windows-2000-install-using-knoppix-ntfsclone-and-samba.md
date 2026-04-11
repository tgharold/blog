---
layout: post
title: 'Imaging a Tecra 8200 Windows 2000 install using Knoppix, NTFSClone, and Samba'
date: '2005-10-17T19:07:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


One of the more annoying things that our users do is to get their Windows workstations into an unworkable state after 9 months or so.  We've tried user education, we use things like spyware removers, eliminating the use of Internet Explorer, etc, but there are a lot of times where it's less time and trouble for us to reset the machine back to a known point.  Now, there are a few ways to do this such as paying for programs like Norton Ghost or Acronis True Image.  Both of those work but they cost $50/seat roughly.  But I'd like to do it for less.  Or at least take a shot at doing it for less.

(I do use Acronis True Image on a few of my systems.  It's good for making more frequent snapshots without having to reboot to a seperate operating system.  It also has an incremental mode that can be used to keep a single image up to date.  For user simplicity, it's hands-down the winner over Ghost.)

First off, you will need to download and burn the Knoppix Boot CD.  I'm using version 4.0.2 which hopefully has what I need (see this Slashdot comment, "[where is ntfsclone](http://linux.slashdot.org/comments.pl?sid=125853&amp;cid=10543386)", from Oct 2004).  The version that shows up on the 4.0.2 Knoppix CD is "ntfsclone v1.11.3-WIP" so I should be good to go.

You should also browse the following links:

[Linux NTFS Project](http://linux-ntfs.sourceforge.net/index.html)
[Bahut:  Cloning XP with Linux and ntfsclone](http://milivoj2.blogspot.com/2005/04/cloning-xp-with-linux-and-ntfsclone.html)
[Knoppix Rescue FAQ](http://www.knoppix.net/wiki/Rescue_FAQ)
[Installing Ubuntu on Fujitsu ST 4000 Tablet PC](http://calkinsc.home.comcast.net/fujitsu_st_4000.html) (they used ntfsclone to backup the WinXP that was on the Tablet PC first)
[ System Recovery with Knoppix](http://slashdot.org/article.pl?sid=04/10/15/2127244)

The hardware that I'm backing up is a Toshiba Tecra 8200 with an 18GB HD that is not going to be very full.  At this point, I've finished installing all of the Windows 2000 patches along with some key tools, but it's still not 100% installed.  Still, it's a good spot to take a snapshot since everything that is installed is working fine.

Steps:

1. Make sure the system is connected to the network, or that there is a USB drive attached with a FAT32 file system.  You'll need a storage location where you can write the image file to.  A network folder is preferred so that you can write to an NTFS file system and avoid the 4GB limit of FAT32.

2. Boot into Windows and perform last-minute housekeeping:

a. Clear out any temporary folders/files.
b. Move easily restored user files off of the system.
c. Empty the trash folder.
d. Do a CHKDSK of the file system (requires reboot)
e. Defrag the hard drive.
f. Verify connectivity

Note for step "b.":  This image is not meant to be a frequent backup of user files.  There should be other tools in place for that (Second Copy 2000, rsync, tar/bzip2).  By pulling easily restored user files off of the hard drive, you'll make the image file much smaller and easier to manage.  Plus, during a restoration, you'll be overwriting user files in the image with newer user files from the most recent backup anyway.

3. Boot to the Knoppix CD.  On the Tecra 8200 you are required to press the [F2] key during the bootup sequence, which will present you with a list of boot sources.  You can then press [C] for CD-ROM.  On other systems, you may need to muck with the boot order in the BIOS so that the CD-ROM comes before the hard drive.  

I will assume that Knoppix boots properly on your system and that you end up at the Knoppix desktop.

4a. If you are going to connect to a network shared folder to store the image file, then look for the penguin icon on the bar at the bottom of the screen labeled "KNOPPIX".  Open this menu, go to "Utilities" and then "Samba Network Neighborhood".  If Samba (SMB) is working properly, then you should see your local Windows domain and you can browse to your network share.

4b. If you are going to connect to a USB drive for storage of the image, then look for (FIXME).

5.  Fire up the command line.  To do this in Knoppix, go back to the "KNOPPIX" (penguin) icon and click on the "Root Shell" option.  You will see a terminal window open up with a prompt that looks like:

<code>root@1[knoppix]#</code>

6. Familiarize yourself with the partitions on the system:

<code>root@1[knoppix]# cat /proc/partitions
major minor  #blocks  name
   3     0   19535040 hda
   3     1   19535008 hda1
   8     0   60051600 sda
   8     1   32764536 sda1
 240     0    1942016 cloop0
root@1[knoppix]# </code>

The above listing shows that there is a ~18GB hard drive installed (hda) with a single partition (hda1) that fills most of the drive.  This drive (hda) is what we plan on backing up, if your system uses a different drive letter for the operating system drive, then you will need to adjust later commands.  Most ATA/IDE disk drives used for booting Windows are labeled as "hda".  You will generally only see "sda" used as the boot drive on systems that boot from SCSI drives.

Notice that there is also a 60GB USB drive attached (sda) with a single 32GB partition (sda1).  If I want, I could mount this 32GB FAT32 partition as my destination media to the /tmp/imagedest mount point (see step 7b).

7a. Create a mount point (/tmp/imagedest) and mount the Samba network share that you browsed to earlier.  Note the name as shown in the Konqueror browse window (smb://DOMAIN\account@servername/foldername).  This is typically case-sensitive, so you'll need to pay close attention to that.  Or you could mount the USB drive at this location.

<code>root@1[knoppix]# mkdir /tmp/imagedest
root@1[knoppix]# mount -t smbfs -o username=DOMAIN\\account //servername/foldername /tmp/imagedest
Password: ******
root@1[knoppix]#</code>

Notes:
- You'll need a double-backslash between your domain name and your account name in the Windows domain.
- Domain names in Samba are almost always all upper-case.
- Account names are almost always all lower-case.
- Samba is picky about case.
- You will be prompted for your password.
- The <b>mount</b> command does not give feedback.  You can check that there is now a new mount point by repeating the <b>mount</b> command without any arguments.

7b. (FIXME) Show how to mount the USB as the target point.

8. Save the partition table and the master boot record (MBR).

<b>Warning: VERIFY your commands before using them.</b>  It's very easy to blow away your operating system by accident when using the following tools.

<code>root@1[knoppix]# sfdisk -d /dev/hda &gt; /tmp/imagedest/myuser-hda.dump
root@1[knoppix]# dd if=/dev/hda bs=512 count=1 of=/tmp/imagedest/myuser-hda.mbr
1+0 records in
1+0 records out
512 bytes transferred in 0.426934 seconds (1199 bytes/sec)
root@1[knoppix]#</code>

Notes:
- I'd recommend replacing "myuser" in the output filenames with a minimum of the date, the model/make of the system being imaged, and possibly the username associated with the system.

9. Use <b>ntfsclone</b> to backup the individual NTFS partitions.  Note that this only works for NTFS partitions and may have unpredictable effects if you try to backup a FAT16 or FAT32 partition.  You will need to repeat this command for each NTFS partition that you want to save.  Notice that we are breaking the image into 4000MB chunks to allow these chunks to be easily placed onto DVD media for archival.  You can use smaller chunk sizes if you run into other issues, but it makes it slightly more difficult later to reconstruct the image.

<code>root@1[knoppix]# ntfsclone -s -o - /dev/hda1 | gzip | split -b 1000m - /tmp/imagedest/myuser-diskimage-hda1.img.gz_
root@1[knoppix]#</code>

Notes:
- There are two places in the command where a "-" appears by itself.  These are critical as they tell <b>ntfsclone</b> to pipe to standard output ("-o -") and that the <b>split</b> command should pull from standard input ("-" by itself).
- You'll probably want to use the underscore ("_") on the end of the image filename so that split adds the 2-letter suffix (aa, ab, ac, etc) in a way that is not confusing.
- Note, I also hit the 2GB limit (even though I was writing to a share on an NTFS volume).  So I went ahead and backed off to 1GB splits.

(FIXME) (to be continued)
