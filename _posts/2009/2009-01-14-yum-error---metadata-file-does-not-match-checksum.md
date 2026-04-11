---
layout: post
title: 'Yum Error - Metadata file does not match checksum'
date: '2009-01-14T10:19:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Ran into this issue today when the pgsql folks updated their repository.  All of our CentOS 5 machines are behind a transparent HTTP proxy cache server (squid).

```
filelists.sqlite.bz2      100% |=========================| 157 kB    00:00     
http://yum.pgsqlrpms.org/8.3/redhat/rhel-5-x86_64/repodata/filelists.sqlite.bz2: [Errno -1] Metadata file does not match checksum
Trying other mirror.
Error: failure: repodata/filelists.sqlite.bz2 from pgdg83: [Errno 256] No more mirrors to try.
```

It doesn't really matter what the package name is, the primary issue is the "[Errno -1] Metadata file does not match checksum" error message.

<b>Solution:</b>

1) Edit /etc/yum.conf and add the following line

http_caching=packages

2) Run "yum cleanup metadata"

3) Retry the yum install

<b>References:</b>

[FedoraForum.org > Fedora Support  > Installation Help > yum "Metadata file does not match checksum" problem](http://forums.fedoraforum.org/showthread.php?t=67591&amp;page=2)
