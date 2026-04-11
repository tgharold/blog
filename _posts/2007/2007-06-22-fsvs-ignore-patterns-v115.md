---
layout: post
title: 'FSVS ignore patterns (v1.1.5)'
date: '2007-06-22T10:47:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Here's a list of the current ignore patterns that I use on my CentOS5 box.

# fsvs ignore dump
./backup
./dev
./home
./lost+found
./media
./mnt
./proc/**
./root/.mozilla/firefox/**/Cache/**
./root/.thumbnails/**
./selinux
./sys
./tmp
./var/cache/**
./var/lock/**
./var/log/**
./var/named/chroot/proc
./var/run/**
./var/spool/**
./var/tmp/**

There are a few commands that I use to keep my sanity:

# fsvs dump ignore | sort &gt; /root/fsvs-ignore.txt
# sort /root/fsvs-ignore.txt | fsvs ignore load

I find that keeping my ignore files in a .txt file under /root makes it easier to work with them.  I'm able to edit the text file, load the ignore patterns into FSVS and see whether it does what it should.  If it's wrong, I re-edit the text file and load them back into FSVS.

...

After mucking with a new box for a week, here's the set of ignore filters that I'm using on another CentOS5 box.  On this particular box, I'm only versioning configuration data (/etc, /var/named).

[root@fw1-shimo /]# fsvs ignore dump | sort
./backup/
./bin/
./dev/
./home/
./lib/
./lib64/
./lost+found
./media/
./mnt/
./proc/
./root/
./sbin/
./selinux/
./srv/
./sys/
./tmp/
./usr/bin/
./usr/include/
./usr/kerberos/
./usr/lib/
./usr/lib64
./usr/libexec/
./usr/local/bin/
./usr/local/include/
./usr/local/lib/
./usr/local/libexec/
./usr/local/share/
./usr/local/src/
./usr/sbin/
./usr/share/
./usr/share/applications/
./usr/share/backgrounds/
./usr/share/dict/
./usr/share/doc/
./usr/share/i18n/
./usr/share/info/
./usr/share/locale/
./usr/share/man/
./usr/share/pixmaps/
./usr/share/X11/
./usr/share/zoneinfo/
./usr/src/
./usr/tmp/
./usr/X11R6/
./var/cache/
./var/lib/
./var/lock/
./var/log/
./var/named/chroot/dev/
./var/named/chroot/proc/
./var/named/chroot/var/run/
./var/run/
./var/spool/
./var/svn/
./var/tmp/
./var/www/
[root@fw1-shimo /]#
