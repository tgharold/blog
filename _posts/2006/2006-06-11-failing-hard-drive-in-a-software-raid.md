---
layout: post
title: 'Failing hard drive in a Software RAID'
date: '2006-06-11T08:02:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>So today's fun is that I have a drive that is failing in my 566Mhz Celeron server.  This is a small server with (3) 120GB hard drives.

hda - 120GB (primary drive, 4 partitions)
hdc - CD-ROM
hde - 120GB (second drive in the RAID1 sets, 4 partitions)
hdg - 120GB (backup drive)

During the rebuild of md3 (which is hda4+hde4) I'm getting constant aborts due to a bad block (or blocks) on hda.

<code># tail -n 500 /var/log/messages
Jun 10 23:17:16 coppermine hda: task_in_intr: status=0x59 { DriveReady SeekComplete DataRequest Error }
Jun 10 23:17:16 coppermine hda: task_in_intr: error=0x40 { UncorrectableError }, LBAsect=100789712, sector=100789712
Jun 10 23:17:16 coppermine ide: failed opcode was: unknown
Jun 10 23:17:16 coppermine end_request: I/O error, dev hda, sector 100789712
Jun 10 23:17:20 coppermine hda: task_in_intr: status=0x59 { DriveReady SeekComplete DataRequest Error }
Jun 10 23:17:20 coppermine hda: task_in_intr: error=0x40 { UncorrectableError }, LBAsect=100789723, sector=100789720
Jun 10 23:17:20 coppermine ide: failed opcode was: unknown
Jun 10 23:17:20 coppermine end_request: I/O error, dev hda, sector 100789720
Jun 10 23:17:20 coppermine raid1: hda: unrecoverable I/O read error for block 92537216
Jun 10 23:17:20 coppermine md: md3: sync done.
Jun 10 23:17:20 coppermine RAID1 conf printout:
Jun 10 23:17:20 coppermine --- wd:1 rd:2
Jun 10 23:17:20 coppermine disk 0, wo:0, o:1, dev:hda4
Jun 10 23:17:20 coppermine disk 1, wo:1, o:1, dev:hde4
Jun 10 23:17:20 coppermine RAID1 conf printout:
Jun 10 23:17:20 coppermine --- wd:1 rd:2
Jun 10 23:17:20 coppermine disk 0, wo:0, o:1, dev:hda4
Jun 10 23:17:20 coppermine RAID1 conf printout:
Jun 10 23:17:20 coppermine --- wd:1 rd:2
Jun 10 23:17:20 coppermine disk 0, wo:0, o:1, dev:hda4
Jun 10 23:17:20 coppermine disk 1, wo:1, o:1, dev:hde4
Jun 10 23:17:20 coppermine md: syncing RAID array md3
Jun 10 23:17:20 coppermine md: minimum _guaranteed_ reconstruction speed: 1000 KB/sec/disc.
Jun 10 23:17:20 coppermine md: using maximum available idle IO bandwith (but not more than 200000 KB/sec) for reconstruction.
Jun 10 23:17:20 coppermine md: using 128k window, over a total of 115926464 blocks.</code>

And mdadm will continue to attempt to rebuild the array until the end of time.  Which is rather pointless.  So the second step is to more closely examine /dev/hda and see whether we're seeing the same block number.

