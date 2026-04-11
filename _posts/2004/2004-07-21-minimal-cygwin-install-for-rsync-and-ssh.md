---
layout: post
title: 'Minimal Cygwin install for RSync and SSH'
date: '2004-07-21T19:19:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>Source links:

[How to setup the secure shell daemon on a Windows 2000 machine?](http://ist.uwaterloo.ca/~kscully/cygwin/CygwinSSHd_win2k.html)
[Windows Rsync Server Setup](http://www.gaztronics.net/rsync.php)
[CygwinInstallationGuide ](http://twiki.complexfission.com/twiki/bin/view/Computer/CygwinInstallationGuide) (a wiki topic about the cygwin installation)

<b>Note:</b> The following probably <b>doesn't work</b> (probably missing a package, or the fact that I have GNU's unix tools for Win32 installed is problematic), but I might come back and make it work later so I'm leaving it here for now.  I ran into trouble when trying to configure SSH.  Right now, I've gone back to my original plan of either [hacking apart the Cygwin files](/techblog/2004/07/hacking-together-minimal-rsync-for.shtml) and manually copying only the DLLs and EXEs that I need or using the [OpenSSH for Windows project at SourceForge](http://sshwindows.sourceforge.net/).

1. Run the [Cygwin setup.exe](http://www.cygwin.com/setup.exe) file and start the instllation.  I chose to install to "c:\bin\cygwin", but left the rest of the options "as-is".  Pick your mirror (use the [Cygwin public mirrors page](http://cygwin.com/mirrors.html) to find one close to you).

2. On the "Select Packages" screen, select the "Curr" option and make sure it says "Category" next to the "View" button at the top.  The installation dialog is (finally) re-sizeable, so stretch it out or maximize it so you can see all of the columns.

3. Beside the "+All" category, it will say "Install", "Uninstall", ... click on the word until all of the categories say "Uninstall".  (Note: These steps assume that you're doing a <b>new</b> Cygwin install and that you don't already have Cygwin installed.)  Now we can start picking the minimum number of packages required to setup SSH and RSync.

4a. Under the "+Admin" category, you'll need to install the "cygrunsrv" package (click once on the "Skip" indicator under the "New" column).  This will turn on a few other packages that this package depends on (mostly under the "+Base", "+Libs", and "+Shells" categories).

4b. Open up the "+Net" category and select the "rsync" and "openssh" packages. You'll also end up with "openssl" which is required in order to use "openssh". 

5. Click the "Next" button to start downloading and installing the packages.  If the download fails, choose another mirror, double-check your package selections (my copy remembered which packages I had already selected), and try again.  The base install size required around 7MB of downloads and expanded out to 24MB (34MB actual due to a 4KB cluster size).

6. Fire up the cygwin shell, you should see a command-line window open with a "$" prompt.  Try out a few unix commands (pwd, ls, whoami) to see if things are working.

7. Further steps... (I'll cover these in future posts)

a) Setup your rsync.conf file (in the "etc" folder)
b) create a service account for use by the rsync service
c) create a Windows service using the "cygrunsvc" tool
d) setup OpenSSH and then re-configure rsync to use it<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2004.shtml">2004</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/RSync.shtml">RSync</a>
		<div class="Byline">
			posted by Thomas at 
			[19:19](http://www.tgharold.com/techblog/2004/07/minimal-cygwin-install-for-rsync-and.shtml)

		</div>