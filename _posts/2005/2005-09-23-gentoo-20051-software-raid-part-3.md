---
layout: post
title: 'Gentoo 2005.1 Software RAID (part 3)'
date: '2005-09-23T16:18:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>Picking up with part 7c after [compiling the kernel](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=7).  Now you need to install your kernel into the boot partition. Change the "2.6.12-Sep2005" portion of the filenames to whatever you want.

<code># cp arch/i386/boot/bzImage /boot/kernel-2.6.12-Sep2005
# cp System.map /boot/System.map-2.6.12-Sep2005
# cp .config /boot/config-2.6.12-Sep2005</code>

If you are using LVM2, you will need to add a line at the end of the autoload file to automatically load the LMV2 module.  Note that you may also need to add a line for DHCP support (not 100% sure about that).  Since I'm using these boxes for servers with static IPs I don't concern myself with it.

<code># echo 'dm-mod' &gt;&gt; /etc/modules.autoload.d/kernel-2.6
# cat /etc/modules.autoload.d/kernel-2.6</code>

Time to configure the "/etc/fstab" file.  There are pages full of documentation on what goes in this file and the handbook covers some of it.  For my VIA EPIA box with only 3 partitions, my fstab file is going to be rather simple.

<code># nano -w /etc/fstab

/dev/md0 /boot ext2 noauto,noatime 1 2
/dev/md2 / ext3 noatime 0 1
/dev/md1 none swap sw 0 0
/dev/cdroms/cdrom0 /mnt/cdrom auto noauto,ro,user 0 0

#/dev/fd0 /mnt/floppy auto noauto 0 0

proc /proc proc defaults 0 0

shm /dev/shm tmpfs nodev,nosuid,noexec 0 0</code>

For my Celeron box which is using LVM2 partitions, it's more complex.

<code># nano -w /etc/fstab

/dev/md0 /boot ext2 noauto,noatime 1 2
/dev/md2 / ext3 noatime 0 1
/dev/md1 none swap sw 0 0
/dev/cdroms/cdrom0 /mnt/cdrom auto noauto,ro,user 0 0

#/dev/fd0 /mnt/floppy auto noauto 0 0

/dev/vgmirror/opt /opt ext3 noatime 0 3
/dev/vgmirror/usr /usr ext3 noatime 0 3
/dev/vgmirror/var /var ext3 noatime 0 3
/dev/vgmirror/home /home ext3 noatime 0 3
/dev/vgmirror/tmp /tmp ext2 noatime 0 3
/dev/vgmirror/vartmp /var/tmp ext2 noatime 0 3 

proc /proc proc defaults 0 0

shm /dev/shm tmpfs nodev,nosuid,noexec 0 0</code>

Now, some misc stuff (see [networking configuration](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=1&amp;chap=8#doc_chap2) for information on setting up DHCP or static IPs):

<code># nano -w /etc/conf.d/hostname
# nano -w /etc/conf.d/domainname
# rc-update add domainname default
# nano -w /etc/conf.d/net
(either leave empty for DHCP or configure your IP and gateway)
# rc-update add net.eth0 default
# cat /etc/resolv.conf
(verify your DNS servers if you specified a static IP)
# nano -w /etc/conf.d/clock
(change CLOCK="UTC" to CLOCK="local")
# passwd
(set your root password to something you will remember)

# useradd -m -G users,wheel,audio -s /bin/bash john
# passwd john
(add a user called 'john' and set a password)</code>

And a few other misc options (system logger, job scheduling):

<code># emerge syslog-ng
# rc-update add syslog-ng default
# emerge dcron
# rc-update add dcron default
# crontab /etc/crontab</code>

I also like to install the "sshd" service at this point so that I can ssh into the box after the initial reboot.  (These notes are based on a very old posting that I made about [installing sshd on Gentoo Linux](/techblog/2004_04_01_archive.shtml).)  Alternately, you can do these commands after booting the box for the first time by logging in as root at the console.

<code># /usr/bin/ssh-keygen -t dsa -b 2048 -f /etc/ssh/ssh_host_dsa_key -N ""
(the key may take a few minutes to generate)
# chmod 600 /etc/ssh/ssh_host_dsa_key
# chmod 644 /etc/ssh/ssh_host_dsa_key.pub
# rc-update add sshd default</code>

Now it's time to install and configure "grub" (the boot loader).  Note that where we are saying "/dev/hdc", you will need to change to match the name of your secondary mirror drive.

<code># emerge grub</code>

(Now, at this point, I got an error at the end of the emerge because I had failed to mount my /proc file system before entering the chroot environment.  The fix was easy, requiring me to exit the chroot environment, mount the /proc filesystem and then re-enter the chroot environment.)

<code># ls -l /boot
# nano -w /boot/grub/grub.conf</code>

Contents of my grub.conf file:

<code># Which listing to boot as default. 0 is the first, 1 the second etc.
default 0
timeout 30

# Sep 2005 installation (software RAID, no LVM2)
title=Gentoo Linux 2.6.12 (Sep 22 2005)  
root (hd0,0)
kernel /kernel-2.6.12-Sep2005 root=/dev/md2</code>

Now I fire up grub and install it onto the MBR of both disks.

<code># grub --no-floppy
grub&gt; find /grub/stage1
(hd0,0)
(hd1,0)
grub&gt; root (hd0,0)
grub&gt; setup (hd0)
grub&gt; device (hd0) /dev/hdc
grub&gt; root (hd0,0)
grub&gt; setup (hd0)
grub&gt; quit</code>

Time for the first reboot.  Now you need to unmount everything that you can (including LVM) prior to reboot.  Since I'm not using LVM2, this is rather simple.

<code>livecd gentoo # exit
livecd / # cd /
livecd / # cat /proc/mounts
(gives you a list of what is mounted)
livecd / # umount /mnt/gentoo/boot
livecd / # umount /mnt/gentoo/proc
livecd / # umount /mnt/gentoo
livecd / # reboot</code>

Pull the CD-ROM at this point, otherwise the LiveCD will probably boot.  Then cross your fingers and watch the console for errors.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2005.shtml">2005</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Gentoo.shtml">Gentoo</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/SoftwareRAID.shtml">SoftwareRAID</a>
		<div class="Byline">
			posted by Thomas at 
			[16:18](http://www.tgharold.com/techblog/2005/09/gentoo-20051-software-raid-part-3.shtml)

		</div>