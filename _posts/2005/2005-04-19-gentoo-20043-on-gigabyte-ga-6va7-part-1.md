---
layout: post
title: 'Gentoo 2004.3 on Gigabyte GA-6VA7+ (part 1)'
date: '2005-04-19T16:21:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---



<b>Note: These directions are works-in-progress... in fact, they might not even work at all until I find out why I'm ending up with non-bootable systems (looks like a bug in the 2.6 kernel).</b>

This is a continuation of [Gentoo and Software RAID (2004.3)](/blog/2005-04-19-gentoo-and-software-raid-20043), where I configured the disks and setup the RAID array.  I'm now picking up at the point where the RAID array has been configured and we're ready to start installing file systems.

/dev/md0 - 128MB boot
/dev/md1 - 2GB root partition
/dev/md2 - 2GB swap
/dev/md3 - rest of disk (user files)

Now, some folks say copy the /etc/mdadm.conf file, but in the same breath, they indicate that mdadm does not require the use of a config file at all.  Since I'm documenting my configuration here, and my array is extremely straightforward, I'm going to skip creating the mdadm.conf file and see how it goes.

Links:
[Software RAID (Gentoo Tips-n-Tricks)](http://www.gentoo.org/doc/en/gentoo-x86-tipsntricks.xml)
[LinuxDevCenter article on mdadm](http://www.linuxdevcenter.com/pub/a/linux/2002/12/05/RAID.html)

The LinuxDevCenter article actually explains how to create the mdadm.conf file yourself (semi-automatically).  Notice the use of wild cards that lets me compactly express that I want all 4 partitions on /dev/hda and /dev/hdc to be used in arrays.  You will need to edit the results to match the syntax of the mdadm.conf file.

```
# echo 'DEVICES /dev/hda*' >> /etc/mdadm.conf
# echo 'DEVICES /dev/hdc*' >> /etc/mdadm.conf
# mdadm --detail --scan >> /etc/mdadm.conf
# nano -w /etc/mdadm.conf
```

Contents of my mdadm.conf file:

```
EVICES /dev/hda*
DEVICES /dev/hdc*
ARRAY /dev/md3 level=raid1 num-devices=2 devices=/dev/hda4,/dev/hdc4                                
ARRAY /dev/md2 level=raid1 num-devices=2 devices=/dev/hda3,/dev/hdc3                                
ARRAY /dev/md1 level=raid1 num-devices=2 devices=/dev/hda2,/dev/hdc2                                
ARRAY /dev/md0 level=raid1 num-devices=2 devices=/dev/hda1,/dev/hdc1 
```

Picking up again with [Chapter 4 of the installation handbook](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&chap=4).  This is also very similar to what I did back in [June 2004 with Software RAID and LVM2](/blog/2004-06-15-gentoo-install-2-via-epia-me6000/).

```
# mke2fs /dev/md0
# mke2fs -j /dev/md1
# mkswap /dev/md2
# swapon /dev/md2
# mount /dev/md1 /mnt/gentoo
# mkdir /mnt/gentoo/boot
# mount /dev/md0 /mnt/gentoo/boot
```

Now, we initialize the 4th raid partition for LVM2 operations.  See [Gentoo LVM2 Documentation](http://www.gentoo.org/doc/en/lvm2.xml) for more details about this.

```
# modprobe dm-mod
# pvcreate /dev/md3
# echo 'devices { filter=["r/cdrom/"] }' >/etc/lvm/lvm.conf
# vgcreate vgmirror /dev/md3
# vgscan
```

Here is my plan for logical volumes inside the vgmirror partition (this uses up 22GB):

4GB /tmp (ext2)
4GB /var/tmp (ext2)
2GB /opt (ext3)
4GB /usr (ext3)
4GB /var (ext3)
4GB /home (ext3)

Create the logical volumes.  If you see the error message "/etc/lvm/backup: fsync failed: Invalid argument", you can ignore this warning (according to [Gentoo's LVM2 page](http://www.gentoo.org/doc/en/lvm2.xml)).

```
# lvcreate -L4G -ntmp vgmirror
# lvcreate -L4G -nvartmp vgmirror
# lvcreate -L2G -nopt vgmirror
# lvcreate -L4G -nusr vgmirror
# lvcreate -L4G -nvar vgmirror
# lvcreate -L4G -nhome vgmirror
# ls -l /dev/vgmirror
# lvscan
```

Output of the lvscan command:

```
  ACTIVE            '/dev/vgmirror/tmp' [4.00 GB] next free (default)
  ACTIVE            '/dev/vgmirror/vartmp' [4.00 GB] next free (default)
  ACTIVE            '/dev/vgmirror/opt' [2.00 GB] next free (default)
  ACTIVE            '/dev/vgmirror/usr' [4.00 GB] next free (default)
  ACTIVE            '/dev/vgmirror/var' [4.00 GB] next free (default)
  ACTIVE            '/dev/vgmirror/home' [4.00 GB] next free (default)
```

Format the logical volumes:

```
# mke2fs /dev/vgmirror/tmp
# mke2fs /dev/vgmirror/vartmp
# mke2fs -j /dev/vgmirror/opt
# mke2fs -j /dev/vgmirror/usr
# mke2fs -j /dev/vgmirror/var
# mke2fs -j /dev/vgmirror/home
```

Make the directories to hold your mounted volumes. Mount your volumes.

```
# mkdir /mnt/gentoo/opt
# mkdir /mnt/gentoo/usr
# mkdir /mnt/gentoo/var
# mkdir /mnt/gentoo/home
# mount /dev/vgmirror/opt /mnt/gentoo/opt
# mount /dev/vgmirror/usr /mnt/gentoo/usr
# mount /dev/vgmirror/var /mnt/gentoo/var
# mount /dev/vgmirror/home /mnt/gentoo/home
```

Make the special directories to hold your temp file volumes (these require special permissions). Then mount your temp file volumes. Also mount your proc folder.

```
# mkdir /mnt/gentoo/tmp
# mount /dev/vgmirror/tmp /mnt/gentoo/tmp
# chmod 1777 /mnt/gentoo/tmp
# mkdir /mnt/gentoo/var/tmp
# mount /dev/vgmirror/vartmp /mnt/gentoo/var/tmp
# chmod 1777 /mnt/gentoo/var/tmp
# mkdir /mnt/gentoo/proc
# mount -t proc none /mnt/gentoo/proc
```

Now we move into [Installation (chapter 5)](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&chap=5) in the handbook.  Verify your system date and then start extracting the tarballs.

```
# date
# ls -l /mnt/cdrom/stages
# cd /mnt/gentoo
# tar -xvjpf /mnt/cdrom/stages/stage1-x86-2004.3.tar.bz2
# ls -l /mnt/cdrom/snapshots
# cd /mnt/gentoo
# tar -xvjf /mnt/cdrom/snapshots/portage-20041022.tar.bz2 -C /mnt/gentoo/usr
# cd /mnt/gentoo
# mkdir /mnt/gentoo/usr/portage/distfiles
# cp /mnt/cdrom/distfiles/* /mnt/gentoo/usr/portage/distfiles/
```

Before I configure the make.conf file, I should take a look at my system configuration.

```
# cat /proc/version
Linux version 2.6.9-gentoo-r1 (root@inertia) (gcc version 3.3.4 20040623 (Gentoo Linux 3.3.4-r1, ssp-3.3.2-2, pie-8.7.6)) #1 SMP Thu Nov 25 03:43:53 UTC 2004
# cat /proc/cpuinfo
processor       : 0
vendor_id       : GenuineIntel
cpu family      : 6
model           : 8
model name      : Celeron (Coppermine)
stepping        : 6
cpu MHz         : 568.097
cache size      : 128 KB
fdiv_bug        : no
hlt_bug         : no
f00f_bug        : no
coma_bug        : no
fpu             : yes
fpu_exception   : yes
cpuid level     : 2
wp              : yes
flags           : fpu vme de pse tsc msr pae mce cx8 sep mtrr pge mca cmov pat pse36 mmx fxsr sse
bogomips        : 1114.11
```

Now we're ready to edit the make.conf file and change flags:

```
# nano -w /mnt/gentoo/etc/make.conf
```

Here is my personal make.conf (<b>use at your own risk</b>).  This is for a Celeron Coppermine CPU (Pentium III).  I prefer to compile for size given the small amount of installed RAM on this system.

```
CFLAGS="-Os -march=pentium3 -pipe -fomit-frame-pointer"
CHOST="i686-pc-linux-gnu"
CXXFLAGS="${CFLAGS}"
MAKEOPTS="-j2"
USE="apache2 kerberos ldap -apm -gif -gnome -gtk -jpeg -kde -mad -mikmod -mpeg -oggvorbis -opengl -oss -pdflib -png -qt -quicktime -sdl -truetype -xmms -xv"
```

Pick up again with [Installing the Gentoo Base System](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&chap=6) in the handbook.  Where we pick a mirror and start the move from stage1 to stage3.  I see that the mirrorselect command has changed between 2004.0 and 2004.3.

```
# mirrorselect -i -o >> /mnt/gentoo/etc/make.conf
# mirrorselect -i -r -o >> /mnt/gentoo/etc/make.conf
```

This should have dumped 2 extra lines into your make.conf file (cat /mnt/gentoo/etc/make.conf).  Here is what got added to my make.conf file:

```
GENTOO_MIRRORS="http://gentoo.osuosl.org/ http://csociety-ftp.ecn.purdue.edu/pub/gentoo/ http://gentoo.chem.wisc.edu/gentoo/"
SYNC="rsync://rsync.us.gentoo.org/gentoo-portage"
```

Now we need to copy some files.

```
# cp -L /mnt/gentoo/etc/make.conf /mnt/gentoo/boot/make.conf-backupcopy
# cp -L /etc/resolv.conf /mnt/gentoo/etc/resolv.conf
# cp -L /etc/mdadm.conf /mnt/gentoo/etc/mdadm.conf
# cp -L /etc/mdadm.conf /mnt/gentoo/boot/mdadm.conf-backupcopy
# mkdir /mnt/gentoo/etc/lvm
# cp -L /etc/lvm/lvm.conf /mnt/gentoo/etc/lvm/lvm.conf
# cp -L /etc/lvm/lvm.conf /mnt/gentoo/boot/lvm.conf-backupcopy
```

Change into the new system (note that we already mounted the proc filesystem earlier).

```
# chroot /mnt/gentoo /bin/bash
# env-update
# source /etc/profile
# emerge --sync
```

This should update your portage tree to the latest version (and make take a while to run).

([See the next step](/2005-04-19-gentoo-20043-on-gigabyte-ga-6va7-part-1/))
