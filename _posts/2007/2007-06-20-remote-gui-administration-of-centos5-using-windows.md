---
layout: post
title: 'Remote GUI administration of CentOS5 using Windows'
date: '2007-06-20T11:55:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Over the years, I've become very spoiled by Windows Terminal Services that we use to administer our Windows 2000 and Windows 2003 servers.  It's fast, it's slick, it allows copy-paste and with a bit of command line fu you can connect to the physical display (instead of one of the two virtual sessions).  It also uses built-in Windows authentication and offers encryption.

So, now that I'm rolling out CentOS 5 servers - I need something similar that allows me to look at the graphical UI on the box from elsewhere.  From what I can tell, my options are:

<b>KVM that supports TCP/IP</b>

Probably one of the holy grails of remote administration.  It allows you to see everything from the BIOS setup screen onward without needing to be physically at the machine.  The downside is cost.  So while I will eventually be hooking one of these up, it's not in the budget for this quarter.

<b>VNC over SSH</b>

I have a love/hate relationship with VNC.  On the Windows clients, we use UltraVNC with built-in Windows authentication and the AES encryption plug-in.  

But if you want to wrap VNC with SSH, you have to configure port forwarding all the time in PuTTY.  Which turns connecting to a remote server into a multi-step process.  With Windows' RDP, I just say "connect to IP address X" and I'm done (and I can connect in as anyone that I want).  For PuTTY+VNC, I have to jump through a lot more hoops.

There's also the (possible) issue that VNC is nowhere as efficient over the network as RDP.  Once you use Terminal Services' RDP, you'll be spoiled and never want to use older technologies.  It (almost) never glitches, it's lightning fast and responsive, and it's just pure remote GUI goodness (except for being a MS-only protocol).

<b>X11 over SSH</b>

This is where I'm heading at the moment.  It uses SSH for authentication, so we can lock things down that way (forcing the use of public keys).

Now, a word of caution.  A misconfigured SSH or X11 server is a security breach waiting to happen.  Pay close attention to chapter 9 in <i>SSH, The Secure Shell, The Definitive Guide</i> by Barrett, Silverman &amp; Byrnes (published by O'Reilly).

<b>Installing [Xming](http://www.straightrunning.com/XmingNotes/) on Windows</b>

In order to do X11 on Microsoft Windows, you need to install "X Server" software on the Windows box.  While there are pay options out there, I'd suggest starting with Xming which is free (GPLv2).  You'll want to download and install both Xming and Xming-fonts.

<b>Configuration of sshd and X11</b>

In order for the local X Server (Xming - running on your Windows system) to talk to the remote Linux server, you'll need to verify some settings on the Linux server.  First up is configuration of the sshd daemon (typically /etc/ssh/sshd_config for OpenSSH). Look for the following 2 lines and make sure they are configured correctly:

X11Forwarding yes
#X11UseLocalhost yes

By default, OpenSSH ships with X11Forwarding set to "no" but the default for X11UseLocalhost is "yes".  So you should only have to add the "X11Forwarding yes" line.

<b>Create a PuTTY session</b>

I'll make the assumption that you're going to use a PuTTY public-key pair.  If you need to install a generated PuTTY key (maybe you want to use a separate PuTTY key for X11 forwarding), then here are the directions for OpenSSH.

(login as yourself or as root and then "su" to your username)
# cd ~/.ssh
# cat &gt; machinename@svn.pub
(paste in PuTTY key)
# ssh-keygen -i -f machinename@svn.pub &gt;&gt; authorized_keys
(Ctrl-D to exit)
<ol>

<li>Right-click on the Pageant icon in the system tray and choose "New Session".  

</li>
<li>Enter the hostname (i.e. 192.168.1.1)

</li>
<li>Go to the Connection -&gt; SSH -&gt; X11 tab

</li>
<li>Turn ON "X11 forwarding"

</li>
<li>Display location should be: localhost:0

</li>
<li>Go back to the Session tab

</li>
<li>Enter a name in the Saved Sessions text box (i.e. "MyHost-X11") and click on "Save"

</li>
<li>Click the "Open" button to connect to the server

</li>
</ol>

If all goes well, you should see a line like:

/usr/bin/xauth:  creating new authority file /home/thomas/.Xauthority

Which tells us that SSH is ready to do some X forwarding.

<b>Fire up Xming</b>

If you haven't already ran Xming you should run XLaunch and just roll through the defaults.  Now, in the PuTTY window that is sitting at a command prompt, try:

# xeyes

And you should see the xeyes application open up on your Windows system.  If you want to continue to start up other X applications, put an ampersand (&amp;) at the end of the line.

<b>More advanced stuff</b>
<ol>

<li>Fire up XLaunch

</li>
<li>Select "One window" and click "Next"

</li>
<li>Select "Start a program" and click "Next"

</li>
<li>The start program should be either "gnome-session" or "startkde"

</li>
<li>Select Run Remote using PuTTY (plink.exe) and turn on the compression option.

</li>
<li>Enter the IP address or hostname in "Connect to computer" of the Linux box that you are connecting to

</li>
<li>Enter your username in the "Login as user"

</li>
<li>Click the "Next" button

</li>
<li>In the "Additional parameters", enter "-screen 0 1024 768" which will set screen zero to be 1024x768

</li>
<li>If you run your SSH server on a non-standard port, enter "-P port" in the PuTTY extra options field (run "plink" at a Windows command prompt to see the possible options)

</li>
<li>Save your configuration file and click "Finish"

</li>
</ol>

If all goes well, you should see the Gnome desktop!

<b>Final thoughts (for the moment)</b>

Now, it's still not as slick as Terminal Services.  But it seems to work just fine and gives me a GUI desktop.  I still plan on doing most of my administration from the command line, but this provides a nice GUI for those who follow in my footsteps.
