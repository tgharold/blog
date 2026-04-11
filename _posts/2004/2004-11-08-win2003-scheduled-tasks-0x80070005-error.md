---
layout: post
title: 'Win2003 Scheduled Tasks 0x80070005 Error'
date: '2004-11-08T10:49:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Trying to setup a backup job (kicked off by a .cmd file) on Windows 2003.  I have a special, limited rights, user account created (rather then running the backup job under the administrator account).  Everything seems fine until I go to test my scheduled task.

Looking at the log (Scheduled Tasks - Advanced - View Log) will show: 

```
Unable to start task.
The specific error is:
0x80070005: Access is denied.
```

["Access is denied" error message when you run a batch job on a Windows Server 2003-based computer](http://support.microsoft.com/?kbid=867466)

As expected, this is a permissions error.  Specifically, you need to grant permissions for batch processes to use "cmd.exe".
