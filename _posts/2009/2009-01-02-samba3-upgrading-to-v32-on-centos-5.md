---
layout: post
title: 'Samba3: Upgrading to v3.2 on CentOS 5'
date: '2009-01-02T08:22:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


CentOS 5 currently only has Samba 3.0.28 in their BASE repository.  The DAG/RPMForge projects don't have updated Samba3 RPMs either (although I do see an OpenPkg RPM).  So the question that I've been dealing with for the past few weeks is "where do I get newer Samba RPMs"?

Ideally, I would get these RPMs from a repository, so that I could be notified via "yum check-update" for when there are security / feature updates.  While I don't mind the occasional source package in .tar.gz or .tar.bz2 format, they rapidly become a maintenance nightmare.  Especially for security-sensitive packages like Samba which tend to be attack targets.

What I've found that looks promising is:

[http://ftp.sernet.de/pub/samba/recent/centos/5/](http://ftp.sernet.de/pub/samba/recent/centos/5/)

Which has a .repo file and looks like it might be usable as a repository for yum.  (See "[Get the latest Samba from Sernet](https://secure.linux.ncsu.edu/moin/SambaRepos)" for confirmation of this.)

    # cd /etc/yum.repos.d/
    # wget http://ftp.sernet.de/pub/samba/recent/centos/5/sernet-samba.repo

Now, the major change is that the RedHat/CentOS packages are named "samba.x86_64" while the sernet.de packages are named "samba3.x86_64".  Also, the sernet.de folks don't sign their packages, so you will need to add "gpgcheck=0" to the end of the .repo file.

(At least, I don't think they do...)

Note: As always, before doing a major upgrade like this, <b>make backups</b>.  At a minimum, make sure you have good backups of your Samba configuration files.  We use FSVS with a SVN backend for all of our configuration files, which makes an excellent change tracking tool for Linux servers.

    # yum remove samba.x86_64
    # yum install samba3.x86_64
    # service smb start

With luck, you should now be up and running with v3.2 of Samba.  You can verify this by looking at the latest log file in the /var/log/samba/ directory.
