---
layout: post
title: 'Rsync and SSH on Windows 2003 Server'
date: '2006-08-21T11:55:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>Taking another stab at setting up RSync and SSH on our Windows 2003 servers.  The goal is that we can upload web files to a central server and then have it synchronize the other servers in the array.  Once again, I'm going to use the [cwRsync and copSSH packages](http://www.itefix.no/) (latest version is 2.0.9).

Installation on a Windows 2003 Domain Controller:
<ol>

<li>Download cwRSync, open up the ZIP file, then extract/run cwRsync_Server_x.x.x_Installer.exe.

</li>
<li>Click "Next" to move past the splash screen

</li>
<li>Click "I Agree" to move past the license screen

</li>
<li>Select both the "Rsync Server" and "OpenSSH Server" (unless you have already installed and configured SSH) then click "Next"

</li>
<li>Choose your installation location, the default is "C:\Program Files\cwRsyncServer"

</li>
<li>Click "Install" to begin the installation process

</li>
<li>cwRsync will install and create a default service account with a randomly generated password.

</li>
<li>Write down the service account password.

</li>
<li>Click "Close" when the install has finished.

</li>
</ol>

So now if you look in "Active Directory Users and Computers", there should be a newly created account called "SvcwRsync".  Since we are installing this on a domain controller, you should rename this account to "SvcwRsync_SERVERNAME" so that it doesn't cause problems for other installations.  You'll also need to change the login details for the "RsyncServer" and "OpenSSH SSHD" services.

Once you have things configured, make sure to go to the Services control and set the services to start up automatically.  I also recommend configuring the Recovery tab so that the services are automatically restarted after 2 or 5 minutes.

...

Now to start locking things down.  First, I'm going to restrict what interfaces (IP addresses) that the cwRSync service can listen on by adding an address line to rsyncd.conf.  

address = 127.0.0.1

One the machine that you will be using to talk to the rsync daemon on the host server, you'll also need the cwRsync tools installed along with OpenSSH.  Because the rsync daemon can only listen on 127.0.0.1 (localhost), we'll need to create an SSH tunnel from the client machine to the host server before we can talk to the rsync daemon.

One the client machine:

1. Create a new folder under "C:\Program Files\cwRsyncServer\home" for the new user.  In my particular case, I'm calling my user "backuppull" because I am pulling backup files off of the rsync server and down to my local machine.

2. Create a ".ssh" folder under that new home folder.

3. Open up a command window (Start, Run, "cmd") and change directories to the home folder ("C:\Program Files\cwRsyncServer\home\backuppull")

4. Create ssh keys for this user.  Since we want to do this sync in a batch file without user-interaction, they'll need to be created with null passwords.  You may wish to use the "-b 2048" option to create stronger keys (recommended for RSA, DSA can only be up to 1024 bits).

mkdir .ssh
..\..\ssh-keygen -t rsa -N "" -b 2048 -f .ssh\id_rsa
..\..\ssh-keygen -t dsa -N "" -b 1024 -f .ssh\id_dsa

5. You will now need to transfer the <b>public</b> key files to the host server.  Again, you will create a new home directory for the user in the "C:\Program Files\cwRsyncServer\home" folder tree along with creating a ".ssh" folder under that home folder.  The two files that need to be copied are:

id_dsa.pub
id_rsa.pub

6. Now append the contents of these files to the ".ssh/authorized_keys" file on the host server.

type id_dsa.pub &gt;&gt; authorized_keys
type id_rsa.pub &gt;&gt; authorized_keys

7. Now to configure SSHD on the host server.  You will need to find and edit the sshd_config file (probably in "C:\Program Files\cwRsyncServer\etc").  The following changes should be made in the current version default settings.

PermitRootLogin no
PasswordAuthentication no<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2006.shtml">2006</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/RSync.shtml">RSync</a>
		<div class="Byline">
			posted by Thomas at 
			[11:55](http://www.tgharold.com/techblog/2006/08/rsync-and-ssh-on-windows-2003-server.shtml)

		</div>