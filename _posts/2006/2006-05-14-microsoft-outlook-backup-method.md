---
layout: post
title: 'Microsoft Outlook Backup method'
date: '2006-05-14T10:17:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


This is how I backup my PST files whenever I login to my laptop.  Because I always have MSOutlook open, I find it difficult to get a good backup of the PST files.

1) You will want a copy of [Info-Zip's ZIP and UNZIP executables](http://www.info-zip.org/).

2) Create a folder on your hard drive to hold these executables.  I recommend creating a folder called "C:\bin" and adding that folder to your system's PATH statement.  

Right-click on My Computer, Properties, Advanced, Environment Variables... Under System Variables, highlight "PATH" and click "Edit"... place C:\BIN at the start.  It should look similar to "<b>C:\bin;</b>%SystemRoot%\system32;%SystemRoot%...".  Make sure you leave the existing directories in the list and just add the "C:\bin;" at the start of the listing.

Place the zip.exe and unzip.exe files in the C:\BIN folder.

3) Locate your PST files.  Create the following as a text file in the same directory.  Name it as "backupemail.cmd".

<code>@echo off
rem Backup my Outlook PST files

IF NOT EXIST "X:\EMailBackup\*" GOTO quit
IF NOT EXIST "C:\Data\EMail\*.pst" GOTO quit

C:
CD "\Data\EMail"
ZIP -u1 X:\EMailBackup\MyPSTs.zip *.pst

X:
CD \EMailBackup

IF EXIST MyPSTs-3.zip DEL MyPSTs-3.zip 
IF EXIST MyPSTs-2.zip REN MyPSTs-2.zip MyPSTs-3.zip
IF EXIST MyPSTs-1.zip REN MyPSTs-1.zip MyPSTs-2.zip
IF EXIST MyPSTs.zip REN MyPSTs.zip MyPSTs-1.zip

:quit</code>

Notes:

a) My PST files are stored in C:\Data\EMail.  Anywhere that you see "C:\Data\EMail" you should replace with the folder name where your PST files are stored.

b) I backup my PST files to X:\EMailBackup.  You will need to replace this path with the location where you keep your ZIP file backups.

c) This script keeps the past 3 backups by renaming them out of the way.

d) You must have at least one file in the X:\EMailBackup folder in order for the backup to run the first time.  After that, the script will work properly.

e) If you find that ZIP is too slow, you may wish to change the "-u9" to "-u1" in order to get faster compression (but less compression).

f) I'm pretty sure the above script is foolproof and correct, but as always you should have a good backup before you attempt things like this.

4) Create a shortcut link to "backupemail.cmd" and place it in your Programs -&gt; Startup folder.  That way it will run as soon as you login.
