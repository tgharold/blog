---
layout: post
title: 'SubVersion for Linux Administrators'
date: '2006-06-14T21:23:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Updated: 26 Aug 2006

I *think* I have this figured out.  After banging my head against the wall for a few months, I finally figured out how to put my /etc configuration folder (and config files) into SubVersion so that I have version control over them.

<b>Assumptions:</b>
<ol>

<li>You need to have SubVersion 1.2 or 1.3 (or later) installed

</li>
<li>You have a folder called /var/svn where you keep your repositories

</li>
<li>I'm assuming that you've su'd to the root account

</li>
<li>Make sure you have a clean system (run etc-update first)

</li>
</ol>

I think that's the only requirements.

<b>Step #1 - Create the repository</b>

The name of the repository can be anything you want.  I tend to name it after the machine name (but you could use the name "system", "config", "admin" or anything else).  In this particular case, I'm setting it up on a machine called "nogitsune" which is my Gentoo AMD64 system.

Creating the repository is easy:

```
# svnadmin create /var/svn/nogitsune
```

Replace "nogitsune" with the preferred name of your repository.  I'd suggest keeping the name as short as possible in case you have to type it by hand later (i.e. "nogitsune", "copper", "alpha", "san1pri", "xen-athens").

<b>Step #2 - Checkout the repository to the root folder</b>

```
nogitsune etc # cd /
nogitsune / # svn co file:///var/svn/nogitsune .
Checked out revision 0.
nogitsune / # svn status
?      media
?      lib64
?      tgh
?      root
?      home
?      var
?      lost+found
?      software
?      sbin
?      mnt
?      tmp
?      opt
?      boot
?      proc
?      backup
?      lib
?      bin
?      usr
?      lib32
?      etc
?      dev
?      sys
nogitsune / # 
```

As long as the "svn status" command returns something like the above, we know that we've connected properly to the SubVersion repository.  You can also look for the ".svn" directory in the root.

```
nogitsune / # ls -la .svn
total 40
drwxr-xr-x   7 root root 4096 Jun 14 21:28 .
drwxr-xr-x  24 root root 4096 Jun 14 21:28 ..
-r--r--r--   1 root root  118 Jun 14 21:28 README.txt
-r--r--r--   1 root root    0 Jun 14 21:28 empty-file
-r--r--r--   1 root root  283 Jun 14 21:28 entries
-r--r--r--   1 root root    2 Jun 14 21:28 format
drwxr-xr-x   2 root root 4096 Jun 14 21:28 prop-base
drwxr-xr-x   2 root root 4096 Jun 14 21:28 props
drwxr-xr-x   2 root root 4096 Jun 14 21:28 text-base
drwxr-xr-x   6 root root 4096 Jun 14 21:28 tmp
drwxr-xr-x   2 root root 4096 Jun 14 21:28 wcprops
nogitsune / # cat .svn/entries
<?xml version="1.0" encoding="utf-8"?>
<wc-entries></wc-entries>   xmlns="svn:">
<entry></entry>   committed-rev="0"
   name=""
   committed-date="2006-06-15T01:26:51.238552Z"
   url="file:///var/svn/nogitsune"
   kind="dir"
   uuid="21f0cb31-3916-0410-ae38-e44852334012"
   revision="0"/>

nogitsune / #
```

<b>Step #3 - Adding directories and files to SubVersion</b>

It's important to understand a little bit how "svn add" and "svn commit" work hand-in-hand.  Just because we've issued the "svn add" command does not mean that our changes have been pushed to the repository.  That requires using the "svn commit" command.

For the first example, I'm going to push the contents of /boot into the Subversion repository.

