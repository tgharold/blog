---
layout: post
title: 'Troubleshooting software RAID boot problems'
date: '2004-06-17T01:08:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


First problem is that the system boots straight into "grub".  Probably due to a missing "grub.conf" file, which I'm pretty sure I had written to the proper location earlier in the install. So I'll load the kernel by hand and fix the config file once I get the box to boot properly.
```
grub>
grub> cat /boot/grub/grub.conf
(no file found)

grub> root (hd0,0)
grub> kernel /kernel-2.6.6-gentoo root=/dev/md2
grub> boot
```

This starts the kernel boot process, which will then lead me to my second error.  In the meantime, if you use [shift-PgUp] and [shift-PgDn] you can scroll back and forth through the boot messages.  A minor problem is that since the raid didn't shutdown cleanly, there are numerous "md: md<i>x</i>: raid array is not clean -- starting background reconstruction" messages.  And I can't even begin to troubleshoot the "Kernel panic: No init found" error until resync is done (that's a 2.5-3.0 hour process).

Looking back at my [kernel configuration](/blog/2004-06-16-gentoo-install-5-manual-kernel-configuration/), I see that Software RAID with RAID1 support was compiled as BUILTIN, and ext2/ext3 were installed by default if I remember correctly.  Those are two of the possible errors that could cause the kernel not to be able to read from the "/" (root) partition.

Also possible is that the "/" filesystem was not properly mounted during the install.  The following is what I've tried to do in order to fix the issue (or at least diagnose the issue).  <b>I would strongly recommend that you do not use the following on a production system unless you understand what everything does.</b>  Since I don't have any data on the system (other then config files), I have a good amount of latitude with regards to what I can do.  Hopefully, since /boot, /usr, /opt, /var and /home are intact, things will go quicker then the first install.

This repair process is basically a complete reinstall because nothing else under "/" (root) actually got written to the hard drive.  Only the separately mounted folders such as /boot, /opt, /usr, /var, and /home were properly mounted.

<b>Note: The following steps assume that you have nothing on your partitions worth keeping, or that you've already backed everything up.</b>  I tried doing it without formatting the "/" partition, but the bootstrap.sh file keeps dying on line 84.  So I'm going to do a format of the "/" partition as well as /opt, /usr, /var, /tmp, and /var/tmp.

Boot the LiveCD, at the boot prompt be sure to pick the boot kernel and pass the arguments that you want, then load the raid and LVM modules.
```
boot: gentoo -nohotplug
(gentoo kernel now loads)

livecd root # modprobe md
livecd root # modprobe dm-mod
livecd root # modprobe via-rhine    (if your network adapter failed to autoload)
livecd root # net-setup eth0        (if your network adapter failed to autoload)
```

If you have a copy of your /etc/raidtab file on floppy, copy it in now, otherwise you'll have to re-key your /etc/raidtab by hand.  If you need, you can temporarly mount partitions to copy files from.
```
livecd root # nano -w /etc/raidtab
livecd root # raidstart -a
livecd root # cat /proc/mdstat
(verify that all raid sets are up and running)

livecd root # swapon /dev/md1
livecd root # mke2fs -j /dev/md2     (OVERWRITES YOUR / PARTITION)
livecd root # mount /dev/md2 /mnt/gentoo
livecd root # mkdir /mnt/gentoo/boot
livecd root # mount /dev/md0 /mnt/gentoo/boot
livecd root # ls /mnt/gentoo/boot
(if you have files already in /boot, this verifies that you mounted in the proper order)

livecd root # mkdir /etc/lvm
livecd root # echo 'devices { filter=["r/cdrom/"] }' > /etc/lvm/lvm.conf
livecd root # vgscan
(verify that it found your existing volume group or groups)

livecd root # vgchange -ay vgmirror
livecd root # lvscan
(verify that your logical volumes now show up and are "ACTIVE")

livecd root # mke2fs -j /dev/vgmirror/opt    (OVERWRITES YOUR / PARTITION)
livecd root # mke2fs -j /dev/vgmirror/usr    (OVERWRITES YOUR / PARTITION)
livecd root # mke2fs -j /dev/vgmirror/var    (OVERWRITES YOUR / PARTITION)
livecd root # mke2fs -j /dev/vgmirror/home   (OVERWRITES YOUR / PARTITION)
livecd root # mke2fs /dev/vgmirror/ttmp      (OVERWRITES YOUR / PARTITION)
livecd root # mke2fs /dev/vgmirror/vartmp    (OVERWRITES YOUR / PARTITION)

livecd root # mkdir /mnt/gentoo/opt
livecd root # mkdir /mnt/gentoo/usr
livecd root # mkdir /mnt/gentoo/var
livecd root # mkdir /mnt/gentoo/home
livecd root # mount /dev/vgmirror/opt /mnt/gentoo/opt
livecd root # mount /dev/vgmirror/usr /mnt/gentoo/usr
livecd root # mount /dev/vgmirror/var /mnt/gentoo/var
livecd root # mount /dev/vgmirror/home /mnt/gentoo/home

livecd root # mkdir /mnt/gentoo/tmp
livecd root # mount /dev/vgmirror/tmp /mnt/gentoo/tmp
livecd root # chmod 1777 /mnt/gentoo/tmp
livecd root # mkdir /mnt/gentoo/var/tmp
livecd root # mount /dev/vgmirror/vartmp /mnt/gentoo/var/tmp
livecd root # chmod 1777 /mnt/gentoo/var/tmp
livecd root # mkdir /mnt/gentoo/proc
livecd root # mount -t proc none /mnt/gentoo/proc

livecd root # date
livecd root # cd /mnt/gentoo
livecd gentoo # tar -xvjpf /mnt/cdrom/stages/stage1-x86-20040218.tar.bz2
livecd gentoo # tar -xvjf /mnt/cdrom/snapshots/portage-20040223.tar.bz2 -C /mnt/gentoo/usr
livecd gentoo # mkdir /mnt/gentoo/usr/portage/distfiles
livecd gentoo # cp /mnt/cdrom/distfiles/* /mnt/gentoo/usr/portage/distfiles/

livecd gentoo # nano -w /mnt/gentoo/etc/make.conf
(repeat your make.conf from the initial install)

livecd gentoo # mirrorselect -a -s4 -o | grep -ve '^Netselect' >> /mnt/gentoo/etc/make.conf
livecd gentoo # cp -L /mnt/gentoo/etc/make.conf /mnt/gentoo/boot/make.conf-backupcopy
livecd gentoo # cp -L /etc/resolv.conf /mnt/gentoo/etc/resolv.conf
livecd gentoo # cp -L /etc/raidtab /mnt/gentoo/etc/raidtab
livecd gentoo # cp -L /etc/raidtab /mnt/gentoo/boot/raidtab-backupcopy
livecd gentoo # mkdir /mnt/gentoo/etc/lvm
livecd gentoo # cp -L /etc/lvm/lvm.conf /mnt/gentoo/etc/lvm/lvm.conf
livecd gentoo # cp -L /etc/lvm/lvm.conf /mnt/gentoo/boot/lvm.conf-backupcopy
livecd gentoo # chroot /mnt/gentoo /bin/bash
livecd / # env-update
livecd / # source /etc/profile
livecd / # emerge sync
livecd / # cd /usr/portage
livecd / # scripts/bootstrap.sh
```

If bootstrap runs correctly (and it should now that I re-formatted the /opt, /usr, /var, /home, /tmp, and /var/tmp volumes), I can pick back up with the [rest of my original install process](/blog/2004-06-15-gentoo-install-3-bootstrapping/)
