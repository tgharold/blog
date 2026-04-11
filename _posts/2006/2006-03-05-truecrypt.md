---
layout: post
title: 'TrueCrypt'
date: '2006-03-05T11:17:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


I've been looking for a good disk encryption system for a while.  In the past few years, I've been using PGP's PGPDisk tool with good success, but there have been a few annoyances.

- Difficulty interacting with WindowsXP, drives have to be mounted at bootup or they won't show up after being mounted.  This made it difficult to keep PGP volumes on DVD-R for ad-hoc mounting to refer to information contained within the encrypted disk.

- PGPDisk does not remember how to mount disks at the previously mounted drive letter.  (Something that DriveCrypt did very well.)

- Pricing.  The PGP suite with PGPDisk has gotten more and more expensive over the years.  It used to be available for well under US$100 with no subscription but now costs US$80/yr for each user.  That cost precludes using it for more then a handful of users.

So, with all that in mind, I've been looking at [TrueCrypt](http://www.truecrypt.org/) which is a replacement for the PGPDisk tool.  It offers the same functionality, but is open-source and free.

Note: Disk encryption works in two ways.

1) You create a file on your hard drive that contains a virtual drive.  The PGPDisk / TrueCrypt / DriveCrypt software allows you to mount this file as a drive letter on your system.  Any data inside of that virtual drive is encrypted on the fly.  When the drive is not mounted, the data is safe from prying eyes.

2) You create an encrypted partition on a dedicated hard drive (or a partition on a hard drive).  This is called "whole disk encryption" by some vendors.  It has some advantages over the file-based method but mostly works in an identical manner.

...

So why should someone use disk encryption?  

The easiest scenario to sell is with someone who uses Quicken or MS Money to manage their finances.  This is the primary reason that I started using disk encryption back in 2000.  Since I keep my Quicken program on my laptop, I want to protect my financial data in case the laptop gets stolen.  By storing my Quicken files inside of an encrypted volume that is rarely mounted, a thief who steals the laptop will not have access to those files.

In addition, if the hard drive fails, I don't have to worry about getting it back up and running to wipe the data before getting a replacement.