```
nogitsune / # mount /boot
nogitsune / # ls -la /boot
total 41261
drwxr-xr-x   4 root root    2048 Nov 29  2005 .
drwxr-xr-x  24 root root    4096 Jun 14 21:28 ..
-rw-r--r--   1 root root       0 Jul 27  2005 .keep
-rw-r--r--   1 root root  917680 Nov 12  2005 System.map-2.6.13-12Nov2005
-rw-r--r--   1 root root  910027 Nov 12  2005 System.map-2.6.13-12Nov2005-2300
-rw-r--r--   1 root root  910027 Nov 12  2005 System.map-2.6.13-12Nov2005-2330
-rw-r--r--   1 root root  898088 Nov 12  2005 System.map-2.6.13-13Nov2005
-rw-r--r--   1 root root  898098 Nov 13  2005 System.map-2.6.13-13Nov2005-1700
-rw-r--r--   1 root root  917799 Nov 13  2005 System.map-2.6.13-13Nov2005-1810
-rw-r--r--   1 root root  917372 Nov 13  2005 System.map-2.6.13-13Nov2005-1948
-rw-r--r--   1 root root  837348 Nov 14  2005 System.map-2.6.13-14Nov2005-1500
-rw-r--r--   1 root root  918716 Nov 14  2005 System.map-2.6.13-14Nov2005-1600
-rw-r--r--   1 root root  846033 Nov 21  2005 System.map-2.6.13-21Nov2005-2300
-rw-r--r--   1 root root  888601 Nov 22  2005 System.map-2.6.13-22Nov2005-0030
-rw-r--r--   1 root root  890145 Nov 29  2005 System.map-2.6.13-29Nov2005-2148
-rw-r--r--   1 root root  916779 Nov  8  2005 System.map-2.6.13-8Nov2005
-rw-r--r--   1 root root  919480 Nov  9  2005 System.map-2.6.13-9Nov2005
lrwxrwxrwx   1 root root       1 Nov  8  2005 boot -> .
-rw-r--r--   1 root root   23975 Nov 12  2005 config-2.6.13-12Nov2005
-rw-r--r--   1 root root   23749 Nov 12  2005 config-2.6.13-12Nov2005-2300
-rw-r--r--   1 root root   23738 Nov 12  2005 config-2.6.13-12Nov2005-2330
-rw-r--r--   1 root root   23782 Nov 12  2005 config-2.6.13-13Nov2005
-rw-r--r--   1 root root   23197 Nov 13  2005 config-2.6.13-13Nov2005-1700
-rw-r--r--   1 root root   24091 Nov 13  2005 config-2.6.13-13Nov2005-1810
-rw-r--r--   1 root root   24106 Nov 13  2005 config-2.6.13-13Nov2005-1948
-rw-r--r--   1 root root   22579 Nov 14  2005 config-2.6.13-14Nov2005-1500
-rw-r--r--   1 root root   23986 Nov 14  2005 config-2.6.13-14Nov2005-1600
-rw-r--r--   1 root root   23084 Nov 21  2005 config-2.6.13-21Nov2005-2300
-rw-r--r--   1 root root   23427 Nov 22  2005 config-2.6.13-22Nov2005-0030
-rw-r--r--   1 root root   23416 Nov 29  2005 config-2.6.13-29Nov2005-2148
-rw-r--r--   1 root root   23986 Nov  8  2005 config-2.6.13-8Nov2005
-rw-r--r--   1 root root   23964 Nov  9  2005 config-2.6.13-9Nov2005
drwxr-xr-x   2 root root    1024 Nov  9  2005 grub
-rw-r--r--   1 root root 2139460 Nov 12  2005 kernel-2.6.13-12Nov2005
-rw-r--r--   1 root root 2081829 Nov 12  2005 kernel-2.6.13-12Nov2005-2300
-rw-r--r--   1 root root 2081802 Nov 12  2005 kernel-2.6.13-12Nov2005-2330
-rw-r--r--   1 root root 2056584 Nov 12  2005 kernel-2.6.13-13Nov2005
-rw-r--r--   1 root root 2064792 Nov 13  2005 kernel-2.6.13-13Nov2005-1700
-rw-r--r--   1 root root 2105823 Nov 13  2005 kernel-2.6.13-13Nov2005-1810
-rw-r--r--   1 root root 2099454 Nov 13  2005 kernel-2.6.13-13Nov2005-1948
-rw-r--r--   1 root root 1958868 Nov 14  2005 kernel-2.6.13-14Nov2005-1500
-rw-r--r--   1 root root 2142469 Nov 14  2005 kernel-2.6.13-14Nov2005-1600
-rw-r--r--   1 root root 2008155 Nov 21  2005 kernel-2.6.13-21Nov2005-2300
-rw-r--r--   1 root root 2017013 Nov 22  2005 kernel-2.6.13-22Nov2005-0030
-rw-r--r--   1 root root 2024425 Nov 29  2005 kernel-2.6.13-29Nov2005-2148
-rw-r--r--   1 root root 2139807 Nov  8  2005 kernel-2.6.13-8Nov2005
-rw-r--r--   1 root root 2151371 Nov  9  2005 kernel-2.6.13-9Nov2005
drwx------   2 root root   12288 Nov  8  2005 lost+found
nogitsune / # svn add -N boot
A         boot
nogitsune / # cd boot
nogitsune boot # ls -la .svn
total 11
drwxr-xr-x  7 root root 1024 Jun 14 21:33 .
drwxr-xr-x  5 root root 2048 Jun 14 21:33 ..
-r--r--r--  1 root root  118 Jun 14 21:33 README.txt
-r--r--r--  1 root root    0 Jun 14 21:33 empty-file
-r--r--r--  1 root root  190 Jun 14 21:33 entries
-r--r--r--  1 root root    2 Jun 14 21:33 format
drwxr-xr-x  2 root root 1024 Jun 14 21:33 prop-base
drwxr-xr-x  2 root root 1024 Jun 14 21:33 props
drwxr-xr-x  2 root root 1024 Jun 14 21:33 text-base
drwxr-xr-x  6 root root 1024 Jun 14 21:33 tmp
drwxr-xr-x  2 root root 1024 Jun 14 21:33 wcprops
nogitsune boot # svn add .keep System* config* kernel* grub boot
A         .keep
A         System.map-2.6.17-25Aug2006-2300
A         config-2.6.17-25Aug2006-2300
A  (bin)  kernel-2.6.17-25Aug2006-2300
A         grub
A         grub/menu.lst
A  (bin)  grub/splash.xpm.gz
A         grub/grub.conf.sample
A  (bin)  grub/e2fs_stage1_5
A  (bin)  grub/fat_stage1_5
A  (bin)  grub/ffs_stage1_5
A  (bin)  grub/iso9660_stage1_5
A  (bin)  grub/jfs_stage1_5
A  (bin)  grub/minix_stage1_5
A  (bin)  grub/reiserfs_stage1_5
A  (bin)  grub/stage1
A  (bin)  grub/stage2
A  (bin)  grub/stage2_eltorito
A  (bin)  grub/ufs2_stage1_5
A  (bin)  grub/vstafs_stage1_5
A  (bin)  grub/xfs_stage1_5
A         grub/grub.conf
A         boot
nogitsune boot # svn status
?      boot
?      lost+found
A      .
A      grub
A      grub/grub.conf
A      grub/stage1
A      grub/stage2
A      grub/e2fs_stage1_5
A      grub/xfs_stage1_5
A      grub/vstafs_stage1_5
A      grub/fat_stage1_5
A      grub/grub.conf.sample
A      grub/menu.lst
A      grub/ffs_stage1_5
A      grub/stage2_eltorito
A      grub/iso9660_stage1_5
A      grub/ufs2_stage1_5
A      grub/jfs_stage1_5
A      grub/reiserfs_stage1_5
A      grub/minix_stage1_5
A      grub/splash.xpm.gz
A      .keep
A      System.map-2.6.17-25Aug2006-2300
A      kernel-2.6.17-25Aug2006-2300
A      config-2.6.17-25Aug2006-2300
nogitsune boot # cd /
nogitsune / # svn commit -m "Initial snapshot of /boot"
Adding         boot
Adding         boot/.keep
Adding         boot/System.map-2.6.17-25Aug2006-2300
Adding         boot/boot
Adding         boot/config-2.6.17-25Aug2006-2300
Adding         boot/grub
Adding  (bin)  boot/grub/e2fs_stage1_5
Adding  (bin)  boot/grub/fat_stage1_5
Adding  (bin)  boot/grub/ffs_stage1_5
Adding         boot/grub/grub.conf
Adding         boot/grub/grub.conf.sample
Adding  (bin)  boot/grub/iso9660_stage1_5
Adding  (bin)  boot/grub/jfs_stage1_5
Adding         boot/grub/menu.lst
Adding  (bin)  boot/grub/minix_stage1_5
Adding  (bin)  boot/grub/reiserfs_stage1_5
Adding  (bin)  boot/grub/splash.xpm.gz
Adding  (bin)  boot/grub/stage1
Adding  (bin)  boot/grub/stage2
Adding  (bin)  boot/grub/stage2_eltorito
Adding  (bin)  boot/grub/ufs2_stage1_5
Adding  (bin)  boot/grub/vstafs_stage1_5
Adding  (bin)  boot/grub/xfs_stage1_5
Adding  (bin)  boot/kernel-2.6.17-25Aug2006-2300
Transmitting file data ......................
Committed revision 1.
nogitsune / # 
```

