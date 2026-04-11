---
layout: post
title: 'Getting started with GPG4Win'
date: '2006-06-12T10:47:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---



[EMail-Security using GnuPG for Windows](http://www.gpg4win.org/) - GPG4Win offers better integration of GnuPG into Windows them past products (such as using WinPT with the command-line version of GnuPG).  That means that the user experience is a lot nicer and it doesn't seem as clunky.

You can [download GPG4Win here](http://www.gpg4win.org/download.html).  The current version is: 1.0.2

Notes:
<ul>

<li>GPGol (the MS Outlook plugin) only works with Microsoft Outlook 2003 (or later?), so if you are using older versions of MSOutlook be sure to *not* install this

</li>
<li>You probably won't need to install Sylpheed-Claws either, unless you are looking for a new e-mail program

</li>
<li>I prefer WinPT over GPA, but your tastes may be different

</li>
</ul>

Installation:
<ol>

<li>Download and run the gpg4win-1.0.2.exe file

</li>
<li>When you reach the "Choose Components" screen, you should deselect GPGol, GPA and Sypheed.  And unless you speak German, you should deselect the Novice Manual and Advanced Manual components.  So for most users you will only be installing: GnuPG, WinPT and GPGee.

</li>
<li>Click "Next" and proceed.

</li>
<li>At the "Install Options", I recommend only installing links to the "Start Menu" (and not the Desktop or Quick Launch bar).

</li>
<li>Finally, proceed forward (using the "Next") button until you reach the "Install" button.

</li>
<li>Clicking on "Install" will begin the installation.

</li>
<li>After installation finishes, you can click on "Next" and "Finish" to exit the installation wizard.

</li>
</ol>

Getting started
<ol>

<li>Go to "Start" --&gt; "Programs" --&gt; GnuPG for Windows --&gt; WinPT

</li>
<li>That will start the WinPT application.

</li>
<li>If you have pre-existing GnuPG keyrings, you should probably select the import option (Copy GnuPG keyrings from another location).  But you can also import existing keys at a later time.

</li>
<li>For now, we will create a GnuPG key pair

</li>
<li>Click on the "Expert" button

</li>
<li>Key type: DSA and ELG (default)

</li>
<li>Subkey size in bits: 2048 (you may wish to use 3072 or 4096)

</li>
<li>Real name: (enter the name that you wish to associate with this key)  This name will appear alongside your key on public keyservers.

</li>
<li>Comment (optional): (typically a company name)  Note that <b>comments are public information</b> and will appear alongside your key on the keyserver.  Most people put their company name in this field, while others enter their website address (i.e. "www.tgharold.com").

</li>
<li>Email address: (enter the e-mail address associated with the key) Again, this is public information that will be on the keyservers to allow people to find your public key.

</li>
<li>Expire Date: <b>Uncheck</b> "Never" and enter an expiration date of a few years (I'd recommend 2 or 3 years).

</li>
<li>Click the "Start" button

</li>
<li>Enter the passphrase that you wish to use when protecting this key.  I would recommend a rather strong one made up of numerous randomly picked words, letters, numbers and symbols.  I will talk about protecting this passphrase later on.

</li>
<li>Repeat your passphrase in the new window.  This is done to ensure that you didn't mistype it the first time.

</li>
<li>The progress dialog will now appear as GnuPG creates the keys for you.  This can take a while as GnuPG needs to obtain random data from the system.  You can speed the process up by typing nonsense into a document and moving the mouse in an erratic manner.

</li>
<li>When GnuPG finishes, it will pop up a window that says "Key Generation Completed"

</li>
<li>You will be offered the chance to backup your keyring.  Click "Yes" and choose a location.  I would recommend a USB key or a floppy disk as a backup target.

</li>
<li>The key has been created and is now listed in the WinPT Key Manager

</li>
</ol>

Configuring WinPT Options
<ol>

<li>Right-click on the WinPT icon in the System Tray

</li>
<li>Select Preferences --&gt; WinPT

</li>
<li>Any options that I do not mention are optional and can be set to anything you desire.  (Meaning that I don't have a specific recommendation for that option.)

</li>
<li>CHECK - Do not use any temporary files

</li>
<li>CHECK - Use clipboard viewer to display the plaintext

</li>
<li>Cache passphrase for N minutes should be set to a value that you are comfortable with.  If you set your machine to automatically lock after 5 minutes, you could cache the passphrase for longer.  But if you don't automatically lock your workstation whenever you are away from the machine you should choose a shorter timeout period.  

</li>
<li>CHECK - Automatic keyring backup

</li>
<li>SELECT "Backup to" and choose a folder location that is on a drive other then C: (such as a USB key drive or a TrueCrypt volume)

</li>
</ol>

Configuring GnuPG Options
<ol>

<li>Right-click on the WinPT icon in the System Tray

</li>
<li>Select Preferences --&gt; GPG

</li>
<li>There's nothing in particular that I feel needs to be changed here, but it does let you add a comment line for ASCII armored files.

</li>
</ol>

Importing old keys into WinPT
<ol>

<li>Right-click on the WinPT icon in the System Tray

</li>
<li>Select "Key Manager"

</li>
<li>Under the "Key" menu, select "Import"

</li>
<li>Browse to your old secring.gpg file

</li>
<li>Highlight the keys that you want to import and click "Import"

</li>
<li>For each key that you've imported, you will need to set the "trust" level of the key.  Note that you can only set "owner/trust" values for keys that have not expired (see the "Validity" column in the key manager).

</li>
<li>Right-click the key and choose "Properties"

</li>
<li>If you are able to change the trust level, the "Change" button next to the "Ownertrust" field will be enabled.  Click on "Change" and set your trust level for a particular key.

</li>
<li>Note: Trust values are important.  Never set a trust level higher then you feel comfortable with.  Verify that you have the right key and that you have validated the fingerprint of the key through a secure channel.

</li>
<li>2nd Note: WinPT does sometimes crash after importing large quantities of keys.  And you sometimes have to exit the Key Manager before you can see newly imported keys.

</li>
</ol>

Final notes:
<ul>

<li>I would recommend not using the "encrypt current window" functionality of WinPT.  It is not working properly for me at the moment.  However, the encrypt/decrypt clipboard functionality works fine.

</li>
<li>Make sure that you backup your secret key files

</li>
</ul>

Backing up your secret key and passphrase on paper
<ol>

<li>In the WinPT Key Manager, highlight your key

</li>
<li>From the menu, choose "Key" then "Export Secret Key"

</li>
<li>Export this key to a secure location (such as a USB key drive, a floppy disk, or a encrypted volume / folder)

</li>
<li>Open the .ASC file in Notepad

</li>
<li>Change the font size using "Format, Font...".  I would suggest a font of "Courier New" in a 11 or 12 point font.

</li>
<li>Print out a copy of your private key block.  That way, in a worst-case scenario, you could hand-enter (or OCR) it back into a new machine.

</li>
<li>Jot a note to yourself at the bottom of the page to remind yourself what the passphrase is for this secret key.  You may wish to be explicit or simply leave yourself vague hints.

</li>
<li>Fold the paper up and place it into a "security" envelope.  Security envelopes have printing on the inside of the envelope which is designed to prevent the contents of the letter from being read without opening the envelope.  For additional security, you may wish to wrap a 2nd sheet of paper around your original sheet.

</li>
<li>You may also include the floppy diskette containing the secret key inside of the envelope.

</li>
<li>Seal the envelope

</li>
<li>Write something memorable (signature, today's date, a song that is playing on the radio) along the sealed flap.  That will give you a chance to detect tampering if the attacker does not reseal the envelope in a way that the markings still line up.

</li>
<li>For additional security, place clear tape over the flap edge (and over your writing).  That makes it more difficult to open without destroying your writing.

</li>
<li>Jot a note to yourself on the outside of the envelope (today's date, the e-mail address of the key)

</li>
<li>Place the envelope in a secure location (such as a bank vault, document safe), preferably at a location that is physically distant from your computer.  You should keep this envelope as secure as you would your will or other important financial papers.

</li>
</ol>
