---
layout: post
title: 'Squid, SELinux and using a separate volume for the cache_dir'
date: '2007-05-27T22:49:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


This was a slightly tricky one.  I'm running CentOS5 with SELinux and I was trying to setup Squid to put its cache_dir on a LVM volume (to keep it from using up space on the root partition).

    # /etc/init.d/squid stop
    # cd /var/spool
    # lvcreate -L64G -nvar-spool-squid vg
    # mke2fs -j /dev/vg/var-spool-squid
    # mkdir /mnt/squid ; mount /dev/vg/var-spool-squid squid
    # cp -a /var/spool/squid/* /mnt/squid/
    # cd /var/spool/squid
    # rm -rf *
    # cd /var/spool
    # mount /dev/vg/var-spools-squid squid
    # /etc/init.d/squid start

    Starting squid: /etc/init.d/squid: line 53:  9440 Aborted                 $SQUID $SQUID_OPTS >>/var/log/squid/squid.out 2>&1
                                                            [FAILED]

    # tail /var/log/messages

    May 27 21:50:48 fw1-hosho setroubleshoot:      SELinux is preventing /usr/sbin/named (named_t) "write" access to named (named_conf_t).      For complete SELinux messages. run sealert -l 663ea169-d194-4c49-a5bb-a6a4bb707990
    May 27 22:39:26 fw1-hosho squid: cache_dir /var/spool/squid: (13) Permission denied

<code># /usr/bin/sealert -l 626e75b4-32aa-4a61-88f7-f36a68fecd35
Summary
    SELinux is preventing access to files with the label, file_t.

Detailed Description
    SELinux permission checks on files labeled file_t are being denied.  file_t
    is the context the SELinux kernel gives to files that do not have a label.
    This indicates a serious labeling problem. No files on an SELinux box should
    ever be labeled file_t. If you have just added a new disk drive to the
    system you can relabel it using the restorecon command.  Otherwise you
    should relabel the entire files system.

Allowing Access
    You can execute the following command as root to relabel your computer
    system: "touch /.autorelabel; reboot"

Additional Information        

Source Context                user_u:system_r:squid_t
Target Context                user_u:object_r:file_t
Target Objects                /var/spool/squid/00 [ dir ]
Affected RPM Packages         squid-2.6.STABLE6-4.el5 [application]
Policy RPM                    selinux-policy-2.4.6-30.el5
Selinux Enabled               True
Policy Type                   targeted
MLS Enabled                   True
Enforcing Mode                Enforcing
Plugin Name                   plugins.file
Host Name                     fw1-hosho.intra.example.com.
Platform                      Linux fw1-hosho.intra.example.com. 2.6.18-8.1.4.el5
                              #1 SMP Thu May 17 03:16:52 EDT 2007 x86_64 x86_64
Alert Count                   10
Line Numbers                  

Raw Audit Messages            

avc: denied { getattr } for comm="squid" dev=dm-0 egid=23 euid=23
exe="/usr/sbin/squid" exit=-13 fsgid=23 fsuid=23 gid=23 items=0 name="00"
path="/var/spool/squid/00" pid=9584 scontext=user_u:system_r:squid_t:s0 sgid=23
subj=user_u:system_r:squid_t:s0 suid=0 tclass=dir
tcontext=user_u:object_r:file_t:s0 tty=(none) uid=23</code>

...

So, the problem is that SELinux had not yet been told to look at the newly created volume (a LVM volume mounted on /var/spool/squid).  Fixing this was rather simple once you know about the restorecon command.

    # cd /var/spool/squid
    # /usr/sbin/squid -z
    # /sbin/restorecon -R *
    # /etc/init.d/squid start