Most of that should be self explanatory.  You can see that I use "svn add -N boot" from the / (root) directory to add the /boot directory, then I move into the /boot folder and issue a selective "svn add".  Pay attention to the "-N" option which prevents the add from recursing down through subdirectories.  You should also take care to only add files that you control as an administrator to the svn repository (avoid adding things like "lost+found" or "._cfg*" files).

If you want to version control something that is 3 levels deep, you need to "svn add -N foldername" for each level in the tree until you get deep enough to add the file.  It might be possible to do it faster in one command, but I'm still learning SubVersion.

For the second example, I'm going to add everything in /etc to SubVersion.

```
# cd /
# svn add -N etc
# cd etc
# svn add *
# svn commit -m "Initial snapshot of /etc"
```

That's the basics.  For the third example, I'll show how to add custom scripts stored in /usr/local/sbin.

```
# cd /
# svn add -N usr ; cd usr
# svn add -N local ; cd local
# svn add -N sbin ; cd sbin
# svn add *
# cd /
# svn commit -m "Initial snapshot of /usr/local/sbin"
```

<b>Step #4 - Creating a cron job to backup your SubVersion repositories</b>

On my systems, I create a folder called /backup which is a separate set of spindles that I mount for quick backups.  Under that folder, I create a sub-folder called "subversion".

