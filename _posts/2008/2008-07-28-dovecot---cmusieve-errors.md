---
layout: post
title: 'Dovecot - CMUSieve Errors'
date: '2008-07-28T11:17:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


After upgrading our CentOS 5 box to the latest revisions this week (including Dovecot 1.1), we're seeing the following error message in the log files.  Sieve was working fine with Dovecot 1.0.

    # cat /var/vmail/dovecot-deliver.log

    deliver(ruth@example.com): Jul 28 11:11:44 Error: dlopen(/usr/lib64/dovecot/lda/lib90_cmusieve_plugin.so) failed: /usr/lib64/dovecot/lda/lib90_cmusieve_plugin.so: undefined symbol: message_decoder_init
    deliver(ruth@example.com): Jul 28 11:11:44 Fatal: Couldn't load required plugins

    # ls -l /usr/libexec/dovecot/sievec
    -rwxr-xr-x 1 root root 165152 Jun 11 03:21 /usr/libexec/dovecot/sievec

    # yum list | grep "dovecot"
    dovecot.x86_64                           1:1.1.1-2_76.el5       installed       
    dovecot-sieve.x86_64                     1.1.5-8.el5            installed       
    dovecot.x86_64                           1:1.1.2-2_77.el5       atrpms          
    dovecot-devel.x86_64                     1:1.1.2-2_77.el5       atrpms 

Not sure yet what went wrong during the upgrade.

...

Update: The problem was that we had made a copy of Dovecot's "deliver" executable to make it setuid to work with virtual user local delivery.  After the update, we forgot to update this copy of the exectuable.

Once we updated the setuid copy of "deliver", things worked fine.
