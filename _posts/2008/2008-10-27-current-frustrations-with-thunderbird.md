---
layout: post
title: 'Current frustrations with Thunderbird'
date: '2008-10-27T11:00:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


I'm currently plagued by the following showing up in my error console in Thunderbird 2.0.0.17 (20080914).

```
Error: uncaught exception: [Exception... "Component returned failure code: 0x80550006 [nsIMsgFolder.getMsgDatabase]"  nsresult: "0x80550006 (<unknown>)"  location: "JS frame :: chrome://messenger/content/mailWidgets.xml :: parseFolder :: line 2061"  data: no]</unknown>
```

The other thing that happens is that eventually, Thunderbird stops talking (hangs) to my IMAP mail server (over SSL).  So I'm unable to send e-mail messages over SMTP/SSL (port 465), or am I able to retrieve any messages from our IMAP (Dovecot over SSL) server until I restart Thunderbird.

It can take anywhere from 5 minutes to 5 hours for this problem to occur.  Starting in safe mode fixes some of the issue, but Thunderbird still chokes up after I've hit a few dozen IMAP folders to get new headers and to download messages.