<code># grep 'hda:' /var/log/messages
May 29 08:43:06 coppermine hda: Maxtor 4R120L0, ATA DISK drive
May 29 08:43:06 coppermine hda: max request size: 128KiB
May 29 08:43:06 coppermine hda: 240121728 sectors (122942 MB) w/2048KiB Cache, CHS=65535/16/63
May 29 08:43:06 coppermine hda: cache flushes supported
May 29 08:43:06 coppermine hda: hda1 hda2 hda3 hda4
Jun  8 22:32:02 coppermine hda: task_in_intr: status=0x59 { DriveReady SeekComplete DataRequest Error }
Jun  8 22:32:02 coppermine hda: task_in_intr: error=0x40 { UncorrectableError }, LBAsect=80342494, sector=80342480
Jun  8 22:32:04 coppermine hda: task_in_intr: status=0x59 { DriveReady SeekComplete DataRequest Error }
Jun  8 22:32:04 coppermine hda: task_in_intr: error=0x40 { UncorrectableError }, LBAsect=80342494, sector=80342488
Jun  8 22:32:05 coppermine raid1: hda: unrecoverable I/O read error for block 72089984
Jun  9 05:10:36 coppermine hda: task_in_intr: status=0x59 { DriveReady SeekComplete DataRequest Error }
Jun  9 05:10:36 coppermine hda: task_in_intr: error=0x40 { UncorrectableError }, LBAsect=100789712, sector=100789712
Jun  9 05:10:39 coppermine hda: task_in_intr: status=0x59 { DriveReady SeekComplete DataRequest Error }
Jun  9 05:10:39 coppermine hda: task_in_intr: error=0x40 { UncorrectableError }, LBAsect=100789722, sector=100789720
Jun  9 05:10:39 coppermine raid1: hda: unrecoverable I/O read error for block 92537216
Jun  9 08:26:40 coppermine hda: task_in_intr: status=0x59 { DriveReady SeekComplete DataRequest Error }
Jun  9 08:26:40 coppermine hda: task_in_intr: error=0x40 { UncorrectableError }, LBAsect=54393160, sector=54393152
Jun  9 08:26:42 coppermine hda: task_in_intr: status=0x59 { DriveReady SeekComplete DataRequest Error }
Jun  9 08:26:42 coppermine hda: task_in_intr: error=0x40 { UncorrectableError }, LBAsect=54393160, sector=54393160
Jun  9 08:26:42 coppermine raid1: hda: unrecoverable I/O read error for block 46140544
Jun  9 13:13:53 coppermine hda: task_in_intr: status=0x59 { DriveReady SeekComplete DataRequest Error }
Jun  9 13:13:53 coppermine hda: task_in_intr: error=0x40 { UncorrectableError }, LBAsect=100789712, sector=100789712
Jun  9 13:13:55 coppermine hda: task_in_intr: status=0x59 { DriveReady SeekComplete DataRequest Error }
Jun  9 13:13:55 coppermine hda: task_in_intr: error=0x40 { UncorrectableError }, LBAsect=100789722, sector=100789720
Jun  9 13:13:55 coppermine raid1: hda: unrecoverable I/O read error for block 92537216
Jun 10 18:30:21 coppermine hda: Maxtor 4R120L0, ATA DISK drive
Jun 10 18:30:21 coppermine hda: max request size: 128KiB
Jun 10 18:30:21 coppermine hda: 240121728 sectors (122942 MB) w/2048KiB Cache, CHS=65535/16/63
Jun 10 18:30:21 coppermine hda: cache flushes supported
Jun 10 18:30:21 coppermine hda: hda1 hda2 hda3 hda4
Jun 10 23:17:16 coppermine hda: task_in_intr: status=0x59 { DriveReady SeekComplete DataRequest Error }
Jun 10 23:17:16 coppermine hda: task_in_intr: error=0x40 { UncorrectableError }, LBAsect=100789712, sector=100789712
Jun 10 23:17:20 coppermine hda: task_in_intr: status=0x59 { DriveReady SeekComplete DataRequest Error }
Jun 10 23:17:20 coppermine hda: task_in_intr: error=0x40 { UncorrectableError }, LBAsect=100789723, sector=100789720
Jun 10 23:17:20 coppermine raid1: hda: unrecoverable I/O read error for block 92537216
Jun 11 04:08:06 coppermine hda: task_in_intr: status=0x59 { DriveReady SeekComplete DataRequest Error }
Jun 11 04:08:06 coppermine hda: task_in_intr: error=0x40 { UncorrectableError }, LBAsect=100789712, sector=100789712
Jun 11 04:08:08 coppermine raid1: hda: unrecoverable I/O read error for block 92537216</code>

This shows me that I have a drive that almost always fails at the same block number each time.  Another grep of the log files makes this even more clear:

<code># <b>grep 'unrecoverable' /var/log/messages</b>
Jun  8 22:32:05 coppermine raid1: hda: unrecoverable I/O read error for block 72089984
Jun  9 05:10:39 coppermine raid1: hda: unrecoverable I/O read error for block 92537216
Jun  9 08:26:42 coppermine raid1: hda: unrecoverable I/O read error for block 46140544
Jun  9 13:13:55 coppermine raid1: hda: unrecoverable I/O read error for block 92537216
Jun 10 23:17:20 coppermine raid1: hda: unrecoverable I/O read error for block 92537216
Jun 11 04:08:08 coppermine raid1: hda: unrecoverable I/O read error for block 92537216</code>

So the first step (<b>after backing up the system</b>) is to stop the software RAID from attempting to constantly rebuild array "md3".  You can do this with the mdadm tool's "manage mode" commands.

Well, maybe not.  I've done a lot of digging in Google, but I can't figure out how to force mdadm to stop a sync that is in progress.  So, I'm booting back to the original 2005.1 Gentoo boot CD so that I can manually control the process.

