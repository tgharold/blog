---
layout: post
title: 'Resizing an ext3 partition in an LVM2 volume'
date: '2005-12-12T11:31:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---



[Extending a Logical Volume](http://www.netadmintools.com/art366.html)

The basic (3) commands are:

lvextend
e2fsck 
resize2fs

For example, I have /home that is currently a 4GB partition mounted in my vgmirror volume group.  In order to turn /home into a 64GB partition, I need to use the following commands.

```
# pvscan
# lvscan
# umount /home
(if you can't unmount the volume, you may need to boot the LiveCD)
# lvextend -L+60G /dev/vgmirror/home
# e2fsck -f /dev/vgmirror/home
# resize2fs /dev/vgmirror/home
# mount /home
```

Now, for /home, odds are high that you will have to boot a LiveCD due to the volume being in use.
