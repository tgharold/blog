---
layout: post
title: 'Installing cwRSync on Windows 2000'
date: '2004-06-10T10:29:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


The instructions over at [cwRSync's install page](http://www.itefix.no/cwrsync/) are a bit vague, so I'm going to jot down the steps that I use.  These steps are for installing rsync in a <b>server</b> configuration.  Since the install process needs to (optionally) create an user account and create a new service, you'll need administrative access to the machine that you are using.  (I'm not sure whether members of the Power Users group have enough privileges.)
<ol>
<li>Download cwRSync, open up the ZIP file, then extract/run <b>cwRsync_x.x.x_Installer.exe</b>.

</li>
<li>Answer "Yes" when asked if you want to continue with the install.

</li>
<li>Answer "Yes" when asked if you want to install cwRSync as a Windows Service.

</li>
<li>Specify the installation folder where you want to install cwRSync.  My personal preference is "c:\bin\cwrsync" instead of the default since our servers already have various command line tools installed under c:\bin.

</li>
<li>Enter the account name and password of the local user account that you are going to use for the cwRSync service.  It's a good idea to use a seperate account for the cwRSync service, but you may also specify an existing account name.

</li>
<li>The upload area can be set to anything.  In fact, you'll probably be removing whatever you set here when you [configure your rsyncd.conf file](http://rsync.samba.org/ftp/rsync/rsyncd.conf.html).  For now, set it to be a sub-folder under where you installed the cwRSync executables to.

</li>
<li>Click the "Install" button.  The installer will then create the folder where cwRSync is being installed to, (optionally) create the user account for the cwRSync service, and it will set restrictive permissions on the install folder so that only the service's user account has rights.

</li>
<li>That takes care of the basics.  If you want, view the installation details prior to exiting the install program and cleaning up.  Read the instructions on the popup dialog.

</li>
</ol>
Next, we need to finish setting up the RSync service in Windows.
<ol>
<li>Right-click on My Computer, pick "Manage".

</li>
<li>In the left panel, scroll down and open up the "Services and Applications" tree, then select "Services".

</li>
<li>Locate the "RsyncServer" service and double-click to open up the properties dialog.

</li>
<li>"General" tab: Change the "Startup type" setting to "Automatic".

</li>
<li>"Log On" tab: Re-type the password for the user account that you're using.  Click the "Apply" button to save your changes and Windows will popup a notification that the user account has been granted the rights to logon as a service.

</li>
<li>"Recovery" tab: Change these to match your preferences.  My personal preference is to restart the service on the first two failures, do nothing on subsequent failures, reseting the fail count after 1 day and restarting the service after a delay of 30 minutes.

</li>
<li>Click "OK" to save and exit.

</li>
<li>Don't start the service yet, the rsyncd.conf file needs to be configured first.

</li>
</ol>
You need to configure the rsyncd.conf file and set up your first "module" (a.k.a. a share path).  Find your rsyncd.conf file (it's in the folder where you installed cwRSync to) and open it up in a text editor (NotePad works).  Now, go read the [official rsyncd.conf help page](http://rsync.samba.org/ftp/rsync/rsyncd.conf.html).  Read it twice if it's your first time, because it's possible to put a very large gaping security hole into your setup if you're not careful.  The default settings at the top of the file are fine, but you may wish to change the "hosts allow = *" to "hosts allow = (your client machine IPs)" as a preventative first step.  Then, even if you screw up the other security mechanisms, you've at least limited which IP addresses an attacker can base an attack from.  (You can test this by telnet'ing to port 873 and seeing whether the rsync service drops your connection.)

Next, we need to start setting up "modules" in the rsyncd.conf file.  "Modules" are basically the same concept as a Windows share, except that you have to use rsync to access the files within the "module".  Ignore what it says on the [cwRSync install page](http://www.itefix.no/phpws/index.php?module=pagemaster&amp;PAGE_user_op=view_page&amp;PAGE_id=8&amp;MMN_position=32:23) about rsync modules having to be sub-directories under the cwrsync folder.  If you grant correct directory permissions to the cwRSync service account, then the service daemon will be able to read or read/write to the target folders without problems.

The default module installed is called "test".  Go ahead and comment it out with '#' symbols and save the file.  From my (limited) testing, it does not appear to be necessary to restart the rsync service in order for it to see changes in the rsyncd.conf file.
<pre>
[test]
path = /cygdrive/c/cwrsync/data
read only = false
transfer logging = yes
</pre>

There are two basic ways to use rsync and this will affect how you grant permissions to the rsync service account.

The first is a read-only ("pull") setup, where the clients can only pull files from the rsync server.  The rsync service account should only have Read &amp; Execute / List Folder Contents / Read permissions for the folder tree that you are going to publish.  In addition, when you setup your module in the configuration file, you should specify "read only = true" as a setting.

The second is a "push" setup where clients are writing changes to the rsync server.  The rsync service account will require "modify" permissions for the shared directory tree. Under your module configuration section in the rsyncd.conf file, a "push" setup must have "read only = false".

Now, for every directory tree on the rsync server that you wish to share, create a new module section (e.g. "[logs]" or "[web]" or "[joes_backup]").  Verify that the cwRSync service account has proper permissions to the file system tree.  Then add the following options (at a minimum) below the module section name:
<pre>
[joes_backup]
path = /cygdrive/e/backup/joe
read only = false
</pre>

That allows <b>any client</b> who manages to authenticate with the rsync service to write the E:\Backup\Joe on the rsync server.  That is not exactly secure and you should take additional steps to lock it down through the use of "hosts allow", "auth users", "secrets file" and perhaps ssh.  Securing your box is a bit beyond the scope of this post.  It's also a bit beyond my experience level since I'm just getting started with rsync.

(Update: See [Securing cwRSync](/blog/2004-06-18-securing-cwrsync/).)
