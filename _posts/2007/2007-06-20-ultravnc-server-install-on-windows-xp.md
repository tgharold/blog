---
layout: post
title: 'UltraVNC (Server) Install on Windows XP'
date: '2007-06-20T08:02:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Installing UltraVNC (see also "[UltraVNC Installation](http://www.uvnc.com/install/installation.html)")
<ol>

<li>Download [UltraVNC](http://www.uvnc.com/) for MS Windows

</li>
<li>Run the setup program (currently this is: UltraVNC-100-RC203-Setup.exe)

</li>
<li>Accept the license agreement and read the Information screen

</li>
<li>Use the default install destination location

</li>
<li>Choose "Complete Install"

</li>
<li>Use the default Start Menu Folder

</li>
<li>Turn ON "Register Ultr@VNC Server as system service"

</li>
<li>Turn ON "Start or restart Ultr@VNC service"

</li>
<li>Turn OFF the (3) options that create desktop icons

</li>
<li>Turn ON "Associated .vnc files with Ultr@VNC Viewer"

</li>
<li>Click "Install" to start the installation.

</li>
</ol>

WinVNC: Default Local System Properties (see "[configuration](http://www.uvnc.com/install/configuration.html) for details)
<ol>

<li>Turn OFF "Enable JavaViewer"

</li>
<li>Turn ON "Display Query Window", Set the timeout to 60 seconds, with "Accept" as the default action.

</li>
<li>Under "Multi viewer connections", CHANGE to "Keep existing connections"

</li>
<li>Under "Authentication", set a secure default password

</li>
<li>Under "Authentication", turn ON "Require MS Logon", turn ON "New MS Logon"

</li>
<li>Click on "Configure MS Logon Groups", Add, enter "Administrators" (note the plural) and click "OK".  Grant that group full control and click "OK" to close the UltraVNC Security Editor window.

</li>
<li>Most other options can be left "as is"

</li>
</ol>

AES Encryption plugin (a.k.a. DSM)
<ol>

<li>Download the [AESV2 Plugin](http://msrc4plugin.home.comcast.net/aesv2plugin.html) (currently: AESV2Plugin100.zip)

</li>
<li>Extract the .DSM file to the program folder where you installed UltraVNC (usually: C:\Program Files\UltraVNC), see  "[DSM quick start](http://msrc4plugin.home.comcast.net/dsmplugins.html)" for more information.

</li>
<li>Re-open the "Default Local System Properties" window for the UltraVNC server (Start -> UltraVNC -> UltraVNC Server -> Show Default Settings).  Alternately, start up the service helper systray app (Run Service Helper) and go to "Admin Properties")

</li>
<li>Under "DSM Plugin", turn ON the "Use:" checkbox and select "AESV2Plugin.dsm" from the list.

</li>
<li>Click "OK"

</li>
</ol>