Note that an excellent resource is:
[LVM2 and Software RAID in Linux](http://hilli.dk/howtos/lvm2-and-software-raid-in-linux/) (May 2005)

<code>livecd ~ # fdisk -l

Disk /dev/hda: 122.9 GB, 122942324736 bytes
16 heads, 63 sectors/track, 238216 cylinders
Units = cylinders of 1008 * 512 = 516096 bytes

   Device Boot      Start         End      Blocks   Id  System
/dev/hda1   *           1         249      125464+  fd  Linux raid autodetect
/dev/hda2             250        4218     2000376   fd  Linux raid autodetect
/dev/hda3            4219        8187     2000376   fd  Linux raid autodetect
/dev/hda4            8188      238200   115926552   fd  Linux raid autodetect

Disk /dev/hde: 122.9 GB, 122942324736 bytes
16 heads, 63 sectors/track, 238216 cylinders
Units = cylinders of 1008 * 512 = 516096 bytes

   Device Boot      Start         End      Blocks   Id  System
/dev/hde1   *           1         249      125464+  fd  Linux raid autodetect
/dev/hde2             250        4218     2000376   fd  Linux raid autodetect
/dev/hde3            4219        8187     2000376   fd  Linux raid autodetect
/dev/hde4            8188      238200   115926552   fd  Linux raid autodetect

Disk /dev/hdg: 122.9 GB, 122942324736 bytes
16 heads, 63 sectors/track, 238216 cylinders
Units = cylinders of 1008 * 512 = 516096 bytes

   Device Boot      Start         End      Blocks   Id  System
/dev/hdg1               1      238000   119951968+  8e  Linux LVM

livecd ~ # modprobe md
livecd ~ # modprobe raid1
livecd ~ # ls -l /dev/md*
livecd ~ # for i in 0 1 2 3; do mknod /dev/md$i b 9 $i; done
livecd ~ # ls -l /dev/md*
brw-r--r--  1 root root 9, 0 Jun 12 00:01 /dev/md0
brw-r--r--  1 root root 9, 1 Jun 12 00:01 /dev/md1
brw-r--r--  1 root root 9, 2 Jun 12 00:01 /dev/md2
brw-r--r--  1 root root 9, 3 Jun 12 00:01 /dev/md3
livecd ~ # mdadm --assemble /dev/md0 /dev/hda1 /dev/hde1
mdadm: /dev/md0 has been started with 2 drives.
livecd ~ # cat /proc/mdstat
Personalities : [raid1] 
md0 : active raid1 hda1[0] hde1[1]
      125376 blocks [2/2] [UU]

unused devices: <none>
livecd ~ # </none></code>

So that starts up the /boot partition.  Now I can check it for errors using e2fsck.  The "-c" checks for bad blocks, the "-C" updates any inodes on the system with bad block information, and "-y" answers 'yes' to any questions.

<code>livecd ~ # e2fsck -c -C -y -v /dev/md0
e2fsck 1.37 (21-Mar-2005)
Checking for bad blocks (read-only test): done                        376
Pass 1: Checking inodes, blocks, and sizes
Pass 2: Checking directory structure                                           
Pass 3: Checking directory connectivity
Pass 4: Checking reference counts
Pass 5: Checking group summary information

/dev/md0: ***** FILE SYSTEM WAS MODIFIED *****

      40 inodes used (0%)
       3 non-contiguous inodes (7.5%)
         # of inodes with ind/dind/tind blocks: 12/6/0
   12593 blocks used (10%)
       0 bad blocks
       0 large files

      26 regular files
       3 directories
       0 character device files
       0 block device files
       0 fifos
       0 links
       2 symbolic links (2 fast symbolic links)
       0 sockets
--------
      31 files
livecd ~ #</code>

Next, I assemble the RAID1 set for the root volume.

<code>livecd ~ # mdadm --assemble /dev/md2 /dev/hda3 /dev/hde3
mdadm: /dev/md2 has been started with 2 drives.
livecd ~ # cat /proc/mdstat
Personalities : [raid1] 
md2 : active raid1 hda3[0] hde3[1]
      2000256 blocks [2/2] [UU]

md1 : active raid1 hda2[0] hde2[1]
      2000256 blocks [2/2] [UU]

md0 : active raid1 hda1[0] hde1[1]
      125376 blocks [2/2] [UU]

unused devices: <none>
livecd ~ # e2fsck -c -C -y -v /dev/md2
e2fsck 1.37 (21-Mar-2005)
Checking for bad blocks (read-only test): done                        064
Pass 1: Checking inodes, blocks, and sizes
Pass 2: Checking directory structure                                           
Pass 3: Checking directory connectivity                                        
Pass 4: Checking reference counts
Pass 5: Checking group summary information                                     

/dev/md2: ***** FILE SYSTEM WAS MODIFIED *****

    6434 inodes used (2%)
      16 non-contiguous inodes (0.2%)
         # of inodes with ind/dind/tind blocks: 75/2/0
  390601 blocks used (78%)
       0 bad blocks
       0 large files

     928 regular files
     153 directories
    1055 character device files
    4025 block device files
       0 fifos
       0 links
     264 symbolic links (264 fast symbolic links)
       0 sockets
--------
    6425 files
livecd ~ #</none></code>

The rest of the system is more complex, LVM2 volumes on top of software RAID.

<code>livecd ~ # modprobe dm-mod
livecd ~ # pvscan
  PV /dev/hdg1   VG vgbackup   lvm2 [114.39 GB / 82.39 GB free]
  Total: 1 [114.39 GB] / in use: 1 [114.39 GB] / in no VG: 0 [0   ]
livecd ~ # vgscan
  Reading all physical volumes.  This may take a while...
  Found volume group "vgbackup" using metadata type lvm2
livecd ~ # lvscan
  inactive          '/dev/vgbackup/backup' [32.00 GB] inherit
livecd ~ # lvchange -a y /dev/vgbackup/backup
  /dev/cdrom: open failed: Read-only file system
livecd ~ # lvscan
  ACTIVE            '/dev/vgbackup/backup' [32.00 GB] inherit
livecd ~ # e2fsck -c -C -y -v /dev/vgbackup/backup
e2fsck 1.37 (21-Mar-2005)
Checking for bad blocks (read-only test): done                        608
Pass 1: Checking inodes, blocks, and sizes
Pass 2: Checking directory structure                                           
Pass 3: Checking directory connectivity                                        
Pass 4: Checking reference counts                                              
Pass 5: Checking group summary information                                     

/dev/vgbackup/backup: ***** FILE SYSTEM WAS MODIFIED *****

      70 inodes used (0%)
      14 non-contiguous inodes (20.0%)
         # of inodes with ind/dind/tind blocks: 35/18/0
  954693 blocks used (11%)
       0 bad blocks
       0 large files

      55 regular files
       6 directories
       0 character device files
       0 block device files
       0 fifos
       0 links
       0 symbolic links (0 fast symbolic links)
       0 sockets
--------
      61 files
livecd ~ # </code>

So far so good.  But most of the errors are in /dev/md3.  So I'm going to assemble /dev/md3 using just one of the drives (/dev/hde4).

<code>livecd ~ # mdadm -v --assemble /dev/md3 /dev/hde4      
mdadm: looking for devices for /dev/md3
mdadm: /dev/hde4 is identified as a member of /dev/md3, slot 2.
mdadm: added /dev/hde4 to /dev/md3 as 2
mdadm: /dev/md3 assembled from 0 drives and 1 spare - not enough to start the array.
livecd ~ # cat /proc/mdstat
Personalities : [raid1] 
md3 : inactive hde4[2]
      115926464 blocks
md2 : active raid1 hda3[0] hde3[1]
      2000256 blocks [2/2] [UU]

md1 : active raid1 hda2[0] hde2[1]
      2000256 blocks [2/2] [UU]

md0 : active raid1 hda1[0] hde1[1]
      125376 blocks [2/2] [UU]

unused devices: <none></none></code>

Unfortunately, mdadm is refusing to mount /dev/md3 using just /dev/hde4.  So we have to force it:

<code>livecd ~ # mdadm --create /dev/md3 --level 1 --force --raid-disks=1 /dev/hde4
mdadm: Cannot open /dev/hde4: Device or resource busy
mdadm: create aborted
livecd ~ # mdadm --stop /dev/md3
livecd ~ # mdadm --create /dev/md3 --level 1 --force --raid-disks=1 /dev/hde4
mdadm: /dev/hde4 appears to be part of a raid array:
    level=1 devices=2 ctime=Sat Oct 22 20:51:12 2005
Continue creating array? y
mdadm: array /dev/md3 started.
livecd ~ # cat /proc/mdstat
Personalities : [raid1] 
md3 : active raid1 hde4[0]
      115926464 blocks [1/1] [U]

md2 : active raid1 hda3[0] hde3[1]
      2000256 blocks [2/2] [UU]

md1 : active raid1 hda2[0] hde2[1]
      2000256 blocks [2/2] [UU]

md0 : active raid1 hda1[0] hde1[1]
      125376 blocks [2/2] [UU]

unused devices: <none>
livecd ~ #livecd ~ # mdadm --create /dev/md3 --level 1 --force --raid-disks=1 /dev/hde4
mdadm: Cannot open /dev/hde4: Device or resource busy
mdadm: create aborted
livecd ~ # mdadm --stop /dev/md3
livecd ~ # mdadm --create /dev/md3 --level 1 --force --raid-disks=1 /dev/hde4
mdadm: /dev/hde4 appears to be part of a raid array:
    level=1 devices=2 ctime=Sat Oct 22 20:51:12 2005
Continue creating array? y
mdadm: array /dev/md3 started.
livecd ~ # cat /proc/mdstat
Personalities : [raid1] 
md3 : active raid1 hde4[0]
      115926464 blocks [1/1] [U]

md2 : active raid1 hda3[0] hde3[1]
      2000256 blocks [2/2] [UU]

md1 : active raid1 hda2[0] hde2[1]
      2000256 blocks [2/2] [UU]

md0 : active raid1 hda1[0] hde1[1]
      125376 blocks [2/2] [UU]

unused devices: <none>
livecd ~ #</none></none></code>

Now I can scan for LVM2 volumes on the md3 array.

<code>livecd ~ # pvscan
  PV /dev/md3    VG vgmirror   lvm2 [110.55 GB / 52.55 GB free]
  PV /dev/hdg1   VG vgbackup   lvm2 [114.39 GB / 82.39 GB free]
  Total: 2 [224.95 GB] / in use: 2 [224.95 GB] / in no VG: 0 [0   ]
livecd ~ # vgscan
  Reading all physical volumes.  This may take a while...
  Found volume group "vgmirror" using metadata type lvm2
  Found volume group "vgbackup" using metadata type lvm2
livecd ~ # lvscan
  inactive          '/dev/vgmirror/tmp' [4.00 GB] inherit
  inactive          '/dev/vgmirror/vartmp' [4.00 GB] inherit
  inactive          '/dev/vgmirror/opt' [2.00 GB] inherit
  inactive          '/dev/vgmirror/usr' [4.00 GB] inherit
  inactive          '/dev/vgmirror/var' [4.00 GB] inherit
  inactive          '/dev/vgmirror/home' [4.00 GB] inherit
  inactive          '/dev/vgmirror/pgsqldata' [16.00 GB] inherit
  inactive          '/dev/vgmirror/www' [4.00 GB] inherit
  inactive          '/dev/vgmirror/svn' [16.00 GB] inherit
  ACTIVE            '/dev/vgbackup/backup' [32.00 GB] inherit
livecd ~ # lvchange -a y /dev/vgmirror/tmp
  /dev/cdrom: open failed: Read-only file system
livecd ~ # lvchange -a y /dev/vgmirror/vartmp
  /dev/cdrom: open failed: Read-only file system
livecd ~ # lvchange -a y /dev/vgmirror/opt   
  /dev/cdrom: open failed: Read-only file system
livecd ~ # lvchange -a y /dev/vgmirror/usr
  /dev/cdrom: open failed: Read-only file system
livecd ~ # lvchange -a y /dev/vgmirror/var
  /dev/cdrom: open failed: Read-only file system
livecd ~ # lvchange -a y /dev/vgmirror/home
  /dev/cdrom: open failed: Read-only file system
livecd ~ # lvchange -a y /dev/vgmirror/pgsqldata
  /dev/cdrom: open failed: Read-only file system
livecd ~ # lvchange -a y /dev/vgmirror/www      
  /dev/cdrom: open failed: Read-only file system
livecd ~ # lvchange -a y /dev/vgmirror/svn
  /dev/cdrom: open failed: Read-only file system
livecd ~ #</code>

Now I can check all of the LVM2 file systems:

<code>livecd ~ # lvscan
  ACTIVE            '/dev/vgmirror/tmp' [4.00 GB] inherit
  ACTIVE            '/dev/vgmirror/vartmp' [4.00 GB] inherit
  ACTIVE            '/dev/vgmirror/opt' [2.00 GB] inherit
  ACTIVE            '/dev/vgmirror/usr' [4.00 GB] inherit
  ACTIVE            '/dev/vgmirror/var' [4.00 GB] inherit
  ACTIVE            '/dev/vgmirror/home' [4.00 GB] inherit
  ACTIVE            '/dev/vgmirror/pgsqldata' [16.00 GB] inherit
  ACTIVE            '/dev/vgmirror/www' [4.00 GB] inherit
  ACTIVE            '/dev/vgmirror/svn' [16.00 GB] inherit
  ACTIVE            '/dev/vgbackup/backup' [32.00 GB] inherit
livecd ~ # e2fsck -c -C -y -v /dev/vgmirror/tmp
e2fsck 1.37 (21-Mar-2005)
Checking for bad blocks (read-only test): done                        576
Pass 1: Checking inodes, blocks, and sizes
Pass 2: Checking directory structure                                           
Pass 3: Checking directory connectivity
Pass 4: Checking reference counts
Pass 5: Checking group summary information

/dev/vgmirror/tmp: ***** FILE SYSTEM WAS MODIFIED *****

      15 inodes used (0%)
       0 non-contiguous inodes (0.0%)
         # of inodes with ind/dind/tind blocks: 0/0/0
   16472 blocks used (1%)
       0 bad blocks
       0 large files

       2 regular files
       4 directories
       0 character device files
       0 block device files
       0 fifos
       0 links
       0 symbolic links (0 fast symbolic links)
       0 sockets
--------
       6 files
livecd ~ # e2fsck -c -C -y -v /dev/vgmirror/vartmp
e2fsck 1.37 (21-Mar-2005)
Checking for bad blocks (read-only test): done                        576
Pass 1: Checking inodes, blocks, and sizes
Pass 2: Checking directory structure                                           
Pass 3: Checking directory connectivity                                        
Pass 4: Checking reference counts
Pass 5: Checking group summary information

/dev/vgmirror/vartmp: ***** FILE SYSTEM WAS MODIFIED *****

    4771 inodes used (0%)
     524 non-contiguous inodes (11.0%)
         # of inodes with ind/dind/tind blocks: 285/1/0
   52582 blocks used (5%)
       0 bad blocks
       0 large files

    4480 regular files
     282 directories
       0 character device files
       0 block device files
       0 fifos
       0 links
       0 symbolic links (0 fast symbolic links)
       0 sockets
--------
    4762 files
livecd ~ # e2fsck -c -C -y -v /dev/vgmirror/opt   
e2fsck 1.37 (21-Mar-2005)
Checking for bad blocks (read-only test): done                        288
Pass 1: Checking inodes, blocks, and sizes
Pass 2: Checking directory structure                                           
Pass 3: Checking directory connectivity
Pass 4: Checking reference counts
Pass 5: Checking group summary information

/dev/vgmirror/opt: ***** FILE SYSTEM WAS MODIFIED *****

      12 inodes used (0%)
       0 non-contiguous inodes (0.0%)
         # of inodes with ind/dind/tind blocks: 0/0/0
   16443 blocks used (3%)
       0 bad blocks
       0 large files

       1 regular file
       2 directories
       0 character device files
       0 block device files
       0 fifos
       0 links
       0 symbolic links (0 fast symbolic links)
       0 sockets
--------
       3 files
livecd ~ # e2fsck -c -C -y -v /dev/vgmirror/usr
e2fsck 1.37 (21-Mar-2005)
Checking for bad blocks (read-only test): done                        576
Pass 1: Checking inodes, blocks, and sizes
Pass 2: Checking directory structure                                           
Pass 3: Checking directory connectivity                                        
Pass 4: Checking reference counts                                              
Pass 5: Checking group summary information                                     

/dev/vgmirror/usr: ***** FILE SYSTEM WAS MODIFIED *****

  202520 inodes used (38%)
    3582 non-contiguous inodes (1.8%)
         # of inodes with ind/dind/tind blocks: 2317/17/0
  439977 blocks used (41%)
       0 bad blocks
       0 large files

  172474 regular files
   26704 directories
       0 character device files
       0 block device files
       0 fifos
    2487 links
    3333 symbolic links (3248 fast symbolic links)
       0 sockets
--------
  204998 files
livecd ~ # e2fsck -c -C -y -v /dev/vgmirror/var
e2fsck 1.37 (21-Mar-2005)
Checking for bad blocks (read-only test): done                        576
Pass 1: Checking inodes, blocks, and sizes
Pass 2: Checking directory structure                                           
Pass 3: Checking directory connectivity                                        
Pass 4: Checking reference counts
Pass 5: Checking group summary information

/dev/vgmirror/var: ***** FILE SYSTEM WAS MODIFIED *****

   30344 inodes used (5%)
     181 non-contiguous inodes (0.6%)
         # of inodes with ind/dind/tind blocks: 54/1/0
  100055 blocks used (9%)
       0 bad blocks
       0 large files

   29856 regular files
     474 directories
       0 character device files
       0 block device files
       0 fifos
       0 links
       3 symbolic links (3 fast symbolic links)
       2 sockets
--------
   30335 files
livecd ~ # e2fsck -c -C -y -v /dev/vgmirror/home
e2fsck 1.37 (21-Mar-2005)
Checking for bad blocks (read-only test): done                        576
Pass 1: Checking inodes, blocks, and sizes
Pass 2: Checking directory structure                                           
Pass 3: Checking directory connectivity                                        
Pass 4: Checking reference counts
Pass 5: Checking group summary information

/dev/vgmirror/home: ***** FILE SYSTEM WAS MODIFIED *****

      58 inodes used (0%)
       0 non-contiguous inodes (0.0%)
         # of inodes with ind/dind/tind blocks: 0/0/0
   24717 blocks used (2%)
       0 bad blocks
       0 large files

      33 regular files
      15 directories
       0 character device files
       0 block device files
       0 fifos
       0 links
       1 symbolic link (1 fast symbolic link)
       0 sockets
--------
      49 files
livecd ~ # e2fsck -c -C -y -v /dev/vgmirror/pgsqldata 
e2fsck 1.37 (21-Mar-2005)
Checking for bad blocks (read-only test): done                        304
Pass 1: Checking inodes, blocks, and sizes
Inode 1802356, i_blocks is 26312, should be 23952.  Fix<y>? yes                

Pass 2: Checking directory structure                                           
Pass 3: Checking directory connectivity                                        
Pass 4: Checking reference counts
Pass 5: Checking group summary information                                     
Block bitmap differences:  -(3625600--3625704) -(3625710--3625711) -(3625716--3625719) -(3625724--3625907)
Fix<y>? yes

Free blocks count wrong for group #110 (6797, counted=7092).                   
Fix<y>? yes

Free blocks count wrong (4056868, counted=4057163).
Fix<y>? yes

/dev/vgmirror/pgsqldata: ***** FILE SYSTEM WAS MODIFIED *****

    1003 inodes used (0%)
      90 non-contiguous inodes (9.0%)
         # of inodes with ind/dind/tind blocks: 167/19/0
  137141 blocks used (3%)
       0 bad blocks
       0 large files

     964 regular files
      30 directories
       0 character device files
       0 block device files
       0 fifos
       0 links
       0 symbolic links (0 fast symbolic links)
       0 sockets
--------
     994 files
livecd ~ # e2fsck -c -C -y -v /dev/vgmirror/www      
e2fsck 1.37 (21-Mar-2005)
Checking for bad blocks (read-only test): done                        576
Pass 1: Checking inodes, blocks, and sizes
Pass 2: Checking directory structure                                           
Pass 3: Checking directory connectivity                                        
Pass 4: Checking reference counts
Pass 5: Checking group summary information

/dev/vgmirror/www: ***** FILE SYSTEM WAS MODIFIED *****

     478 inodes used (0%)
       0 non-contiguous inodes (0.0%)
         # of inodes with ind/dind/tind blocks: 0/0/0
   25147 blocks used (2%)
       0 bad blocks
       0 large files

     455 regular files
      14 directories
       0 character device files
       0 block device files
       0 fifos
       0 links
       0 symbolic links (0 fast symbolic links)
       0 sockets
--------
     469 files
livecd ~ # e2fsck -c -C -y -v /dev/vgmirror/svn
e2fsck 1.37 (21-Mar-2005)
Checking for bad blocks (read-only test): done                        304
Pass 1: Checking inodes, blocks, and sizes
Pass 2: Checking directory structure                                           
Pass 3: Checking directory connectivity                                        
Pass 4: Checking reference counts
Pass 5: Checking group summary information                                     

/dev/vgmirror/svn: ***** FILE SYSTEM WAS MODIFIED *****

     128 inodes used (0%)
      17 non-contiguous inodes (13.3%)
         # of inodes with ind/dind/tind blocks: 15/10/0
  146674 blocks used (3%)
       0 bad blocks
       0 large files

      98 regular files
      21 directories
       0 character device files
       0 block device files
       0 fifos
       0 links
       0 symbolic links (0 fast symbolic links)
       0 sockets
--------
     119 files
livecd ~ #</y></y></y></y></code>

So all of the filesystems on /dev/hde4 check out okay.  Now I want to take a closer look at the drives to verify that they have no bad blocks.  The best way to do this is with a read-only disk test using badblocks.

<code># badblocks -sv /dev/hdg1</code>

From the looks of my testing on the various drives, hda is the problem drive with a few surface errors.  So I'm going to wholy replace drive hda with a fresh 120GB drive.

So I've moved the cables from hda to connect with hde, and I've put a new 120GB hard drive into the hde position.  Since I setup the box properly way back when (installing grub to both disks) things are working very well and the machine booted right back up.

First we copy the partition layout from hda to hde, then I copy the boot sector from hda to hde.

<code>coppermine thomas # sfdisk -d /dev/hda | sfdisk /dev/hde
Checking that no-one is using this disk right now ...
OK

Disk /dev/hde: 238216 cylinders, 16 heads, 63 sectors/track
Old situation:
Warning: The partition table looks like it was made
  for C/H/S=*/255/63 (instead of 238216/16/63).
For this listing I'll assume that geometry.
Units = cylinders of 8225280 bytes, blocks of 1024 bytes, counting from 0

   Device Boot Start     End   #cyls    #blocks   Id  System
/dev/hde1          0+  14945   14946- 120053713+   6  FAT16
/dev/hde2          0       -       0          0    0  Empty
/dev/hde3          0       -       0          0    0  Empty
/dev/hde4          0       -       0          0    0  Empty
New situation:
Units = sectors of 512 bytes, counting from 0

   Device Boot    Start       End   #sectors  Id  System
/dev/hde1   *        63    250991     250929  fd  Linux raid autodetect
/dev/hde2        250992   4251743    4000752  fd  Linux raid autodetect
/dev/hde3       4251744   8252495    4000752  fd  Linux raid autodetect
/dev/hde4       8252496 240105599  231853104  fd  Linux raid autodetect
Successfully wrote the new partition table

Re-reading the partition table ...

If you created or changed a DOS partition, /dev/foo7, say, then use dd(1)
to zero the first 512 bytes:  dd if=/dev/zero of=/dev/foo7 bs=512 count=1
(See fdisk(8).)
coppermine thomas # dd if=/dev/hda bs=512 count=1 of=/dev/hde
1+0 records in
1+0 records out
coppermine thomas # fdisk -l /dev/hda

Disk /dev/hda: 122.9 GB, 122942324736 bytes
16 heads, 63 sectors/track, 238216 cylinders
Units = cylinders of 1008 * 512 = 516096 bytes

   Device Boot      Start         End      Blocks   Id  System
/dev/hda1   *           1         249      125464+  fd  Linux raid autodetect
/dev/hda2             250        4218     2000376   fd  Linux raid autodetect
/dev/hda3            4219        8187     2000376   fd  Linux raid autodetect
/dev/hda4            8188      238200   115926552   fd  Linux raid autodetect
coppermine thomas # fdisk -l /dev/hde

Disk /dev/hde: 122.9 GB, 122942324736 bytes
16 heads, 63 sectors/track, 238216 cylinders
Units = cylinders of 1008 * 512 = 516096 bytes

   Device Boot      Start         End      Blocks   Id  System
/dev/hde1   *           1         249      125464+  fd  Linux raid autodetect
/dev/hde2             250        4218     2000376   fd  Linux raid autodetect
/dev/hde3            4219        8187     2000376   fd  Linux raid autodetect
/dev/hde4            8188      238200   115926552   fd  Linux raid autodetect
coppermine thomas # </code>

Now I need to add the new partitions to the software RAID arrays.

<code>coppermine thomas # cat /proc/mdstat
Personalities : [raid1] 
md1 : active raid1 hda2[1]
      2000256 blocks [2/1] [_U]

md2 : active raid1 hda3[1]
      2000256 blocks [2/1] [_U]

md3 : active raid1 hda4[0]
      115926464 blocks [1/1] [U]

md0 : active raid1 hda1[1]
      125376 blocks [2/1] [_U]

unused devices: <none>
coppermine thomas # mdadm /dev/md0 -a /dev/hde1
mdadm: hot added /dev/hde1
coppermine thomas # cat /proc/mdstat
Personalities : [raid1] 
md1 : active raid1 hda2[1]
      2000256 blocks [2/1] [_U]

md2 : active raid1 hda3[1]
      2000256 blocks [2/1] [_U]

md3 : active raid1 hda4[0]
      115926464 blocks [1/1] [U]

md0 : active raid1 hde1[2] hda1[1]
      125376 blocks [2/1] [_U]
      [=&gt;...................]  recovery =  9.7% (12928/125376) finish=0.5min speed=3232K/sec

unused devices: <none>
coppermine thomas #</none></none></code>

Repeat the above for the other 3 RAID1 arrays that are degraded.

At this point, I'm basically done.  It's time to make another backup and maybe swap the hda/hde cables to verify that I copied the boot sector correctly.

...

The big problem is that md3 is showing up with only a single drive "[U]" instead of "[U_]".  So I need to figure out how to tell mdadm to add /dev/hde4 to the array and force it to resync.  (To fix this, you use the "grow" command of mdadm.)

<code>coppermine thomas # mdadm --grow /dev/md3 --raid-disks=2
coppermine thomas # cat /proc/mdstat
Personalities : [raid1]
md1 : active raid1 hde2[0] hda2[1]
      2000256 blocks [2/2] [UU]

md2 : active raid1 hde3[0] hda3[1]
      2000256 blocks [2/2] [UU]

md3 : active raid1 hda4[0]
      115926464 blocks [2/1] [U_]

md0 : active raid1 hde1[0] hda1[1]
      125376 blocks [2/2] [UU]

unused devices: <none>
coppermine thomas # mdadm /dev/md3 --add /dev/hde4
mdadm: hot added /dev/hde4
coppermine thomas # cat /proc/mdstat
Personalities : [raid1] 
md1 : active raid1 hde2[0] hda2[1]
      2000256 blocks [2/2] [UU]

md2 : active raid1 hde3[0] hda3[1]
      2000256 blocks [2/2] [UU]

md3 : active raid1 hde4[2] hda4[0]
      115926464 blocks [2/1] [U_]
      [&gt;....................]  recovery =  0.0% (6656/115926464) finish=1153.4min speed=1664K/sec

md0 : active raid1 hde1[0] hda1[1]
      125376 blocks [2/2] [UU]

unused devices: <none>
coppermine thomas #</none></none></code><div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2006.shtml">2006</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/SoftwareRAID.shtml">SoftwareRAID</a>
		<div class="Byline">
			posted by Thomas at 
			[08:02](http://www.tgharold.com/techblog/2006/06/failing-hard-drive-in-software-raid.shtml)

		</div>