```
# ls -l /backup/subversion
total 96
-rw-r--r--  1 root root 20 Nov 30  2005 dev.svnadmin.dump.2005.11.gz
-rw-r--r--  1 root root 20 Dec 31 02:00 dev.svnadmin.dump.2005.12.gz
-rw-r--r--  1 root root 20 Jan 31 02:00 dev.svnadmin.dump.2006.01.gz
-rw-r--r--  1 root root 20 Feb 28 02:00 dev.svnadmin.dump.2006.02.gz
-rw-r--r--  1 root root 20 Mar 31 02:00 dev.svnadmin.dump.2006.03.gz
-rw-r--r--  1 root root 20 Apr 30 02:00 dev.svnadmin.dump.2006.04.gz
-rw-r--r--  1 root root 20 May 31 02:00 dev.svnadmin.dump.2006.05.gz
-rw-r--r--  1 root root 20 Jun 14 02:00 dev.svnadmin.dump.2006.06.gz
-rw-r--r--  1 root root 20 Nov 30  2005 photo.svnadmin.dump.2005.11.gz
-rw-r--r--  1 root root 20 Dec 31 02:00 photo.svnadmin.dump.2005.12.gz
-rw-r--r--  1 root root 20 Jan 31 02:00 photo.svnadmin.dump.2006.01.gz
-rw-r--r--  1 root root 20 Feb 28 02:00 photo.svnadmin.dump.2006.02.gz
-rw-r--r--  1 root root 20 Mar 31 02:00 photo.svnadmin.dump.2006.03.gz
-rw-r--r--  1 root root 20 Apr 30 02:00 photo.svnadmin.dump.2006.04.gz
-rw-r--r--  1 root root 20 May 31 02:00 photo.svnadmin.dump.2006.05.gz
-rw-r--r--  1 root root 20 Jun 14 02:00 photo.svnadmin.dump.2006.06.gz
-rw-r--r--  1 root root 20 Nov 30  2005 web.svnadmin.dump.2005.11.gz
-rw-r--r--  1 root root 20 Dec 31 02:00 web.svnadmin.dump.2005.12.gz
-rw-r--r--  1 root root 20 Jan 31 02:00 web.svnadmin.dump.2006.01.gz
-rw-r--r--  1 root root 20 Feb 28 02:00 web.svnadmin.dump.2006.02.gz
-rw-r--r--  1 root root 20 Mar 31 02:00 web.svnadmin.dump.2006.03.gz
-rw-r--r--  1 root root 20 Apr 30 02:00 web.svnadmin.dump.2006.04.gz
-rw-r--r--  1 root root 20 May 31 02:00 web.svnadmin.dump.2006.05.gz
-rw-r--r--  1 root root 20 Jun 14 02:00 web.svnadmin.dump.2006.06.gz
```

As you can see from my backup folder, I have 3 repositories being backed up (dev, photo, web) and I rotate to a new backup filename every month.  It's not ideal because a bad backup could cause me to lose up to 30 days of work, but it meets my needs.  More risk-adverse admins may want to switch to a new backup file on a daily basis.

To create this backup, I use the following script:

```
nogitsune / # cd /usr/local/sbin
nogitsune sbin # ls -l svndaily.sh
-rwxr-xr-x  1 root root 646 Nov 27  2005 svndaily.sh
nogitsune sbin # cat svndaily.sh
#!/bin/sh
# backup subversion repositories to /backup/subversion/filename.year.month.gz
# notice the use of the backtick character (`) instead of single-quote character (')
# overwrites the backup file every day

BACKUPDATE=`date +%Y.%m`
#echo $BACKUPDATE

# svnadmin dump /var/svn/reponame | gzip -c > /backup/subversion/reponame.svnadmin.dump.${BACKUPDATE}.gz
svnadmin dump /var/svn/dev | gzip -c > /backup/subversion/dev.svnadmin.dump.${BACKUPDATE}.gz
svnadmin dump /var/svn/photo | gzip -c > /backup/subversion/photo.svnadmin.dump.${BACKUPDATE}.gz
svnadmin dump /var/svn/web | gzip -c > /backup/subversion/web.svnadmin.dump.${BACKUPDATE}.gz

nogitsune sbin #
```

Note: Each of the "svnadmin dump" lines should be all on one line and not split across two lines.

As far as I know, svndump is adequate to the task of backing up SubVersion repositories.
