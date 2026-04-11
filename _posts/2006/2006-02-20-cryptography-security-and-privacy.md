---
layout: post
title: 'Cryptography, Security and Privacy'
date: '2006-02-20T15:24:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---



[infoAnarchy Wiki](http://www.infoanarchy.org/wiki/index.php/Main_Page)

[Eraser - File Wipe Tool](http://www.heidi.ie/eraser/) (Note: I would recommend not using the new 5.8 beta until all the bugs are worked out.)

[Wikipedia - File Wiping](http://en.wikipedia.org/wiki/File_wipe)

Also, the GnuPG folks have upgraded their tools to be a little more integrated with Windows.  See [GPG4Win](http://www.gpg4win.org/) which includes WinPT, GPG and a few other tools collected into an easy to use and easy to install package.  It's a lot nicer then the old system where WinPT called the commandline version of GnuPG.

...

Encryption 101

TrueCrypt - allows you to create "virtual" hard drives where the contents are fully encrypted.  The simplest method is to create a virtual drive as a file on a hard drive.  This file is then mounted and assigned to a drive letter.  Once mounted, applications can use it just like any other drive with no compatibility issues.  These drives are typically protected by pass phrases that you type in to mount the drive.  Virtual drives can be configured to automatically dismount after a period if inactivity.

GPG4Win - e-mail / clipboard / file encryption.  Requires the creation of a public/private keypair.  The public key can be published and does not need to be kept secret at all (in fact, it's most useful when public).  The private key needs to be kept secure and protected with a strong passphrase.  Items encrypted with the public key can only be decrypted with the private key.  For e-mail, someone would encrypt the contents of the e-mail with your private key, send it to you with the assurances that only you can decrypt the contents of the message (using your private key).  In addition, messages can be encrypted with multiple public keys allowing them to be decrypted by any of the matching private keys (one message, multiple recipients).  Individual files can also be encrypted by GPG/PGP, but must be decrypted before use.

Windows EFS (Encrypting File System) - A component of Windows 2000 / Windows XP.  It allows you to flag individual folders or files on a hard drive for encryption on-the-fly.  This allows you to work with encrypted files without having to manually decrypt/re-encrypt them.  The downside is that it's difficult to backup the EFS keys, the keys can be compromised easily, and if the host O/S dies or is reinstalled you will lose access to the files.  Mostly useful as a slight speedbump or in cases where you are concerned about data being left on a dead hard drive after it fails.  Data kept safe using EFS must be backed up regularly (such as copying it to a TrueCrypt volume) in order to avoid data loss.

...

Practical uses:

A) Encrypted USB backup drive.  I have a USB hard drive hooked up to my laptop.  This drive contains a single TrueCrypt volume that I mount at login and use as a backup target every few hours.  So if the laptop dies, I just install TrueCrypt on the new laptop/hard drive, mount the backup drive, and I can restore my data.  But I don't have to worry about anyone else getting at the data and restoring it.

B) Encrypted volume on my laptop's hard drive.  I have financial data stored on my laptop (since it's my primary machine).  Needless to say, if someone were to steal my laptop, I worry greatly about their access to that information.  So I have a TrueCrypt volume file in the root of my C: (C:\Personal.tc) that I mount to a drive letter whenever I need to access my financial records.  In order to keep this data safe, I periodically copy the TC file to another drive or to CD-R.
