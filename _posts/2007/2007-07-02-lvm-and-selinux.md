---
layout: post
title: 'LVM and SELinux'
date: '2007-07-02T15:38:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


I was a bit perplexed... I had created a LV called /dev/vg/svn, had it mounted, was reading/writing data to it with no issues.  But after I rebooted the CentOS5 server, I'm unable to mount the LV.

```
[root@localhost /]# /usr/sbin/pvscan
PV /dev/md6   VG vg   lvm2 [144.78 GB / 59.78 GB free]
Total: 1 [144.78 GB] / in use: 1 [144.78 GB] / in no VG: 0 [0   ]
[root@localhost /]# /usr/sbin/vgscan
Reading all physical volumes.  This may take a while...
Found volume group "vg" using metadata type lvm2
[root@localhost /]# /usr/sbin/lvscan
No volume groups found
[root@localhost /]# /usr/sbin/lvdisplay
No volume groups found
[root@localhost /]# /usr/sbin/lvdisplay vg
--- Logical volume ---
LV Name                /dev/vg/svn
VG Name                vg
LV UUID                taYjia-BWWs-IWG3-313k-VoC2-ghik-01mFCg
LV Write Access        read/write
LV Status              NOT available
LV Size                85.00 GB
Current LE             21760
Segments               1
Allocation             inherit
Read ahead sectors     0

[root@localhost /]# 
```

So lvdisplay knows that the LV is there, but only if I tell it to look at the VG named "vg".

...

Turns out that it's an SELinux issue.  Because SELinux was blocking access to the /etc/lvm/.cache file, it was causing problems.  Fixing it was as simple as:

```
# cd /etc/lvm
# /sbin/restorecon -v .cache
# /usr/sbin/lvscan
inactive          '/dev/vg/svn' [85.00 GB] inherit
```
