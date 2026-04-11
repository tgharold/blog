---
layout: post
title: 'TrueCrypt - Basic Thoughts'
date: '2006-03-09T02:02:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Probably the easiest way to get started with on-the-fly encryption is to create a TrueCrypt volume file and mount that as a Windows drive letter.  The volume file (i.e. "mydrive.tc") can be stored on any hard drive and can be easily backed up as long as the volume is not mounted.  Controlling who can mount a volume can be limited by using either a passphrase and/or a set of "keyfiles".

Once you have created the volume, you can store files inside it (using the mounted volume's drive letter) just like you would store files on any regular hard drive, USB/Firewire drive, or network share.  It's completely invisible to the application.  This makes it ideal for storing application data such as e-mail, financial programs, or other sensitive data.

For starters, I recommend creating a volume file that is protected with only a passphrase.  This file should be small enough to copy off to CD or DVD media as a periodic backup.  The passphrase should be something easy to remember, but difficult to guess.  Punctuation and mixed-case should be part of the passphrase.

Once you have a good passphrase, you should guard against its discovery or loss.  A good way of doing this is to write the passphrase down on an 3x5 index card.  Fold the card in half and place it inside a folded piece of letter-sized paper. Place all of that inside a security envelope (security envelopes have a printed pattern on the interior which is designed to make it difficult to shine light through the envelope to read the contents).  Seal the envelope and write your name or information over the edge of the flap, then place clear packing tape over the flap edge.  Store the envelope in a secure location such as a bank vault or document safe.  You should be reasonably secure against someone opening it up without discovery.

Creating and mounting the volume file:
<ol>

<li>Open up the TrueCrypt window.</li>

<li>Click the "Create Volume" button, this opens up the <b>TrueCrypt Volume Creation Wizard</b>
</li>

<li>Create a <b>standard</b> TrueCrypt volume, click "Next"</li>

<li>Pick a location for your volume file.  I would recommend an easy to locate folder such as C:\ or C:\Data.  Give the file a reasonable name that is not overly specific (i.e. "ZDrive.tc").  You can use a file extension other then ".TC", but a determined attacker will be able to find out which files are TrueCrypt volumes anyway.  Click "next" once you have specified where the volume file will be created.</li>

<li>Choose your encryption and hash algorithms.  The defaults (AES and RIPEMD-160) are generally good enough.  Click "Next" when done.</li>

<li>Enter your volume size.  650MB (CD-sized) or 4050MB (DVD-sized) are good values which allow you to easily backup your volume file to optical media.  You can always create another, larger, volume later and copy your data from the old one to the new one.  Click "Next" when ready.</li>

<li>Enter your passphrase that you picked earlier.  Click "Next" when ready.</li>

<li>Now you are ready to format the encrypted volume.  For smaller volumes (less then 1GB), I would recommend FAT.  Click "Format" when finished.</li>

<li>Click "Exit" to leave the wizard.</li>

</ol>

Now you are ready to mount your new volume:
<ol>

<li>In the "Volume" section at the bottom of the TrueCrypt window, click on the "Select File..." button.</li>

<li>Browse to and select your volume from the list.</li>

<li>Choose an unused drive letter in the upper window.</li>

<li>Click on the "Mount" button.</li>

<li>You will be prompted to enter your passphrase for the volume.</li>

<li>You may now start copying data to your new encrypted volume.</li>

</ol>
