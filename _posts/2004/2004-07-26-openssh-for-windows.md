---
layout: post
title: 'OpenSSH for Windows'
date: '2004-07-26T17:01:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>I've pretty much given up on trying to extract the key bits from Cygwin in order to setup a SSHD server.  The [OpenSSH for Windows](http://sshwindows.sourceforge.net/) project at SourceForge seems to have what I'm looking for, they just don't have the RSync application included.

For an excellent introduction to SSH, check out [OpenSSH for the impatient](http://www.ypsolog.com/docs/openssh.html).

For setting up OpenSSH on a server, go ahead and grab the packages from the [OpenSSH for Windows](http://sshwindows.sourceforge.net/) SourceForge project.  The version that I'm using at the moment is "setupssh381-20040709".  Inside that file you'll find a "setupssh.exe" which will install the packages as well as creating the Windows Service.  I like to install my copy to "c:\bin\openssh".

Now open up the "c:\bin\openssh\docs\readme.txt" (or quickstart.txt) and follow the directions in order to create the "group" and "passwd" files.  Then start up the OpenSSHD service (either from the command line as shown in quickstart.txt or using the Services control panel).

You should now be setup so that you can SSH in to the server from another workstation and get a command prompt on the server.  However, the default install is pretty good in security, so you should not need to change anything sshd_config file.  However, some things you may wish to change are:

1) The default server key-length is 1024 bits (which is okay, but not outstanding anymore).  The man page says key lengths over 1024 bits don't matter, but another books says you should use 2048 bit keys.

2) Some key variables in the sshd_config file are:

a) PermitRootLogin - should be set to "no" which prevents you from logging in as root from another machine.  

b) RSAAuthentication - setting this to no will disable the ability to login with a SSH1 client (I think...).  The default sshd_config file has this explicitly set to "no".

c) PasswordAuthentication - you may want to change this to "no" and force users to setup a public/private key pair in order to login to the server.

(note: this post was never completed... so use with a grain of salt)<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2004.shtml">2004</a>
		<div class="Byline">
			posted by Thomas at 
			[17:01](http://www.tgharold.com/techblog/2004/07/openssh-for-windows.shtml)

		</div>