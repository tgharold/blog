---
layout: post
title: 'Failed drive slice in a Software RAID after resync'
date: '2007-12-05T08:43:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


One of the things that I do periodically on my servers is to run a mdadm resync.  Because this can put a heavy strain on the disk system, I strongly suggest that you have good backups in place.  My home systems run a check about once a month, servers at work run a check early on Tuesday mornings.

The script is very simple, and you can even fire off the command by writing "check" to the sync_action variable of the md process.

<code>#!/bin/sh
# Tells mdadm to verify that the arrays are synchronized.
# This deals with the issue where a seldom-read disk block has gone bad
# by doing a daily/weekly verification of the array.

echo check &gt; /sys/block/md0/md/sync_action
echo check &gt; /sys/block/md1/md/sync_action
echo check &gt; /sys/block/md2/md/sync_action
echo check &gt; /sys/block/md3/md/sync_action
echo check &gt; /sys/block/md4/md/sync_action
echo check &gt; /sys/block/md5/md/sync_action
echo check &gt; /sys/block/md6/md/sync_action</code>

In this particular case, all of my RAID slices verified correctly, except for one of them.  In this particular situation I'm running a triple-active RAID1 array.  (Instead of using a hot-spare disk, I'm putting live data onto all three disks and using all three actively.)

See also [Failing hard drive in a Software RAID](/blog/2006-06-11-failing-hard-drive-in-a-software-raid/)

<code>$ cat /proc/mdstat
Personalities : [raid1] 
md0 : active raid1 sdc1[2] sdb1[1] sda1[0]
      256896 blocks [3/3] [UUU]

md2 : active raid1 sdc3[2] sdb3[1] sda3[0]
      12289600 blocks [3/3] [UUU]

md4 : active raid1 sdc5[2] sdb5[1] sda5[0]
      33551616 blocks [3/3] [UUU]

md3 : active raid1 sdc6[2] sdb6[1] sda6[0]
      1052160 blocks [3/3] [UUU]

md5 : active raid1 sdc7[2] sdb7[1] sda7[0]
      64010880 blocks [3/3] [UUU]

md6 : active raid1 sdc8[2] sdb8[1] sda8[0]
      267257216 blocks [3/3] [UUU]

md7 : active raid1 sdf1[2] sde1[1] sdd1[0]
      488383936 blocks [3/3] [UUU]

md1 : active raid1 sdc2[3](F) sdb2[1] sda2[0]
      12289600 blocks [3/2] [UU_]

unused devices: &lt;none&gt;</code>

The md1 array is my / (root) partition.  Since the rest of the disk slices appear to be fine, I'm going to proceed with the assumption that it was a minor glitch.

<b>Step 0: Analyze the failure</b>

The first sign of error was the (F) showing up in /proc/mdstat.  Apparently I don't have mdadm configured yet in monitor mode so that it e-mails me when it finds an error.

<code># grep "sdc2" messages     
Dec  4 09:11:58 fw1-shimo kernel: raid1: Disk failure on sdc2, disabling device. 
Dec  4 09:12:06 fw1-shimo kernel:  disk 2, wo:1, o:0, dev:sdc2</code>

The full detail from the mdadm resync:

<code># grep "Dec  4 09" messages | grep "md:"
Dec  4 09:08:33 fw1-shimo kernel: md: md6: sync done.
Dec  4 09:08:33 fw1-shimo kernel: md: syncing RAID array md1
Dec  4 09:08:33 fw1-shimo kernel: md: minimum _guaranteed_ reconstruction speed: 1000 KB/sec/disc.
Dec  4 09:08:33 fw1-shimo kernel: md: using maximum available idle IO bandwidth (but not more than 200000 KB/sec) for reconstruction.
Dec  4 09:08:33 fw1-shimo kernel: md: using 128k window, over a total of 12289600 blocks.
Dec  4 09:11:31 fw1-shimo kernel: md: md1: sync done.
# </code>

