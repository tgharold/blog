---
layout: post
title: 'Benchmarking - hdparm'
date: '2006-08-19T14:47:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


So as I prepare for the iSCSI build, I need to start gathering tools to help me find bottlenecks.  As well as establishing baseline performance estimates.

<b>hdparm -tT {blockdevice name}</b> - This tool ships standard with most (all?) versions of Linux.  It's a read-only, non-destructive (if used properly), command that can be used to test raw read performance from any block device.  So you can check individual drives in a RAID array as well as doing a quick check of the over all RAID array performance.  Run time is generally around 10 seconds.

Here are some sample runs from my firewall box (VIA C3 600MHz, 1GB RAM, 2x60GB 5400rpm notebook drives):

```
nezumi backup1 # hdparm -tT /dev/md2

/dev/md2:
 Timing cached reads:   276 MB in  2.02 seconds = 136.88 MB/sec
 Timing buffered disk reads:  106 MB in  3.06 seconds =  34.61 MB/sec

nezumi backup1 # hdparm -tT /dev/hda2

/dev/hda2:
 Timing cached reads:   276 MB in  2.02 seconds = 136.78 MB/sec
 Timing buffered disk reads:   90 MB in  3.04 seconds =  29.58 MB/sec

nezumi backup1 # hdparm -tT /dev/hdc3

/dev/hdc3:
 Timing cached reads:   276 MB in  2.02 seconds = 136.87 MB/sec
 Timing buffered disk reads:   88 MB in  3.04 seconds =  28.91 MB/sec

nezumi backup1 # hdparm -tT /dev/md2 

/dev/md2:
 Timing cached reads:   276 MB in  2.02 seconds = 136.49 MB/sec
 Timing buffered disk reads:  108 MB in  3.03 seconds =  35.65 MB/sec

nezumi backup1 # hdparm -tT /dev/md2

/dev/md2:
 Timing cached reads:   276 MB in  2.02 seconds = 136.72 MB/sec
 Timing buffered disk reads:  108 MB in  3.00 seconds =  35.99 MB/sec
```

What you will notice is that the "cached" reads value has more to do with the memory speed then the speed of the disk.  The buffered disk read values are closer to real-world performance values.  There are no surprises in the performance of the VIA C3 system.

However, on my older Gigabyte Celeron 566MHz system, there's a big surprise:

```
coppermine thomas # hdparm -tT /dev/hda4

/dev/hda4:
 Timing cached reads:   336 MB in  2.00 seconds = 167.99 MB/sec
 Timing buffered disk reads:   10 MB in  3.18 seconds =   3.15 MB/sec

coppermine thomas # hdparm -tT /dev/hde4

/dev/hde4:
 Timing cached reads:   336 MB in  2.01 seconds = 167.32 MB/sec
 Timing buffered disk reads:   86 MB in  3.07 seconds =  27.99 MB/sec

coppermine thomas # hdparm -tT /dev/hdg1

/dev/hdg1:
 Timing cached reads:   336 MB in  2.00 seconds = 167.65 MB/sec
 Timing buffered disk reads:   58 MB in  3.02 seconds =  19.20 MB/sec

coppermine thomas # hdparm -tT /dev/md2 

/dev/md2:
 Timing cached reads:   336 MB in  2.01 seconds = 166.99 MB/sec
 Timing buffered disk reads:   12 MB in  3.28 seconds =   3.66 MB/sec

coppermine thomas # hdparm -tT /dev/md3

/dev/md3:
 Timing cached reads:   336 MB in  2.00 seconds = 167.65 MB/sec
 Timing buffered disk reads:   10 MB in  3.18 seconds =   3.15 MB/sec
```

This shows that there are severe performance issues with any block devices using /dev/hda (such as /dev/md2 and /dev/md3).  The motherboard chipset is either extremely slow, or there are performance bottlenecks that need to be investigated.

The test results also show that the old Celeron 566MHz is slightly faster then the VIA C3 (167MB/s vs 137MB/s).  So if I can find and fix the bottleneck for /dev/hda, I should see a significant increase in performance from this particular unit.

```
nogitsune etc # hdparm -tT /dev/hda

/dev/hda:
 Timing cached reads:   3220 MB in  2.00 seconds = 1609.90 MB/sec
 Timing buffered disk reads:  172 MB in  3.02 seconds =  56.95 MB/sec

nogitsune etc # hdparm -tT /dev/sda

/dev/sda:
 Timing cached reads:   3236 MB in  2.00 seconds = 1617.90 MB/sec
 Timing buffered disk reads:  184 MB in  3.00 seconds =  61.25 MB/sec

nogitsune etc # hdparm -tT /dev/md3

/dev/md3:
 Timing cached reads:   3208 MB in  2.00 seconds = 1603.90 MB/sec
 Timing buffered disk reads:  188 MB in  3.03 seconds =  62.08 MB/sec

nogitsune etc # hdparm -tT /dev/hde1

/dev/hde1:
 Timing cached reads:   3228 MB in  2.00 seconds = 1613.90 MB/sec
 Timing buffered disk reads:  136 MB in  3.01 seconds =  45.15 MB/sec

nogitsune etc # hdparm -tT /dev/hdg1

/dev/hdg1:
 Timing cached reads:   3232 MB in  2.00 seconds = 1615.90 MB/sec
 Timing buffered disk reads:  136 MB in  3.00 seconds =  45.27 MB/sec

nogitsune etc # hdparm -tT /dev/md4

/dev/md4:
 Timing cached reads:   3244 MB in  2.00 seconds = 1621.90 MB/sec
 Timing buffered disk reads:  136 MB in  3.00 seconds =  45.33 MB/sec

nogitsune etc # hdparm -tT /dev/hdk1

/dev/hdk1:
 Timing cached reads:   3232 MB in  2.00 seconds = 1615.90 MB/sec
 Timing buffered disk reads:  136 MB in  3.01 seconds =  45.21 MB/sec

nogitsune etc # hdparm -tT /dev/hdo1

/dev/hdo1:
 Timing cached reads:   3224 MB in  2.00 seconds = 1611.90 MB/sec
 Timing buffered disk reads:  136 MB in  3.00 seconds =  45.33 MB/sec

nogitsune etc # hdparm -tT /dev/hds1

/dev/hds1:
 Timing cached reads:   3224 MB in  2.00 seconds = 1611.90 MB/sec
 Timing buffered disk reads:  134 MB in  3.01 seconds =  44.49 MB/sec

nogitsune etc # hdparm -tT /dev/md5

/dev/md5:
 Timing cached reads:   3224 MB in  2.00 seconds = 1611.90 MB/sec
 Timing buffered disk reads:  266 MB in  3.01 seconds =  88.43 MB/sec

nogitsune etc # hdparm -tT /dev/sdb1

/dev/sdb1:
 Timing cached reads:   3232 MB in  2.00 seconds = 1615.90 MB/sec
 Timing buffered disk reads:  162 MB in  3.01 seconds =  53.85 MB/sec
```

What we see here is that for the RAID1 arrays, speed is equivalent to the disks within the array.  But for the RAID5 array with (3) disks, speed is 2x that of the single disks within the array.
