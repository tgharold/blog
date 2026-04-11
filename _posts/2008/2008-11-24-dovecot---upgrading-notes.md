---
layout: post
title: 'Dovecot - Upgrading Notes'
date: '2008-11-24T11:57:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>At the office, we're using a virtual Dovecot server where each person's mail folders are owned by an unique user in the Linux account system.  

[Dovecot: Virtual Users](http://wiki.dovecot.org/VirtualUsers) - covers the basics

[Dovecot: UserIds](http://wiki.dovecot.org/UserIds#mailusers) - explains why we use different UIDs for different accounts

[Dovecot: LDA](http://wiki.dovecot.org/LDA) - explains how to setup the "deliver" executable to deal with multiple user IDs.

<i>Multiple UIDs

If you're using more than one UID for users, you're going to have problems running deliver. Most MTAs won't let you run deliver as root, so for now you'll need to make it setuid root. However it's insecure to make deliver setuid-root, especially if you have untrusted users in your system. You should take extra steps to make sure that untrusted users can't run it and potentially gain root privileges. You can do this by placing deliver into a directory where only your MTA has execution access. </i>

All of which means that whenever we update Dovecot with "yum update", we need to make sure that we fix up the Dovecot "deliver" executable file (which uses setuid) to also match.

So let's figure out which "deliver" we need to fix up each time:

<code># find / -name deliver
/usr/local/libexec/dovecot/lda/deliver
/usr/libexec/dovecot/deliver</code>

Alternately, look at Postfix's master.cf file:

<code># grep "deliver" /etc/postfix/master.cf
# grep "deliver" /etc/postfix/master.cf
# Many of the following services use the Postfix pipe(8) delivery
# The Cyrus deliver program has changed incompatibly, multiple times.
  flags=R user=cyrus argv=/usr/lib/cyrus-imapd/deliver -e -m ${extension} ${user}
  user=cyrus argv=/usr/lib/cyrus-imapd/deliver -e -r ${sender} -m ${extension} ${user}
# Other external delivery methods.
     flags=DRhu user=vmail:vmail argv=/usr/local/libexec/dovecot/lda/deliver -f ${sender} -d ${recipient}
#    flags=DRhu user=vmail:vmail argv=/usr/lib/dovecot/deliver -d ${recipient}</code>

The key line in that jumble being:

<code>flags=DRhu user=vmail:vmail argv=/usr/local/libexec/dovecot/lda/deliver -f ${sender} -d ${recipient}</code>

If we take a look at the file size, ownership, attributes and security settings (for SELinux):

<code># cd /usr/libexec/dovecot/
# ls -la deliver 
-rwxr-xr-x 1 root root 802824 Jul 24 06:32 deliver
# ls -lZ deliver 
-rwxr-xr-x  root root system_u:object_r:dovecot_deliver_exec_t deliver

# cd /usr/local/libexec/dovecot/
# ls -la
total 24
drwx------ 2 vmail vmail 4096 Jun 16 23:00 lda
# ls -lZ
drwx------  vmail vmail system_u:object_r:bin_t          lda

# cd /usr/local/libexec/dovecot/lda/
# ls -la deliver
-rwsr-xr-x 1 root root 802824 Aug 12 18:12 deliver
# ls -lZ deliver
-rwsr-xr-x  root root system_u:object_r:dovecot_deliver_exec_t deliver</code>

What we see here is a couple of things regarding how the Dovecot LDA is setup.

<ol>

<li>The Postfix master.cf file controls which "deliver" gets used for local delivery of e-mail.  (The "deliver" executable is part of Dovecot, so we're using Dovecot for local delivery.)</li>

<li>/usr/local/libexec/dovecot//lda/deliver - this is where our "setuid" version of the "deliver" executable is located</li>

<li>The "lda" folder is owned by vmail:vmail (limited access) and only the vmail user can access the contents of the folder.  Postfix knows to use the vmail user because that's what we told it to do in the master.cf file.</li>

<li>Both the official "deliver" executable (in the /usr/libexec/dovecot/ directory) and our "setuid" copy have the same byte size, date/time, and are both labled as "system_u:object_r:dovecot_deliver_exec_t" for SELinux.</li>

</ol>

The steps that we take when we update Dovecot are then:

<ol>

<li>
<b>yum update dovecot</b> - updates the Dovecot executables to the latest version over at the <b>atrpms</b> repository</li>

<li>
<b>cp --no-preserve=all /usr/libexec/dovecot/deliver /usr/local/libexec/dovecot/lda/deliver</b> - copies the new deliver executable over to the lda folder where we will setuid on it</li>

<li>
<b>chmod u+s</b> is what we use to set the setuid bit on the copy in the lda folder, but we shouldn't need to do that once we set things up initially</li>

<li>
<b>service dovecot restart</b> - restarts the Dovecot service using the new executables</li>

<li>
<b>grep "AVC" /var/log/audit/audit.log | tail -n 50</b> - look for any errors relating to Dovecot</li>

</ol>
<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2008.shtml">2008</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Dovecot.shtml">Dovecot</a>
		<div class="Byline">
			posted by Thomas at 
			[11:57](http://www.tgharold.com/techblog/2008/11/dovecot-upgrading-notes.shtml)

		</div>