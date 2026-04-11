---
layout: post
title: 'Gentoo AMD64 install in Xen DomU'
date: '2006-09-30T12:11:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>(I'm assuming that you've already created a working Xen Dom0 domain and that you already have a Xen DomU kernel with which you can boot the Gentoo guest OS.  I'm skipping a lot of steps and doing what I think works based on previous Gentoo installs.)

Disk preparation: I'm installing the Gentoo guest OSs into LVM volumes managed by the Dom0 hypervisor domain.  Each guest OS gets a single partition for root that is exported to the guest OS as /dev/sda1.  In rare cases, I'm also providing a 2nd and 3rd LVM partition for the guest OS which are exported as /dev/sda2 and /dev/sda3.

<code>xena-adele thomas # lvcreate -L4G vgmirror -n domu-svn1root
  Logical volume "domu-svn1root" created
xena-adele thomas # mke2fs -j /dev/vgmirror/domu-svn1root
mke2fs 1.39 (29-May-2006)
Filesystem label=
OS type: Linux
Block size=4096 (log=2)
Fragment size=4096 (log=2)
524288 inodes, 1048576 blocks
52428 blocks (5.00%) reserved for the super user
First data block=0
Maximum filesystem blocks=1073741824
32 block groups
32768 blocks per group, 32768 fragments per group
16384 inodes per group
Superblock backups stored on blocks: 
        32768, 98304, 163840, 229376, 294912, 819200, 884736

Writing inode tables: done                            
Creating journal (32768 blocks): done
Writing superblocks and filesystem accounting information: done

This filesystem will be automatically checked every 20 mounts or
180 days, whichever comes first.  Use tune2fs -c or -i to override.
xena-adele thomas # mkdir /mnt/gentoo
mkdir: cannot create directory `/mnt/gentoo': File exists
xena-adele thomas # mount /dev/vgmirror/domu-svn1root /mnt/gentoo</code>

That takes care of the first 4 sections in the handbook.  In my case, the vgmirror group is an LVM volume group backed by software RAID (RAID1+hotspare) that the Dom0 hypervisor manages using mdadm.

A 4GB volume is probably about the minimum useful size for a Gentoo install, even a stripped down server-only install like this one.  It's safe enough as long as you have a monitoring job to watch disk space and/or are using an aggressive logrotate schedule.

I already had the portage and stage3 *.bz2 files downloaded from last month, so I don't need to download them.  Otherwise, you should grab the latest stage3 tarball and the latest portage snapshot from the public servers.  Both of these files should be placed into /mnt/gentoo.

Extraction of the 2 bz2 files is simple:

<code># cd /mnt/gentoo
# ls -l *.bz2
# tar xvjpf stage3-*.tar.bz2
# tar xvjf portage-*.tar.bz2 -C /mnt/gentoo/usr</code>

That puts us at step 5e in the Gentoo Handbook.  You can remove the *.bz2 files from /mnt/gentoo, but you'll probably want to back them up somewhere safe so you can reference them when building the next DomU.

Edit your make.conf file and configure the GENTOO_MIRROR=, SYNC=, and USE= lines.

Now you're ready to prepare for the chroot.

<code># cp -L /etc/resolv.conf /mnt/gentoo/etc/resolv.conf
# mount -t proc none /mnt/gentoo/proc
# mount -o bind /dev /mnt/gentoo/dev
# chroot /mnt/gentoo /bin/bash
# env-update
&gt;&gt; Regenerating /etc/ld.so.cache...
# source /etc/profile
# export PS1="(chroot) $PS1"
# emerge --sync</code>

That will go pretty quick if you have a local rsync mirror.

<code># ln -sf /usr/share/zoneinfo/EST5EDT /etc/localtime</code>

You can skip configuration of the kernel and installing grub/lilo since both of those tasks are handled by the hypervisor domain.  The only exception to this guideline is if you have kernel modules that need to be installed and loaded.  This should be a rare occurance in a Xen guest domain.

The fstab should be pretty simple.  Especially if you have the system configured with a single partition.  In my case, /etc/fstab looks like:

<code>/dev/sda1               /               ext3            noatime         0 1
proc                    /proc           proc            defaults        0 0
shm                     /dev/shm        tmpfs           nodev,nosuid,noexec     0 0</code>

Now for some final clean-up work:

(chroot) livecd linux # nano -w /etc/conf.d/hostname
(chroot) livecd linux # nano -w /etc/conf.d/net
config_eth7=( "192.168.142.100 netmask 255.255.255.0" )
routes_eth7=( "default gw 192.168.142.1" )
(chroot) livecd linux # cd /etc/init.d
(chroot) livecd init.d # ln -s net.lo net.eth0
(chroot) livecd init.d # rc-update add net.eth0 default
* net.eth0 added to runlevel default
* rc-update complete.
(chroot) livecd init.d # cat /etc/resolv.conf
(verify your DNS servers if you specified a static IP)
(chroot) livecd init.d # passwd
(set your root password to something you will remember)
New UNIX password:
Retype new UNIX password:
passwd: password updated successfully
# cd /
# emerge syslog-ng
# rc-update add syslog-ng default
(then update /etc/syslog-ng/syslog-ng.conf)
# emerge dcron
# rc-update add dcron default
# crontab /etc/crontab
# /usr/bin/ssh-keygen -t rsa -b 2048 -f /etc/ssh/ssh_host_rsa_key -N ""
(the key may take a a minute to generate)
# /usr/bin/ssh-keygen -t dsa -b 1024 -f /etc/ssh/ssh_host_dsa_key -N ""
# chmod 600 /etc/ssh/ssh_host_?sa_key
# chmod 644 /etc/ssh/ssh_host_?sa_key.pub
# rc-update add sshd default
# useradd -m -G users,wheel,audio -s /bin/bash username
(then put your user's public key file in their ~/.ssh folder)

Time to exit the chroot, unmount everything, and try to start the guest domain.  Odds are high that you will have trouble completely dismounting /mnt/gentoo (even if you umount /mnt/gentoo/proc and /mnt/gentoo/dev first).  So you'll likely have to restart the entire machine to get things clean.

(Which is why you'll only want to create the base system *once*.  Then copy it for new setups.)

I strongly suggest running GNU "screen" in the Dom0 hypervisor domain.  That will allow you to create a new screen to test out the install ([Ctrl-A][C] to create a new screen).  Then you can simply start the new guest domain with:

<code># xm create -c mydomainconfigfile</code>

You can then shutdown (and exit) the domain by logging in as root and typing "shutdown -h now".  Once the guest domain seems to be working, fire it up without the "-c" option to get it running in the background.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2006.shtml">2006</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Gentoo.shtml">Gentoo</a>
		<div class="Byline">
			posted by Thomas at 
			[12:11](http://www.tgharold.com/techblog/2006/09/gentoo-amd64-install-in-xen-domu.shtml)

		</div>