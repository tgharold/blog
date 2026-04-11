---
layout: post
title: 'SSH authorized_keys (creating pub keys using SecureCRT)'
date: '2006-12-13T19:15:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


For optimal security, it's better to require public keys for logging into a server rather then allowing password authentication.  As long as the user's keep their SSH private key files safe (along with protecting them with a decent passphrase), you're less likely to encounter a break-in of your Unix/Linux servers.

The process is similar for PuTTY, but SecureCRT offers a much cleaner interface then PuTTY.  Because of the way things work in SSH2-land, you typically create the SSH2 keys using the client software in Windows, then copy the public key up to your user directory on the server that it will be used for.  (Or you have an admin install the public key for you.)

Note #1: One advantage of public keys is that SecureCRT runs a key-agent in the background.  So for additional connections to the same server, you will not be re-prompted for a password.  This will allow you somewhat seamless movement between the 4 Solaris servers.

Note #2: You can use a particular key file for multiple servers.  You should do this as little as possible, because if an attacker swipes your private keyfile and passphrase, they can impersonate you on those servers.  My recommendation for users is that they create a "super-secure" key and a "less-secure" key.  The super-secure key should be used with critical servers and the less-secure key can be used for other servers.

<b>Steps to create a public key pair in SecureCRT</b>

1) Options -> Global Options -> SSH2.

Alternately, to create a session specific key (a better method).

a) Click on the Connect button, highlight the Session for which you want to create a session key and choose Properties.

b) Connection -> Authentication -> Primary -> PublicKey -> Properties

2) Under "Public Key", choose "Use Identify File".  This file is the central storage location for all of your public/private SSH2 keys.  It should be placed somewhere secure and backed up frequently.  Your "My Documents" folder is probably a good place.

3) Click "Create Identify File"

4) Key type can be either RSA or DSA (doesn't matter except for older systems like Solaris).

5) The passphrase should be something you can remember.  It will be used to encrypt your private key.  The comment should probably be of the form "user@servername", although there are no strict requirements for what you place in the comment.

6) A key length of 1024 bits is fine.  On more modern hardware, key length of 2048 bits can be used.  DSA keys can only be 1024 bits.  Given recent developments in the world of encryption, it may be better to use 2048 bit RSA keys.

7) Choose a directory for the private key.  It should also be somewhere safe and part of your regular backups.  A location like "C:\SSHKeys" or placing the key files in your "My Documents" folder, or somewhere under your user profile directories is best.  For even more security, you may wish to place the key files on a removable USB key that you carry around.

8) Send the contents of the "something.pub" key to the server admin so that they can add it to the authorized key file on the servers.  This will look something like:

---- BEGIN SSH2 PUBLIC KEY ----
Subject: Thomas
Comment: "Thomas@Solaris"
AAAAB3NzaC1kc3MAAACBALR3kfLsT5y1c84OCnaFqtp1+tB5QLMVcrY/6GuA7MXq0EP6
c47diCztdSzfvRgUV02uyC6LKKqypvwJeGvt987J1P7e1Mxo1jb5EEYoOyFuL683XK8u
NknA+Oj9l3cJeVhzGczwmTqf6hVCsRih8rxkwewkD4zNc60MeLveAqn9AAAAFQCPqhmR
ElRW4OaotTrU9Wf4JmQYYQAAAIEAsWeirEUPzurmsBzY4nEQ19bQQGuTedeps9EgzN6q
ocS4AEtyBotTMgMTlRIf/rrrRCt6W58fjrHIrMlgljBbopaPrHsdO0v9+iqNRkjAFCIE
kbhiTJHri81MNoQADj7gnN+jsOc0GfOIha+6p0ocnkU07v5HyvUH1C+qA+zvC0oAAACA
No2vpbOp/HpTeeq+guOccJaTmJy8WH7wAtBKewI3WCWSw8ygWtxkOrD9sdIreUeN58G5
eecdUWuxInAnMPmEn4f49sUAejO/0E7P8XKx1Mqx2CUYNOyoQ1EsX5lZXg6Hbx2Gc4BW
1uPFJw13j/9jAfQlRYzAqK80uS/cUwTaH9o=
---- END SSH2 PUBLIC KEY ----

9) Make a backup of your private key and public key files.  One option would be to burn them to CD-R (multiple copies on the disk), write the passphrase on the CD-R, then put it all into a sealed envelope in a secure offsite location (safe-deposit box).  Alternately, you may wish to simply print it out on paper and OCR it back if you lose the key files.
