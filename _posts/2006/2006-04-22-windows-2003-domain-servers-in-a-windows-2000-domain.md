---
layout: post
title: 'Windows 2003 Domain Servers in a Windows 2000 Domain'
date: '2006-04-22T20:01:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>So, I'm working on installing our first Windows 2003 server as a domain controller in an existing Windows 2000 Active Directory domain.  Now, if I remember correctly, when I first tried this last fall, it errored out due to the AD domain not having all of the schema details needed for a Windows 2003 domain controller.

Ah, here we go... got the error message:

------------------------

Title: Active Directory Installation Wizard

Msg: The Active Directory Installation Wizard cannot continue because the forest is not prepared for installing Windows Server 2003.  Use the Adprep command-line tool to prepare both the forest and the domain.  For more information about using the Adprep, see Active Directory Help.

"The version of the Active Directory schema of the source forest is not compatible with the version of Active Directory on this computer."

------------------------

So... off we go to research this.  The server already exists as a member server within our Windows 2000 domain.  A good search term is probably going to be "[forest is not prepared for installing Windows Server 2003](http://www.google.com/search?num=20&amp;hl=en&amp;lr=&amp;safe=off&amp;c2coff=1&amp;q=%2B%22forest+is+not+prepared+for+installing+Windows+Server+2003%22&amp;btnG=Search)".

[Error message when you run the Active Directory Installation Wizard: ...](http://support.microsoft.com/?kbid=917385) (Microsoft)
[Dcpromo.exe and Winnt32.exe log errors when you...](http://support.microsoft.com/?id=278875)
[Title: Problen promoting W2003 as additional DC over a VPN](http://www.experts-exchange.com/Operating_Systems/Windows_Server_2003/Q_21820446.html)

The second link is the most helpful of the bunch for this particular case (an existing Windows 2000 domain where I'm trying to add new domain controllers that are running Windows 2003).

However, since there are potential issues with Mac clients when upgrading to Windows 2003 domain servers, I'm going to hold off on the upgrade until my next trip to the main office.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2006.shtml">2006</a>
		<div class="Byline">
			posted by Thomas at 
			[20:01](http://www.tgharold.com/techblog/2006/04/windows-2003-domain-servers-in-windows.shtml)

		</div>