And finally, evidence from the logs that shows that sdc was having issues:

<code>Dec  4 09:11:34 fw1-shimo kernel: ata3.00: exception Emask 0x0 SAct 0x0 SErr 0x0 action 0x0
Dec  4 09:11:34 fw1-shimo kernel: ata3.00: (BMDMA stat 0x60)
Dec  4 09:11:34 fw1-shimo kernel: ata3.00: tag 0 cmd 0x25 Emask 0x9 stat 0x51 err 0x40 (media error)
Dec  4 09:11:34 fw1-shimo kernel: ata3: EH complete
Dec  4 09:11:35 fw1-shimo kernel: ata2.00: exception Emask 0x0 SAct 0x0 SErr 0x0 action 0x0
Dec  4 09:11:35 fw1-shimo kernel: ata2.00: (BMDMA stat 0x0)
Dec  4 09:11:35 fw1-shimo kernel: ata2.00: tag 0 cmd 0xc8 Emask 0x9 stat 0x51 err 0x40 (media error)
Dec  4 09:11:35 fw1-shimo kernel: ata2: EH complete
Dec  4 09:11:37 fw1-shimo kernel: ata3.00: exception Emask 0x0 SAct 0x0 SErr 0x0 action 0x0
Dec  4 09:11:37 fw1-shimo kernel: ata3.00: (BMDMA stat 0x60)
Dec  4 09:11:37 fw1-shimo kernel: ata3.00: tag 0 cmd 0x25 Emask 0x9 stat 0x51 err 0x40 (media error)
Dec  4 09:11:37 fw1-shimo kernel: ata3: EH complete
Dec  4 09:11:50 fw1-shimo kernel: ata3.00: exception Emask 0x0 SAct 0x0 SErr 0x0 action 0x0
Dec  4 09:11:51 fw1-shimo kernel: ata3.00: (BMDMA stat 0x60)
Dec  4 09:11:51 fw1-shimo kernel: ata3.00: tag 0 cmd 0x25 Emask 0x9 stat 0x51 err 0x40 (media error)
Dec  4 09:11:51 fw1-shimo kernel: ata3: EH complete
Dec  4 09:11:51 fw1-shimo kernel: ata3.00: exception Emask 0x0 SAct 0x0 SErr 0x0 action 0x0
Dec  4 09:11:52 fw1-shimo kernel: ata3.00: (BMDMA stat 0x60)
Dec  4 09:11:52 fw1-shimo kernel: ata3.00: tag 0 cmd 0x25 Emask 0x9 stat 0x51 err 0x40 (media error)
Dec  4 09:11:52 fw1-shimo kernel: ata3: EH complete
Dec  4 09:11:52 fw1-shimo setroubleshoot:      SELinux is preventing /usr/sbin/sendmail.postfix (system_mail_t) "read" to /dev/md1 (proc_mdstat_t).      For complete SELinux messages. run sealert -l d5c655f4-6fc3-445b-ab9d-3b21336cb2d0
Dec  4 09:11:52 fw1-shimo kernel: ata3.00: exception Emask 0x0 SAct 0x0 SErr 0x0 action 0x0
Dec  4 09:11:53 fw1-shimo kernel: ata3.00: (BMDMA stat 0x60)
Dec  4 09:11:53 fw1-shimo kernel: ata3.00: tag 0 cmd 0x25 Emask 0x9 stat 0x51 err 0x40 (media error)
Dec  4 09:11:53 fw1-shimo kernel: ata3: EH complete
Dec  4 09:11:53 fw1-shimo kernel: ata3.00: exception Emask 0x0 SAct 0x0 SErr 0x0 action 0x0
Dec  4 09:11:53 fw1-shimo kernel: ata3.00: (BMDMA stat 0x60)
Dec  4 09:11:54 fw1-shimo kernel: ata3.00: tag 0 cmd 0x25 Emask 0x9 stat 0x51 err 0x40 (media error)
Dec  4 09:11:54 fw1-shimo kernel: sd 2:0:0:0: SCSI error: return code = 0x08000002
Dec  4 09:11:54 fw1-shimo kernel: sdc: Current: sense key: Medium Error
Dec  4 09:11:54 fw1-shimo kernel:     Additional sense: Unrecovered read error - auto reallocate failed
Dec  4 09:11:55 fw1-shimo kernel: end_request: I/O error, dev sdc, sector 25091744
Dec  4 09:11:55 fw1-shimo kernel: ata3: EH complete
Dec  4 09:11:55 fw1-shimo kernel: SCSI device sdc: 781422768 512-byte hdwr sectors (400088 MB)
Dec  4 09:11:55 fw1-shimo kernel: sdc: Write Protect is off
Dec  4 09:11:56 fw1-shimo kernel: SCSI device sdc: drive cache: write back
Dec  4 09:11:56 fw1-shimo kernel: SCSI device sdb: 781422768 512-byte hdwr sectors (400088 MB)
Dec  4 09:11:56 fw1-shimo kernel: sdb: Write Protect is off
Dec  4 09:11:57 fw1-shimo kernel: SCSI device sdb: drive cache: write back
Dec  4 09:11:57 fw1-shimo kernel: SCSI device sdc: 781422768 512-byte hdwr sectors (400088 MB)
Dec  4 09:11:57 fw1-shimo kernel: Incorrect number of segments after building list
Dec  4 09:11:57 fw1-shimo kernel: counted 127, received 15
Dec  4 09:11:58 fw1-shimo kernel: req nr_sec 0, cur_nr_sec 8
Dec  4 09:11:58 fw1-shimo kernel: raid1: Disk failure on sdc2, disabling device. 
Dec  4 09:11:58 fw1-shimo kernel:       Operation continuing on 2 devices
Dec  4 09:11:58 fw1-shimo kernel: blk: request botched
Dec  4 09:11:58 fw1-shimo kernel: Incorrect number of segments after building list
Dec  4 09:11:59 fw1-shimo kernel: counted 112, received 16
Dec  4 09:11:59 fw1-shimo kernel: req nr_sec 0, cur_nr_sec 8
Dec  4 09:11:59 fw1-shimo kernel: blk: request botched
Dec  4 09:11:59 fw1-shimo kernel: sdc: Write Protect is off
Dec  4 09:12:00 fw1-shimo kernel: Incorrect number of segments after building list
Dec  4 09:12:00 fw1-shimo kernel: counted 96, received 16
Dec  4 09:12:00 fw1-shimo kernel: req nr_sec 0, cur_nr_sec 8
Dec  4 09:12:01 fw1-shimo kernel: blk: request botched
Dec  4 09:12:01 fw1-shimo kernel: Incorrect number of segments after building list
Dec  4 09:12:01 fw1-shimo kernel: counted 80, received 16
Dec  4 09:12:01 fw1-shimo kernel: req nr_sec 0, cur_nr_sec 8
Dec  4 09:12:02 fw1-shimo kernel: blk: request botched
Dec  4 09:12:02 fw1-shimo kernel: Incorrect number of segments after building list
Dec  4 09:12:02 fw1-shimo kernel: counted 64, received 16
Dec  4 09:12:02 fw1-shimo kernel: req nr_sec 0, cur_nr_sec 8
Dec  4 09:12:03 fw1-shimo kernel: blk: request botched
Dec  4 09:12:03 fw1-shimo kernel: SCSI device sdc: drive cache: write back
Dec  4 09:12:03 fw1-shimo kernel: Incorrect number of segments after building list
Dec  4 09:12:03 fw1-shimo kernel: counted 48, received 16
Dec  4 09:12:04 fw1-shimo kernel: req nr_sec 0, cur_nr_sec 8
Dec  4 09:12:04 fw1-shimo kernel: blk: request botched
Dec  4 09:12:04 fw1-shimo kernel: Incorrect number of segments after building list
Dec  4 09:12:04 fw1-shimo kernel: counted 32, received 16
Dec  4 09:12:05 fw1-shimo kernel: req nr_sec 0, cur_nr_sec 8
Dec  4 09:12:05 fw1-shimo kernel: blk: request botched
Dec  4 09:12:05 fw1-shimo kernel: ata3.00: WARNING: zero len r/w req
Dec  4 09:12:06 fw1-shimo last message repeated 5 times</code>

