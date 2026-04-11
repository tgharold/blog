---
layout: post
title: 'fsvs urls or fsvs initialize results in No such file or directory (2) error'
date: '2008-07-14T14:50:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


So I was setting up FSVS 1.1.16 on a new CentOS 5.1 box this week (one of the first things that I do as soon as possible before configuration starts).  And I encountered the following error:

# fsvs -v urls svn+ssh://svn.example.com/sys-machinename

An error occurred at 14:40:31.865: No such file or directory (2)
  in url__output_list
  in url__work
  in main: action urls failed

...

The fix is to create the "/etc/fsvs" folder

fsvs 1.1.16 was smart enough to remind me to create /var/spool/fsvs, but it apparently doesn't give a good error message when the "/etc/fsvs" folder does not exist.
