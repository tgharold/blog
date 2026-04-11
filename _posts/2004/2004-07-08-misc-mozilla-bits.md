---
layout: post
title: 'Misc Mozilla Bits'
date: '2004-07-08T09:49:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Just a few misc Mozilla 1.7 settings that I've found useful.  All of these need to be added/changed in your <b>prefs.js</b> file in your profile directory.  Make sure that you've exited out of all Mozilla windows, including the QuickLaunch icon in the system tray before making your edits.  Otherwise, when Mozilla exits again later, it will overwrite your changes.

It's also a good idea to make a backup file of your prefs.js file prior to making changes.

1) Changing the trash folder in Mozilla Mail (or Thunderbird) to match what is used on your IMAP server.  The standard trash folder is called "Trash", but my IMAP service uses "Deleted Items" instead.  To make things simple, I changed Mozilla to use "Deleted Items" as well for that particular account.  Replace "serverx" with the appropriate server number (e.g. "server7") that matches your IMAP account.

user_pref("mail.server.server<i>x</i>.trash_folder_name", "Deleted Items"); 

Changing the default folder for saved copies of sent items from "Sent" to "Sent Items" is a bit easier.  Just right-click on the e-mail account and pick "Properties", then look in "Copies & Folders" and change where Mozilla/Thunderbird stores copies of e-mails that you have sent.

For the technically minded, the lines in "prefs.js" that are affected by this change are:

user_pref("mail.identity.id5.fcc_folder", "imap://username@imap.somedomain.com/Sent Items");
user_pref("mail.identity.id5.fcc_folder_picker_mode", "1");

2) Displaying an error page instead of just a blank page when a webpage times out.  One of the most annoying features in base Mozilla/Firebird is the way that they handle timeout errors.  Instead of getting an error message on the screen, you get a blank page and the location bar will have been cleared.  Which, if you were trying to load the page in the background for later viewing, means you have to try and remember or figure out what link you were trying to look at.  Adding the following line to your prefs.js file will at least give you an error display that lets you retry the URL:

user_pref("browser.xul.error_pages.enabled", true);
