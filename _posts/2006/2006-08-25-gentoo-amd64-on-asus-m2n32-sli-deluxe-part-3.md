---
layout: post
title: 'Gentoo AMD64 on Asus M2N32-SLI Deluxe (part 3)'
date: '2006-08-25T21:20:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


It's now time to start refering to the [Gentoo Installation Handbook](http://www.gentoo.org/doc/en/handbook/index.xml) for AMD64.  While I'm pretty sure that my install method works, it's worthwhile verifying against the handbook.  Plus I'm using a minimal CD to do the installation, so things will be slightly different then normal.

(I use my own recipe for the initial configuration due to the mix of Software RAID + LVM2.  It has served me well over the past few years and works well.)

This page starts with section 5 in the Gentoo handbook (Installing the Gentoo Installation Files).

<code>livecd / # date
Fri Aug 25 21:23:52 UTC 2006
livecd / # cd /mnt/gentoo
livecd gentoo # links http://www.gentoo.org/main/en/mirrors.xml</code>

Follow the directions on the Gentoo handbook page to download the correct stage3 tarball for your install.  The steps are roughly thus:

<ol>

<li>Pick an HTTP mirror from the list (arrow up/down then press [Enter] on the link)

</li>
<li>Go into the "releases/" folder

</li>
<li>Go into the "amd64/" folder (note: Not all mirrors carry the AMD64 folder, you may need to pick another mirror)

</li>
<li>Go into the "current/" folder

</li>
<li>Go into the "stages/" folder

</li>
<li>Find the stage3-amd64-NNNN.N-tar.bz2 tarball, highlight it and click [D] to download

</li>
<li>Press [Q] to quit out of links

</li>
</ol>

Now you should have the tarball in /mnt/gentoo:

<code>livecd gentoo # ls -l
total 105797
drwxr-xr-x  3 root root      4096 Aug 25 21:11 backup
drwxr-xr-x  3 root root      1024 Aug 25 20:46 boot
drwxr-xr-x  3 root root      4096 Aug 25 20:59 home
drwx------  2 root root     16384 Aug 25 20:47 lost+found
-rw-r--r--  1 root root 108186115 Aug 25 22:05 stage3-amd64-2006.0.tar.bz2
drwxrwxrwt  3 root root      4096 Aug 25 20:59 tmp
drwxr-xr-x  3 root root      4096 Aug 25 21:00 usr
drwxr-xr-x  5 root root      4096 Aug 25 21:10 var
livecd gentoo #</code>

Extract the tarball:

<code>livecd gentoo # tar xvjpf stage3-*.tar.bz2</code>

You'll follow similar steps for the portage tarball.  In fact, we probably should've downloaded it at the same time to /mnt/gentoo.

<code>livecd gentoo # tar xvjf /mnt/gentoo/portage-20060123.tar.bz2 -C /mnt/gentoo/usr</code>

Setup your make flags.  Since I have an X2 CPU, I'm using "-j3" for MAKEOPTS.

<code>livecd gentoo # vi /mnt/gentoo/etc/make.conf
# These settings were set by the catalyst build script that automatically built this stage
# Please consult /etc/make.conf.example for a more detailed example
CFLAGS="-march=k8 -O2 -pipe"
CHOST="x86_64-pc-linux-gnu"
CXXFLAGS="${CFLAGS}"
MAKEOPTS="-j3"</code>

Now we start in on [Section 6 (Installing the Gentoo Base System)](http://www.gentoo.org/doc/en/handbook/handbook-amd64.xml?part=1&amp;chap=6).  Time to pick mirrors and other things.

<code>livecd gentoo # mirrorselect -i -o &gt;&gt; /mnt/gentoo/etc/make.conf
livecd gentoo # mirrorselect -i -r -o &gt;&gt; /mnt/gentoo/etc/make.conf
livecd gentoo # cat /mnt/gentoo/etc/make.conf
# These settings were set by the catalyst build script that automatically built this stage
# Please consult /etc/make.conf.example for a more detailed example
CFLAGS="-march=k8 -O2 -pipe"
CHOST="x86_64-pc-linux-gnu"
CXXFLAGS="${CFLAGS}"
MAKEOPTS="-j3"

GENTOO_MIRRORS="http://gentoo.arcticnetwork.ca/ http://www.gtlib.gatech.edu/pub/gentoo http://gentoo.chem.wisc.edu/gentoo/ http://gentoo.mirrors.pair.com/ "

SYNC="rsync://rsync.namerica.gentoo.org/gentoo-portage"
livecd gentoo #</code>

Copy the resolv.conf file and mount /proc and /dev:

<code>livecd gentoo # cp -L /etc/resolv.conf /mnt/gentoo/etc/resolv.conf
livecd gentoo # mount -t proc none /mnt/gentoo/proc
livecd gentoo # mount -o bind /dev /mnt/gentoo/dev</code>

We're ready to chroot and start the build.

<code>livecd gentoo # chroot /mnt/gentoo /bin/bash
livecd / # env-update
&gt;&gt;&gt; Regenerating /etc/ld.so.cache...
livecd / # source /etc/profile
livecd / # export PS1="(chroot) $PS1"
(chroot) livecd / #</code>

Read the next section carefully!  I use an extremely limited USE flag (that turns off all multimedia and graphical support).

<code>(chroot) livecd / # emerge --sync

(chroot) livecd / # ls -FGg /etc/make.profile
lrwxrwxrwx  1 50 Aug 25 22:10 /etc/make.profile -&gt; ../usr/portage/profiles/default-linux/amd64/2006.0/
(chroot) livecd / # nano -w /etc/make.conf
USE="-alsa -apm -arts -bitmap-fonts -gnome -gtk -gtk2 -kde -mad -mikmod -motif -opengl -oss -qt -quicktime -sdl -truetype -truetype-fonts -type1-fonts -X -xmms -xv"
(chroot) livecd / # ls /usr/share/zoneinfo
(chroot) livecd / # ln -sf /usr/share/zoneinfo/EST5EDT /etc/localtime
(chroot) livecd / # date
(chroot) livecd / # zdump GMT
(chroot) livecd / # zdump EST5EDT</code>

Read section 7 carefully.  I'm using the default "gentoo-sources" kernel.

<code>(chroot) livecd / # USE="-doc symlink" emerge gentoo-sources</code>

I'll cover configuration of the kernel in the next post.
