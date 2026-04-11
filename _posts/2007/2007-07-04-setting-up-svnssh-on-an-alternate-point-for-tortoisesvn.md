---
layout: post
title: 'Setting up svn+ssh on an alternate point for TortoiseSVN'
date: '2007-07-04T14:50:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


This builds off a post to the TortoiseSVN user list: [Specifying custom port for svn+ssh: a workaround](http://svn.haxx.se/tsvnusers/archive-2007-01/0272.shtml)
<ol>

<li>Right-click on the Pageant icon in the system tray (I'm assuming that you're loading the SSH public key that you use for SVN into Pageant).

</li>
<li>Choose "New Session"

</li>
<li>Enter the hostname / IP address and SSH port that you'll be connecting to.  If you're going to connect as "svn+ssh://thomas@svn.tgharold.com:2222", then this would be "svn.tgharold.com" and "2222".

</li>
<li>Go back to the "Session" tab and name the session as "svn.tgharold.com:2222".

</li>
</ol>

Now you will be able to use both TortoiseSVN and the command-line version of SVN to talk to your repository over the alternate SSH port.

<b>Why do this?</b>

This is useful for cases where you want to put a SVN server on a publicly accessible IP address.  What you will find is that if you leave SSH running on the default port, you will be inviting attacks on your SSH server.  On the other hand, if you put the SSH server on an alternate port, you'll find that it gets attacked a lot less often (1-2 orders of magnitude difference would be likely).

Since mid-Oct of last year (around 8.5 months), we've logged <b>90,300</b> attack attempts against our SSH server.  Usually they come in batches of attempting to guess accounts that normally exist or by attacking a list of common usernames.  Since we don't allow root login, we don't allow password authentication, we only allow public key authentication and our SSH keys are limited to running "svnserve -t", we have yet to see a break-in attempt succeed.
