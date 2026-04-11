---
layout: post
title: 'cwRSync and copSSH'
date: '2005-05-03T20:29:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>
<i>Note: These directions are works-in-progress... in fact, they might not even work at all.  I got side-tracked before I could finish this and will re-visit it at some point in the future.</i>

The folks who created cwRSync ([www.itefix.no](http://www.itefix.no/)) have now released a package called copSSH which is basically SSH for windows and works with cwRSync.  I'll be refering back to my old post about [installing cwRSync](http://www.tgharold.com/techblog/2004/06/installing-cwrsync-on-windows-2000.shtml).  The latest version I have is from late April 2005 and includes bug fixes for Windows Server 2003.

Also see the [rsyncd.conf file for configuring rsync](http://rsync.samba.org/ftp/rsync/rsyncd.conf.html).

These steps are for installing rsync in a <b>server configuration</b> (meaning that it will be listening on the listed ports). Since the install process needs to (optionally) create an user account and create a new service, you'll need administrative access to the machine that you are using. (I'm not sure whether members of the Power Users group have enough privileges.)

<ol>

<li>Download cwRSync, open up the ZIP file, then extract/run cwRsync_x.x.x_Installer.exe.

</li>
<li>Click "Next" to begin the install.

</li>
<li>Read and agree to the licence.

</li>
<li>Make sure that both the client and server components are checked off and click "Next".

</li>
<li>Choose your installation location.  I prefer to put mine in a custom location (C:\bin\cwRsync).

</li>
<li>Click "Install" to begin the installation.

</li>
<li>The default user account is "cwrsync" (with a random password) and it will be installed as a service.  You will probably want to change the password to something stronger and adjust the properties of the service in Computer Management.  Specifically, I changed the Recovery tab to auto-restart the service after 5 minutes if it dies.  I've left the "auto-start" setting to "manual" until I've finished configuration and testing.

</li>
<li>By default, the newly created "cwRSync" folder grants permissions to the Administrators group (full control), the CWRSYNC user account (full control) and the Users account (read/execute).

</li>
<li>Now you should configure your rsyncd.conf file.

</li>
</ol>

Now we need to install copSSH.

<ol>

<li>Download copSSH, open up the ZIP file, then extract/run copSSH_x.x.x_Installer.exe.

</li>
<li>Click "Next" to begin the install.

</li>
<li>Read and agree to the licence.

</li>
<li>Change the install folder to match where you installed cwRSync (C:\bin\cwRsync).  (This is according to the FAQ on the itefix.no web site.)

</li>
<li>This creates a new service called "OpenSSH SSHD" with a default users account of "SvcCOPSSH"

</li>
<li>You will probably want to change the password to something stronger and adjust the properties of the service in Computer Management.  Specifically, I changed the Recovery tab to auto-restart the service after 5 minutes if it dies.  I've changed the "auto-start" setting to "manual" until I've finished configuration and testing.

</li>
<li>Notice that the copSSH installation blows away existing permissions on the c:\bin\cwRSync folder.  This may require fixing (I have to test first).

</li>
<li>Re-start the SSHD service in manual mode (if you stopped it earlier).

</li>
</ol>
<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2005.shtml">2005</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/RSync.shtml">RSync</a>
		<div class="Byline">
			posted by Thomas at 
			[20:29](http://www.tgharold.com/techblog/2005/05/cwrsync-and-copssh.shtml)

		</div>