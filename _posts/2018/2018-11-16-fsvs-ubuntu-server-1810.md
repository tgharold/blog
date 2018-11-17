---
layout: post
title: 'FSVS on Ubuntu Server 18.04.1'
date: '2018-11-16T16:34:00.000-05:00'
author: Thomas Harold
category:
- SysAdmin
tags:
- FSVS
- Linux

---

Under CentOS Server, there were some extra things that had to be installed at the start to use [FSVS](http://fsvs.tigris.org/).  This is the first time that I'm installing under Ubuntu Server.

FSVS is a way of version controlling your entire server (or parts of it, like `/etc`) into Subversion (SVN).  For servers that you are not managing with puppet / chef / ansible / etc., it provides a way to track configuration changes over time.  Even with configuration systems like puppet/chef, it can still be useful for tracking configuration changes over time.  Since SVN is a very efficient over-the-wire protocol for binary files, it can also be used to backup those in addition to text-based configuration files.  It gets more efficient when multiple servers are all stored in the same SVN repository as you'll get deduplication across the entire repo.

---

I'm starting with a brand new install of Ubuntu Server 18.04.1 using the `ubuntu-18.04.1-live-server-amd64.iso` file.  This is being installed on a Synology NAS (plus series) with 1GB RAM and 1TB of drive space allocated for the VM.

    sudo add-apt-repository universe
    sudo apt update

The default install only includes bionic, bionic-security and bionic-dates PPAs.  To get some other packages, you'll need to install the "universe" PPA.  Once you have the universe installed, the following should work.

    sudo apt install fsvs

That package will also require some other things to be installed like subversion and a few other things.

(This is so much easier than what I had to jump through on CentOS 5 and 6.  My thanks go out to the person that added the fsvs package to the Ubuntu package repository.)


