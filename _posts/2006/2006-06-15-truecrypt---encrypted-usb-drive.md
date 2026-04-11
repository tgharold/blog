---
layout: post
title: 'TrueCrypt - Encrypted USB Drive'
date: '2006-06-15T10:36:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


TrueCrypt comes in handy for securing external USB or Firewire drives.  Especially when those drives are used for backups of sensitive files or if you are going to ship the drives from point A to point B.  Or even if you are worried about someone swiping the drive and mounting it on another workstation to access files that you have stored there.

Plus, as long as you know the passphrase and/or have the keyfiles used to decrypt the volume, you can move the USB device from workstation to workstation without losing access to the content.

A. right-click on My Computer, choose "Manage"
<ol>

<li>Under "Storage", go to "Disk Management"

</li>
<li>Find the USB drive that you wish to convert to TrueCrypt (note that this will <b>DESTROY</b> all data on the USB drive)

</li>
<li>Remove any existing partitions / drive letters assigned to the USB drive.

</li>
</ol>

B. Create the new partition on the USB drive
<ol>

<li>Right-click, New Partition

</li>
<li>Create a "Primary" partition

</li>
<li>Use the entire drive (or only part of the drive if you wish)

</li>
<li>Do not assign a drive letter

</li>
<li>Do not format the partition

</li>
<li>Click "Finish", note the "Disk #"

</li>
</ol>

C. Create the TrueCrypt drive on the partition
<ol>

<li>Open up TrueCrypt, click on "Create Volume"

</li>
<li>Create a standard TrueCrypt volume

</li>
<li>Click on "Select Device" and choose the empty USB disk and partition

</li>
<li>Double-check that you've selected the correct device

</li>
<li>Encryption algorithm: AES, Hash: RIPEMD-160

</li>
<li>Size cannot be adjusted

</li>
<li>Enter your passphrase twice

</li>
<li>Begin the format (NTFS for anything over a few gigabytes)

</li>
</ol>

Once the partition has been formatted with TrueCrypt you can then return to the TrueCrypt window and mount the drive to a drive letter.  If this drive is always connected to the system you may wish to mount it upon login by making it a "favorite" volume in TrueCrypt.
