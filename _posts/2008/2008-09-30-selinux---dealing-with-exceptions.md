---
layout: post
title: 'SELinux - dealing with exceptions'
date: '2008-09-30T11:38:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


So we're seeing errors in our /var/log/messages like:

    Sep 28 03:52:51 fvs-pri setroubleshoot: SELinux is preventing freshclam (freshclam_t) "read" to ./main.cld (var_t). For complete SEL
    inux messages. run sealert -l 10ce7bfb-6c44-473e-94a1-4691c04d2bef
    Sep 28 03:52:51 fvs-pri setroubleshoot: SELinux is preventing freshclam (freshclam_t) "write" to ./clamav (var_t). For complete SELi
    nux messages. run sealert -l 276efeb4-6990-497f-bcf0-6df0327c6f52

It's fairly easy to write exceptions, using audit2allow.

For example:

    # cd /usr/share/selinux/devel/

    # egrep "(clam)" /var/log/audit/audit.log /var/log/audit/audit.log.1 | audit2allow -M clam20081230

    # /usr/sbin/semodule -i clam20080930.pp

Note: This is the very quick and dirty way of dealing with exceptions - it really doesn't fix the underlying issue.
