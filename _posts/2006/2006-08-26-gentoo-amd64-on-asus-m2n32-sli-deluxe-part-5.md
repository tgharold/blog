---
layout: post
title: 'Gentoo AMD64 on Asus M2N32-SLI Deluxe (part 5)'
date: '2006-08-26T06:45:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Now there were a few minor things that I had to fix after the reboot before I could SSH back in.  I hadn't pointed my swap line in /etc/fstab at the proper mdadm RAID volume, the 3c509 moved from eth7 to eth4 after the reboot, I had to use the "noapic" kernel option and I'm still getting the IRQ7 warning.

But the system is mostly in a workable state at this point.  So it's time to start installing administration packages and cleaning up the install.  I'll save the existing kernel as my "base" configuration in case I screw things up.

The first package that I always install is <b>emerge screen</b>.  That provides me with multiple virtual terminals in my single SSH connection.  Even better, if I disconnect accidentally, I don't lose my state and programs that were running within screen sessions will continue running.  After reconnecting, I can type "screen -x" and reconnect to my old sessions.

Other key packages to install, even on a basic system like this one, are:

app-benchmarks/bonnie
app-editors/vim
app-misc/colordiff
app-portage/gentoolkit
app-text/tree
dev-util/subversion
net-analyzer/iptraf
net-analyzer/nettop
net-analyzer/nload
net-misc/ntp
sys-apps/dstat
sys-apps/eject
sys-apps/smartmontools
sys-process/atop

<code>san1-azure ~ # emerge -pv bonnie vim colordiff gentoolkit tree subversion iptraf nettop nload ntp dstat eject smartmontools atop

These are the packages that I would merge, in order:

Calculating dependencies ...done!
[ebuild  N    ] app-benchmarks/bonnie-2.0.6  6 kB 
[ebuild  N    ] dev-util/ctags-5.5.4-r2  254 kB 
[ebuild  N    ] app-editors/vim-core-7.0.17  -acl -bash-completion -livecd +nls 5,997 kB 
[ebuild  N    ] app-editors/vim-7.0.17  -acl -bash-completion -cscope +gpm -minimal (-mzscheme) +nls +perl +python -ruby -vim-pager -vim-with-x 0 kB 
[ebuild  N    ] app-vim/gentoo-syntax-20051221  -ignore-glep31 18 kB 
[ebuild  N    ] app-misc/colordiff-1.0.5-r2  13 kB 
[ebuild  N    ] app-portage/gentoolkit-0.2.2  84 kB 
[ebuild  N    ] app-text/tree-1.5.0  -bash-completion 25 kB 
[ebuild  N    ] dev-libs/apr-0.9.12  +ipv6 -urandom 1,024 kB 
[ebuild  N    ] dev-libs/apr-util-0.9.12  +berkdb -gdbm -ldap 578 kB 
[ebuild  N    ] net-misc/neon-0.26.1  +expat -gnutls +nls -socks5 +ssl -static +zlib 763 kB 
[ebuild  N    ] dev-util/subversion-1.3.2-r1  -apache2 -bash-completion +berkdb -emacs -java +nls -nowebdav +perl +python -ruby +zlib 6,674 kB 
[ebuild  N    ] net-analyzer/iptraf-2.7.0-r1  +ipv6 410 kB 
[ebuild  N    ] net-libs/libpcap-0.9.4  +ipv6 415 kB 
[ebuild  N    ] sys-libs/slang-1.4.9-r2  -cjk -unicode 628 kB 
[ebuild  N    ] net-analyzer/nettop-0.2.3  22 kB 
[ebuild  N    ] net-analyzer/nload-0.6.0  118 kB 
[ebuild  N    ] net-misc/ntp-4.2.0.20040617-r3  -caps -debug +ipv6 -logrotate -openntpd -parse-clocks (-selinux) +ssl 2,403 kB 
[ebuild  N    ] sys-apps/dstat-0.6.0-r1  35 kB 
[ebuild  N    ] sys-apps/eject-2.1.0-r1  +nls 65 kB 
[ebuild  N    ] mail-client/mailx-support-20030215  8 kB 
[ebuild  N    ] net-libs/liblockfile-1.06-r1  31 kB 
[ebuild  N    ] mail-client/mailx-8.1.2.20040524-r1  126 kB 
[ebuild  N    ] sys-apps/smartmontools-5.36  -static 528 kB 
[ebuild  N    ] sys-process/acct-6.3.5-r1  300 kB 
[ebuild  N    ] sys-process/atop-1.15  102 kB 

Total size of downloads: 20,638 kB
san1-azure ~ # </code>

That should take all of about 0.1 seconds on this Athlon64 X2.  (I joke, slightly... the box is quite snappy even with only 7200rpm SATA drives.)

Now I'm going to [configure SubVersion](/techblog/2006/06/subversion-for-linux-administrators.shtml).  There have been some changes in that process that I learned through trial and error.  Folders that I would recommend placing under version control are:

/boot (most files)
/etc (most files, especially configuration files)
/usr/local/sbin (local sysadmin scripts that you create)
/usr/src (the .config file, make sure you add the actual directory with "svn add -N" before adding the "linux" symbolic link)

I know there are other folders to add, but I typically add them on the fly as I start customizing the system.
