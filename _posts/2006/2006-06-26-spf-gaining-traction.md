---
layout: post
title: 'SPF gaining traction?'
date: '2006-06-26T07:03:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


As I was signing up for a few mailing lists, I was glancing through the confirmation / welcome messages and I see that there are now some SPF headers showing up in those checks.  The <b>ezmlm</b> list manager program includes the full body of the subscribe/confirmation message in its responses:

```
Received-SPF: pass (asf.osuosl.org: domain of tgh@tgharold.com designates 69.36.9.168 as permitted sender)
Received: from [69.36.9.168] (HELO omega.jtlnet.com) (69.36.9.168)
    by apache.org (qpsmtpd/0.29) with ESMTP; Sun, 25 Jun 2006 19:04:13 -0700
```

A quick glance through my other mailing list confirmation messages didn't turn up any more.  Other mailing list software doesn't reflect back the sign-up mail message so it's not possible to see if SPF checks are being used or not.

I run a very strict SPF record for this domain.  I wish companies would check the SPF record before bouncing messages back to me (due to joe-jobs by spammers).
