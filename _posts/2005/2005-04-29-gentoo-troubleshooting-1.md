---
layout: post
title: 'Gentoo: Troubleshooting 1'
date: '2005-04-29T11:44:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


So, I've got a system that isn't booting yet.  The boot error is:

```
* Mounting proc at /proc [ ok ]
* Mounting sysfs at /sys [ !! ]
can't create lock file /etc/mtab~944: Read-only file system (use -n flag to override)
```

First, I have to go back to the boot CD and get up and running:

```
livecd root # passwd
livecd root # /etc/init.d/sshd start
livecd root # ifconfig
(at this point, I switch over to using SecureCRT on the other system)
livecd root # modprobe md
livecd root # modprobe raid1
livecd root # for i in 0 1 2 3; do mknod /dev/md$i b 9 $i; done
livecd root # mdadm --assemble /dev/md0 /dev/hda1 /dev/hdc1
livecd root # mdadm --assemble /dev/md1 /dev/hda2 /dev/hdc2
livecd root # mdadm --assemble /dev/md2 /dev/hda3 /dev/hdc3
livecd root # mdadm --assemble /dev/md3 /dev/hda4 /dev/hdc4
```

That gets the raid arrays up and running.

```
livecd root # swapon /dev/md2
livecd root # mount /dev/md1 /mnt/gentoo
livecd root # mount /dev/md0 /mnt/gentoo/boot
livecd root # modprobe dm-mod
livecd root # mkdir /etc/lvm
livecd root # echo 'devices { filter=["r/cdrom/"] }' >/etc/lvm/lvm.conf
livecd / # lvscan
livecd / # lvchange -ay vgmirror
```

Which gets the LVM2 up and running (and the logical volumes set to active).

```
# mount /dev/vgmirror/opt /mnt/gentoo/opt
# mount /dev/vgmirror/usr /mnt/gentoo/usr
# mount /dev/vgmirror/var /mnt/gentoo/var
# mount /dev/vgmirror/home /mnt/gentoo/home
# mount /dev/vgmirror/tmp /mnt/gentoo/tmp
# chmod 1777 /mnt/gentoo/tmp
# mount /dev/vgmirror/vartmp /mnt/gentoo/var/tmp
# chmod 1777 /mnt/gentoo/var/tmp
# mount -t proc none /mnt/gentoo/proc
```

Should be ready to chroot into the hard disk.

```
# chroot /mnt/gentoo /bin/bash ; env-update
```

Gonna redo my kernel configuration (see [Gentoo 2004.3 on Gigabyte GA-6VA7+ (part 4)](/2005-04-20-gentoo-20043-on-gigabyte-ga-6va7-part-4/)) because I suspect that something needed to be loaded in differently.

```
# cd /usr/src/linux
# make menuconfig
```

Going to switch the LVM2 from loading as a "module" and change it to being "built-in".  Could be an error on the Gentoo LVM2 page according to a [note I see in the gentoo wiki](http://gentoo-wiki.com/HOWTO_Gentoo_Install_on_Software_RAID_mirror_and_LVM2_on_top_of_RAID).

```
# make && make modules_install
# cp arch/i386/boot/bzImage /boot/kernel-2.6.11-gentoo-Apr20
# cp System.map /boot/System.map-2.6.11-gentoo-Apr20
# cp .config /boot/config-2.6.11-gentoo-Apr20
# nano -w /etc/modules.autoload.d/kernel-2.6
(remove dm-mod from being auto-loaded)
livecd linux # exit
livecd / # cd /
livecd / # cat /proc/mounts

(unmount all of your mounted partitions, including the LVM mounts)

livecd / # umount ... (insert list of mounted file systems)

livecd / # vgchange -an vgmirror
livecd / # reboot

(remove the gentoo boot CD)
```

Now to see if it works.  No luck.  Redoing the above, but going to re-do my LVM2, but changing to be 'static' per the wiki.

```
# echo 'sys-fs/lvm2 static' >> /etc/portage/package.use
# emerge lvm2
```

No joy here either.  Time to go do some more searching.

Attempt #3 (#4?), editing the grub.conf file and adding "udev" to the end of the "kernel" line.  Nothing complex, just tack " udev" onto the end of the kernel line using nano.

No joy again.

Attempt #4 - added an initrd line to the grub.conf file.  Doubtful that this will fix the issue.

Nope.

Attempt #5 - using [this thread over at the gentoo forums](http://forums.gentoo.org/viewtopic-t-318344-highlight-mtab.html), I added some more information to my kernel line in the grub.conf file.

Nope.
