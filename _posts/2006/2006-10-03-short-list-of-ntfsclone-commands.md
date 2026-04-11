---
layout: post
title: 'Short list of NTFSClone commands'
date: '2006-10-03T14:08:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


This assumes that you have a hidden Linux partition (ext2/ext3) on the hard drive and that you're creating an image on that hidden drive.  Most of the time that means you're writing to either /dev/hda2 or /dev/sda2, but you should double-check that.

List the partitions on the known hard drives:
```
# fdisk -l
```

Mount the hidden Linux partition:
```
# mkdir /mnt/image
# mount /dev/hda2 /mnt/image
# mkdir /mnt/image/machinename-date
# cd /mnt/image/machinename-date
```

Image the drive (be very careful with commands!):
```
# sfdisk -d /dev/hda > machinename-date-hda.sfdisk.dump
# dd if=/dev/hda bs=512 count=1 of=machinename-date-hda.mbr
# ntfsclone -s -o - /dev/hda1 | gzip | split -b 500m - machinename-date-ntfsclone-hda1.img.gz_
```

Notes:

- There are two places in the command where a "-" appears by itself. These are critical as they tell ntfsclone to pipe to standard output ("-o -") and that the split command should pull from standard input ("-" by itself).

- You'll probably want to use the underscore ("_") on the end of the image filename so that split adds the 2-letter suffix (aa, ab, ac, etc) in a way that is not confusing.

- Note, the split size of 500MB is used in order to avoid the 2GB limit when writing to SMB network shares.  Plus it lets you spread the files across multiple disks if needed.
