---
layout: post
title: 'Sluggish linux box, troubleshooting steps'
date: '2005-11-12T12:06:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Time to sit down and jot some things down so I can figure out which device/driver in my Gentoo AMD64 box is causing issues.  This gets a little complex because I have (5) 5400rpm 300GB PATA drives, (2) 7200rpm 300GB PATA drives and (1) 7200rpm 200GB SATA drive installed.

Back when I finally booted into the AMD64 LiveCD, I got the following information from /proc/partitions:

```
livecd ~ # cat /proc/partitions
major minor #blocks name

7 0 49712 loop0
33 0 292970160 hde - 300GB 5400rpm PATA (PDC20269)
34 0 292970160 hdg - 300GB 5400rpm PATA (PDC20269)
57 0 292970160 hdk - 300GB 5400rpm PATA (HPT302)
89 0 292970160 hdo - 300GB 5400rpm PATA (HPT302)
91 0 292970160 hds - 300GB 5400rpm PATA (HPT302)
3 0 293057352 hda - 300GB 7200rpm PATA (motherboard primary IDE)
8 0 293057352 sda - 300GB 7200rpm PATA (PDC20378 m/b)
8 16 199148544 sdb - 200GB 7200rpm SATA (m/b SATA)
livecd ~ #
```

Key:
HPT302 = HighPoint Rocket133SB PCI cards (1 PATA port per card)
PDC20269 = Promise Ultra133 TX2 PCI card (2 PATA ports)
PDC20378 = Promise RAID controller on A8V motherboard

So, that tells me that if I manage to get my kernel configured properly, I should be seeing all (8) drives with no sluggishness due to oddball drivers.  The question of the moment is how do I find out what configuration was used to build the Linux kernel on the LiveCD?  That, or I should look into attempting to use "genkernel" to create my settings semi-automatically.

I found the kernel configuration for the LiveCD by booting the LiveCD and looking at the compressed file /proc/config.gz.  You can see the contents of this file by using the command:

```
# cat /proc/config.gz | gzip -d | less
```

So I went and looked at the differences between my Nov 8th kernel (which works, except for support for the onboard Promise chip and the HPT302s) and my problematic Nov 9th kernel.

```
nogitsune linux # diff /boot/config-2.6.13-8Nov2005 /boot/config-2.6.13-9Nov2005
4c4
< # Tue Nov  8 18:19:03 2005
---
> # Wed Nov  9 05:13:43 2005
416c416
< # CONFIG_CHR_DEV_SG is not set
---
> CONFIG_CHR_DEV_SG=y
456c456
< # CONFIG_SCSI_SATA_PROMISE is not set
---
> CONFIG_SCSI_SATA_PROMISE=y
nogitsune linux #
```

That's it.  Just two changes to the .config file.  So I'm currently undoing the "CONFIG_CHR_DEV_SG=y" line and leaving the Promise SATA line in.  I've recompiled and I'm getting ready to reboot to see if it recognizes the PATA disk connected to the PDC20378 chip on the motherboard.

It did, but still didn't fix the issue of sluggishness.

Useful steps to know about when booting off the LiveCD for my system.  I manually reassemble the RAID items and mount all of my LVM2 partitions.

```
livecd ~ # modprobe md
livecd ~ # modprobe dm-mod
livecd ~ # modprobe raid1
livecd ~ # for i in 0 1 2 3; do mknod /dev/md$i b 9 $i; done
livecd ~ # swapon /dev/md1
swapon: /dev/md1: Invalid argument
livecd ~ # mdadm --assemble /dev/md0 /dev/hda1 /dev/sda1
mdadm: /dev/md0 has been started with 2 drives.
livecd ~ # mdadm --assemble /dev/md1 /dev/hda2 /dev/sda2
mdadm: /dev/md1 has been started with 2 drives.
livecd ~ # mdadm --assemble /dev/md2 /dev/hda3 /dev/sda3
mdadm: /dev/md2 has been started with 2 drives.
livecd ~ # mdadm --assemble /dev/md3 /dev/hda4 /dev/sda4
mdadm: /dev/md3 has been started with 1 drive (out of 2) and 1 spare.
livecd ~ # swapon /dev/md1
livecd ~ # mount /dev/md2 /mnt/gentoo
livecd ~ # mount /dev/md0 /mnt/gentoo/boot
livecd ~ # vgchange -ay vgmirror
  6 logical volume(s) in volume group "vgmirror" now active
livecd ~ # mount /dev/vgmirror/opt /mnt/gentoo/opt
livecd ~ # mount /dev/vgmirror/usr /mnt/gentoo/usr
livecd ~ # mount /dev/vgmirror/var /mnt/gentoo/var
livecd ~ # mount /dev/vgmirror/home /mnt/gentoo/home
livecd ~ # mount /dev/vgmirror/tmp /mnt/gentoo/tmp
livecd ~ # chmod 1777 /mnt/gentoo/tmp
livecd ~ # mount /dev/vgmirror/vartmp /mnt/gentoo/var/tmp
livecd ~ # chmod 1777 /mnt/gentoo/var/tmp
livecd ~ # mount -t proc none /mnt/gentoo/proc
livecd ~ # chroot /mnt/gentoo /bin/bash
livecd / # env-update
>>> Regenerating /etc/ld.so.cache...
livecd / # source /etc/profile
```

Modules that get loaded on the 2005.1 AMD64 LiveCD on my system:

```
livecd linux # cat /proc/modules
raid1 14720 4 - Live 0xffffffff880f9000
md 36480 5 raid1, Live 0xffffffff880ef000
ipv6 212928 10 - Live 0xffffffff880ba000
floppy 52824 0 - Live 0xffffffff880ac000
pcspkr 4056 0 - Live 0xffffffff880aa000
skge 30224 0 - Live 0xffffffff880a1000
dm_mod 39264 7 - Live 0xffffffff88096000
ata_piix 7812 0 - Live 0xffffffff88093000
ahci 9348 0 - Live 0xffffffff8808f000
sata_qstor 8068 0 - Live 0xffffffff8808c000
sata_vsc 6788 0 - Live 0xffffffff88089000
sata_uli 6144 0 - Live 0xffffffff88086000
sata_sis 5888 0 - Live 0xffffffff88083000
sata_sx4 11396 0 - Live 0xffffffff8807f000
sata_nv 7556 0 - Live 0xffffffff8807c000
sata_via 7172 0 - Live 0xffffffff88079000
sata_svw 6404 0 - Live 0xffffffff88076000
sata_sil 7940 0 - Live 0xffffffff88073000
sata_promise 9092 4 - Live 0xffffffff8806f000
libata 30856 12 ata_piix,ahci,sata_qstor,sata_vsc,sata_uli,sata_sis,sata_sx4,sata_nv,sata_via,sata_svw,sata_sil,sata_promise, Live 0xffffffff88066000
sbp2 19080 0 - Live 0xffffffff88060000
ohci1394 27596 0 - Live 0xffffffff88058000
ieee1394 63096 2 sbp2,ohci1394, Live 0xffffffff88047000
sl811_hcd 11392 0 - Live 0xffffffff88043000
ohci_hcd 17156 0 - Live 0xffffffff8803d000
uhci_hcd 26528 0 - Live 0xffffffff88035000
usb_storage 55616 0 - Live 0xffffffff88026000
usbhid 27680 0 - Live 0xffffffff8801e000
ehci_hcd 25864 0 - Live 0xffffffff88016000
usbcore 86008 7 sl811_hcd,ohci_hcd,uhci_hcd,usb_storage,usbhid,ehci_hcd, Live 0xffffffff88000000
livecd linux #
```
