---
layout: post
title: 'Microsoft Outlook error 0x800CCC92'
date: '2006-05-31T15:46:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>I get the following error when trying to retrieve e-mail from our POP3 Postfix mail server (on Solaris 5.8).  We're also using Sendmail to interact with the PreciseMail spam filtering system:

Task 'mail.example.com - Sending and Receiving' reported error (0x800CCC92): 'Your e-mail server rejected your login.  Verify your user name and password in your account properties.  Under Tools, click E-mail accounts.  The server responded: ??RR /usr/mail/.thomas.pop lock busy! Is another session active? (11)'

Basically, it indicates that the previous POP3 connection terminated in an unclean manner.

Links:
[Telnet - POP Commands (retrieving mail using telnet)](http://www.yuki-onna.co.uk/email/pop.html)
[POP lock busy](http://www.exit109.com/emailproblems.html#poplock)

Looking at the contents of /usr/mail ("ls -la /usr/mail") you will see that there are at least one (and possibly multiple) .pop files in the directory (".username.pop").<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2006.shtml">2006</a>
		<div class="Byline">
			posted by Thomas at 
			[15:46](http://www.tgharold.com/techblog/2006/05/microsoft-outlook-error-0x800ccc92.shtml)

		</div>