---
layout: post
title: 'Gentoo: Segmentation fault in vgscan during boot'
date: '2004-06-19T14:31:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Now for the other error that I got during the initial bootup.
<pre>* Using /etc/modules.autoload.d/kernel-2.6 as config:
* Loading module dm-mod...                                                 [ ok ]
* Autoloaded 1 module(s)
* Setting up the Logical Volume Manager...
/sbin/rc: line 429: 4422 Segmentation Fault /sbin/vgscan &gt;/dev/nul         [ ok ]
* Starting up RAID devices: ...
* Checking all filesystems...
/dev/md0: clean, 39/18072 files, 5573/72192 blocks
fsck.ext: No such file or directory while trying to open /dev/vgmirror/opt
/dev/vgmirror/opt:
The superblock could not be read or does not describe a correct ext2
filesystem.  If the device is valid and it really contains an ext2
filesystem (and not swap or ufs or something else), then the superblock
is corrupt and you might try running e2fsck with an alternate superblock:
    e2fsck -b 8193 <device>

("No such file or directory..." error repeats for all of the other 
logical volumes in the volume group(s) on the system)</device></pre>

My initial guess is that the software RAID is not loading up prior to the LVM stuff trying to load.  Possibly, I'll have to edit the ordering in "/etc/init.d/checkfs", however since RAID is compiled into the kernel as built-in, and the LVM stuff is a module, the RAID should've already started prior to the LVM stuff.

Looking closer at the boot screen, I can see the "md:" lines correctly autodetecting the RAID arrays.  So RAID support seems to be working fine.  In fact, if I login to maintenance mode, and "<b>cat /proc/mdstat</b>", all of the RAID arrays show up correctly.

<b>Attempt #1:</b> 

Moved things around in /etc/init.d/checkfs.  No change in the end-result, except that the messages are re-ordered ("Starting up RAID devices" now appears before "Setting up the Logical Volume Manager") and the error message changes to "4422 Segmentation Fault /sbin/vgscan &gt;/dev/nul".  Probably a dry-hole in terms of finding and fixing the real problem.

<b>Attempt #2:</b> 

Flipped back to the [Gentoo LVM2 documents](http://www.gentoo.org/doc/en/lvm2.xml) to see if I missed anything in setting up the LVM set to auto-mount at startup.  Booted my way into maintenance mode and use "<b>vgscan -v</b>" to let vgscan attempt to find all of the volume groups.  "vgscan" will take a while to run, at least with verbose (-v) mode you'll be able to see some status.  On my setup, "vgscan" correctly located the "vgmirror" volume group.

Did a look at the "/etc/lvm" folder on the root volume using "<b>ls -la /etc/lvm</b>" and saw something surprising.  There is a ".cache" file which is <b>huge</b> (mine was 10881785 in size).  Doing a "cat" of the contents, I see some entries like "/dev/discs/disc2/discs/disc2.../disc2/md/254" which looks like a recursive loop of some sort.  

Hint #2, run "vgdisplay -vv" and I see the error message "Too many levels of symbolic links" after each of those long entries.  I also see this problem if I run "vgscan -vv".  I finally changed my "/etc/lvm/lvm.conf" file to look like the following, and vgscan and vgdisplay are very quick at finding the volume group on my raid array and no longer segfault while looking at other items:
<pre>devices = {
    scan=["/dev/md"]
    filter=["a|^/dev/md/3$|","r/.*/"]
    }</pre>

Note that this filter only allows vgscan to scan the "md3" device.    This keeps vgscan from scanning other devices that don't need to be scanned on my system (and fixes the segfault issue where it goes into infinite recursion on certain devices).  If you need to scan other RAID devices (/dev/md1, etc.) or other physical partitions, then you'll need to adjust the "accept" portion of the filter.

Save, shutdown the raid (<b>raidstop -a /dev/md0</b> for each /dev/md* device), and reboot.  My server now boots up correctly.

Links:

[Re: mkfs.xfs on software raid5 (2.6.5 kernel) - MD array /dev/md2 not in clean state ](http://groups.google.com/groups?hl=en&amp;lr=&amp;ie=UTF-8&amp;c2coff=1&amp;selm=Sb%25zc.38791%24ih7.31403%40fe2.columbus.rr.com) (alt.os.linux.gentoo) - Shows the exact error message that I'm seeing.

[Re: [gentoo-user] LVM2 ](http://groups.google.com/groups?hl=en&amp;lr=&amp;ie=UTF-8&amp;c2coff=1&amp;threadm=1FXah-4Up-49%40gated-at.bofh.it&amp;rnum=2&amp;prev=/groups%3Fq%3D%252Blvm%2B%252B%2522software%2Braid%2522%2B%252Blinux%2B%252Bgentoo%2B%252Border%26hl%3Den%26lr%3D%26ie%3DUTF-8%26c2coff%3D1%26selm%3D1FXah-4Up-49%2540gated-at.bofh.it%26rnum%3D2) Date: 2004-03-31 15:40:13 PST (linux.gentoo.user) - Talks about the ordering in which software RAID and the LVM modules load.

[Example of lvm.conf file](https://www.redhat.com/archives/linux-lvm/2003-December/msg00009.html) - shows a more complex lvm.conf file, complete with multiple filters.

[A more complete example lvm.conf file](http://gondor.com/lvm/lvm.conf)
