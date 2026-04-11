---
layout: post
title: 'SAN design - part 2'
date: '2006-08-19T15:40:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Trying to decide how to allocate disks within the SAN unit.  I have (14) or (17) slots.  For now, I'll assume that the 5:3 bay units work which will give me a total of 17 disks.

<pre>-------------------------------------------------
BAYS / DRIVE CONFIGURATION (2 INT, 15 BAY-COOLER)
-------------------------------------------------
INT1    M/B      RAID1(A)    RAID1(A)
INT2    ''       ''          ''
BCA1    ''       RAID1(B1)   RAID1(B1)
BCA2    ''       RAID1(B2)   RAID1(B2)
BCA3    ''       RAID1(B3)   RAID1(B3)
BCA4    HP2300   RAID1(B1)   RAID1(B1)
BCA5    ''       RAID1(B2)   RAID1(B2)
BCB1    ''       RAID1(B3)   RAID1(B3)
BCB2    ''       HOT SPARE   HOT SPARE
BCB3    HP2320   RAID1 (C1)  RAID6(C)
BCB4    ''       ''          ''
BCB5    ''       RAID1 (C2)  ''
BCC1    ''       ''          ''
BCC2    ''       RAID1 (C3)  ''
BCC3    ''       ''          ''
BCC4    ''       RAID1 (C4)  ''
BCC5    ''       ''          ''</pre>

INTx - Internal drive bay at back of case
BCAx - 5:3 bay cooler
BCBx - 5:3 bay cooler
BCCx - 5:3 bay cooler

M/B - Indicates that I'm using the 5 SATA ports on the motherboard
HP2300 - HighPoint RocketRAID 2300 PCIe x1 SATA 4-port
HP2320 - HighPoint RocketRAID 2320 PCIe x4 SATA 8-port

A) In the first configuration I have:

700GB RAID1
2100GB RAID0 over (3) RAID1 sets
2800GB RAID0 over (4) RAID1 sets
====
5600GB total (11200GB gross capacity)

B) The second configuration sets up a 8-disk RAID6 array

700GB RAID1
2100GB RAID0 over (3) RAID1 sets
4200GB RAID6 over 8 disks
====
7000GB total (11200GB gross capacity)

The RAID0 over (3) RAID1 sets (a.k.a. RAID 10) should give me roughly 3x the performance of a regular RAID1 volume.  Reads and writes should both see a 3x improvement over a simple RAID1.

For the RAID6 volume, I estimate that read performance will be 6x that of the RAID1 set but I'm not sure what write performance will be.