<b>Step 1: Drop the failed slice</b>

<code># /sbin/mdadm /dev/md1 --fail /dev/sdc2
mdadm: set /dev/sdc2 faulty in /dev/md1
# /sbin/mdadm /dev/md1 --remove /dev/sdc2
mdadm: hot removed /dev/sdc2</code>

<b>Step 2: Zero out the failed slice</b>

My thinking here is that by zeroing out the failed slice, I can force the SATA disk to remap any sectors that have gone bad.

<code># dd if=/dev/zero of=/dev/sdc2
dd: writing to `/dev/sdc2': Input/output error
24577993+0 records in
24577992+0 records out
12583931904 bytes (13 GB) copied, 1916.7 seconds, 6.6 MB/s</code>

Well, that's not a good sign (and the disk was clicking a bit).  So I'll run smartctl and check the disk's SMART info (see [Monitoring Hard Disks with SMART](http://www.linuxjournal.com/article/6983)).

<code># /usr/sbin/smartctl -i -d ata /dev/sdc
smartctl version 5.36 [x86_64-redhat-linux-gnu] Copyright (C) 2002-6 Bruce Allen
Home page is http://smartmontools.sourceforge.net/

=== START OF INFORMATION SECTION ===
Device Model:     SAMSUNG HD400LJ
Serial Number:    S0H2J1KLA07831
Firmware Version: ZZ100-15
User Capacity:    400,088,457,216 bytes
Device is:        In smartctl database [for details use: -P show]
ATA Version is:   7
ATA Standard is:  ATA/ATAPI-7 T13 1532D revision 4a
Local Time is:    Wed Dec  5 09:43:36 2007 EST

==&gt; WARNING: May need -F samsung or -F samsung2 enabled; see manual for details.

SMART support is: Available - device has SMART capability.
SMART support is: Enabled</code>

However, the "-Hc" output of smartctl says that the disk health is still "PASSED" and not "FAILING".  So it's possible that the disk doesn't need to be retired yet.

<code># /usr/sbin/smartctl -Hc -d ata /dev/sdc
smartctl version 5.36 [x86_64-redhat-linux-gnu] Copyright (C) 2002-6 Bruce Allen
Home page is http://smartmontools.sourceforge.net/

=== START OF READ SMART DATA SECTION ===
SMART overall-health self-assessment test result: PASSED

General SMART Values:
Offline data collection status:  (0x05) Offline data collection activity
                                        was aborted by an interrupting command from host.
                                        Auto Offline Data Collection: Disabled.
Self-test execution status:      ( 121) The previous self-test completed having
                                        the read element of the test failed.
Total time to complete Offline 
data collection:                 (7640) seconds.
Offline data collection
capabilities:                    (0x5b) SMART execute Offline immediate.
                                        Auto Offline data collection on/off support.
                                        Suspend Offline collection upon new
                                        command.
                                        Offline surface scan supported.
                                        Self-test supported.
                                        No Conveyance Self-test supported.
                                        Selective Self-test supported.
SMART capabilities:            (0x0003) Saves SMART data before entering
                                        power-saving mode.
                                        Supports SMART auto save timer.
Error logging capability:        (0x01) Error logging supported.
                                        General Purpose Logging supported.
Short self-test routine 
recommended polling time:        (   2) minutes.
Extended self-test routine
recommended polling time:        ( 130) minutes.</code>

Personally, since I know the drive makes clicking noises and throws an error during the dd wipe, I'm going to swap it out.
