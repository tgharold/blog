---
layout: post
title: 'NTBackup to a disk file'
date: '2005-10-05T19:36:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>
<i>Note: This post may be incomplete...</i>

Sometimes you have to start simple.  For us, after fighting with tape drives and tape drive software, we've switched back to using NTBACKUP that comes with Windows 2000 Server and Windows 2003 Server.  We've also given up on tape drives for the moment since our backup needs have drastically outstripped what the old tape drive is capable of.

(Note to self:  If you're going to use a tape drive to backup your daily files.  Make sure you own (3+) drives of the same make/model that can read tapes from each other.  Make sure at least one of those drives is located at an alternate location and is tested weekly.  You may want to connect up with another local company who is also using the same technology, such as another company in the same building/town.)

Our backup plan for data files has a few goals and is still a work in progress:

1) Easy restoration when a user says "oops".  This means that we need an easy way to restore files that a user has screwed up or accidentally deleted.  Possibly even entire folder trees.  

We handle this primarily through using "Shadow Copies" in Windows 2003 Server with a sizeable shadow cache setup on another drive within the server.  We have roughly 60GB of user data right now, and our cache is 25GB.  Shadows are created twice per day (7am and noon) on Monday-Friday and we're getting around 30 days of retention at the moment.

Our secondary plan for dealing with "oops" issues is the weekly full NTBackup job that is written to a central file server.  We keep 2 sets of those weekly backups on that central server, giving us 7-14 days of "oops" protection.  In addition, since we're backing up to files, we don't have to go scrounging for tapes in order to do a quick file restore.  Daily appends also get written to those weekly snapshot folders.

Our third, down-n-dirty method is a workstation that mirrors all changes to a local drive on a nightly basis.  This isn't very reliable and loses file attributes and security settings.  But it does serve as a last resort in cases where the two primary methods fail.

2) The second goal is off-site storage of backups.  This is made easier by putting all of the weekly snapshots and daily updates onto a central server.  That allows us to collect the latest versions of the .BKF files and quickly move them to a removeable drive.  In addition, the speed of the removable drive matters less because it can be updated after the backup window.  The only issue you'll run into is that Windows has difficulty copying large files, so you will have to dig out the GNU Win32 tools (such as the "cp" command) in order to move these multi-gigabyte files around.

So now for the gory details.  

Our central backup server is called, appropriately enough, "Backup1" with a single share point called "Backups".  Under the backup folder, we have 2 subfolders, one for each week ("Weekly1" and "Weekly2").  This requires creating 2 backup jobs on each server that we want to backup, with the scheduling set to write to the appropriate folder during the proper week.  You could also do some scripting to determine which week to write to, but simpler is better for us.

One trick is to store your backup specification file (.BKS) in a central location and use it for all data backups on that server.  You'll note that our backup specification file is called "Server2-DataFileBackupSpecification.bks" and gets used by all of the jobs on that server that are backing up user data.

Here's our backup command for Week #1:

C:\WINNT\system32\NTBACKUP.EXE backup "@D:\Data\NTBackup\Server2-DataFileBackupSpecification.bks" /n 
"Server2-Weekly1Snapshot" /d "Server2-Weekly1Snapshot" /v:yes /r:no /rs:no /hc:off /m normal /j 
"Server2-Weekly1Snapshot" /l:s /f "\\Domain1\Backups\Weekly1\Server2-WeeklySnapshot.bkf"

And the command for Week #2: 

C:\WINNT\system32\NTBACKUP.EXE backup "@D:\Data\NTBackup\Server2-DataFileBackupSpecification.bks" /n 
"Server2-Weekly2Snapshot" /d "Server2-Weekly2Snapshot" /v:yes /r:no /rs:no /hc:off /m normal /j 
"Server2-Weekly2Snapshot" /l:s /f "\\Domain1\Backups\Weekly2\Server2-WeeklySnapshot.bkf"

Notice that the target filename is identical and the only difference is that you store it in the other folder.  This allows our offsite system to pull the latest file from <b>either</b> folder without any fancy tricks (other then comparing source/target timestamps).

Microsoft reference links:
[Windows 2003 Server - NTBackup Command](http://www.microsoft.com/technet/prodtechnol/windowsserver2003/library/ServerHelp/2b8c47c9-a769-46d2-9e26-f4d16f0261f8.mspx)
[Windows XP - NTBackup Command](http://www.microsoft.com/resources/documentation/windows/xp/all/proddocs/en-us/ntbackup_command.mspx)

That takes care of the weekly snapshots (a full backup that also resets the archive bit).  For our daily updates, we need to set NTBackup to append to those files and only backup files that have changed since the snapshot was taken.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2005.shtml">2005</a>
		<div class="Byline">
			posted by Thomas at 
			[19:36](http://www.tgharold.com/techblog/2005/10/ntbackup-to-disk-file.shtml)

		</div>