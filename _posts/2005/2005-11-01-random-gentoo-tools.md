---
layout: post
title: 'Random Gentoo Tools'
date: '2005-11-01T21:05:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Things that might be useful to a system administrator and which don't come pre-installed on Gentoo.

curl
denyhosts
fail2ban
linkx
lynx
nload
screen

In order to install "denyhosts", you'll probably have to muck with application specific keywords.  See [USE flags (gentoo.org)](http://www.gentoo.org/doc/en/handbook/handbook-x86.xml?part=2&chap=2) or [FAQ USE Flags (Gentoo Linux Wiki)](http://gentoo-wiki.com/FAQ_USE_Flags).  Look for information on editing the "/etc/portage/package.keywords" file.  The current version of denyhosts is tagged with "~x86" (indicating that it compiles, but has not been verified?).
