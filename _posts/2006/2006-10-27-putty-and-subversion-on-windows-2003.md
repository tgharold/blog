---
layout: post
title: 'PuTTY and SubVersion on Windows 2003'
date: '2006-10-27T20:04:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


One thing we use SubVersion for in the office is for tracking configuration changes to our Linux servers.  Everything under /etc or any other file that we change by hand (or with configuration tools) gets put into SVN which tracks the changes.  It's possible to do the same thing under Windows (although not everything can be tracked).

A) Install PuTTY on the Win2003 server

1. The usual defaults are fine (install to C:\Program Files\PuTTY)

2. Create a public key (RSA, 2048 bit, no passphrase) and save it somewhere on the Windows 2003 server hard drive.  I'd recommend an easy-to-type location because you'll be referencing constantly in batch files.

<b>Security implications:</b>

- Make sure that the account on the SVN server is a limited account, maybe even with a restricted shell.  Just in case the authorized_keys file restriction is ever removed by accident.

- Setting the authorized_keys file to only allow "svnserve -t" as a command will keep most attackers from gaining console access to the server.  But you're relying on the security of the svnserver application to not have an buffer/overflow exploits that allow shell access.

- Our decision was that the public key on the Win2003 server did not need a passphrase.  The risks are worth it in order to be able to script svn commands to shove log files across the wire to the central SVN server every hour.

3. Upload the public key to your SVN server, configure it in the authorized_keys file and restrict it to only allowing command="svnserve -t".

```
# su accountname
# cd /home/accountname
# mkdir .ssh
# chmod 700 .ssh
# cd .ssh
# cat > machinename@svn.pub
(paste in PuTTY key)
# ssh-keygen -i -f machinename@svn.pub >> authorized_keys
# vi authorized_keys
(add command="svnserve -t" to the front of the new key line)
# chmod 600 *
```

4. Fire up PuTTY and attempt to connect to your SVN server.  That will cache the server's public key in PuTTY's records.

B) Install the SubVersion Win32 command-line client on the server.

1. Install SVN to the default location

2. Right-click on My Computer, Properties, Advanced, Environment Variables

3. Under System Variables, click "New":
Variable name: SVN_ASP_DOT_NET_HACK
Variable value (can be anything at all): _svn

4. Under System Variables, highlight "PATH" and click "Edit".  Add ";C:\Program Files\PuTTY" to the end of the PATH statement (which assumes you installed PuTTY to that location)

5. Under User Variables, click "New":
Variable name: SVN_SSH

```
plink -ssh -l user -pw password
- "user" should be your username on the SVN server
- the "-pw password" is optional if you did not put a passphrase on your key
```

C) Add the base set of directories to the server.

1. Check connectivity to the SVN server

```
C:\ svn list svn+ssh://user@svn.example.com/var/svn/repos
```

(if that doesn't work, go back and verify SSH connectivity)

2. Create a "C" folder in the root of the repository to represent your "C" drive.  I usually do it on another system in a temporary folder.

3. Do the default checkout to the root of C: and D:

    C:\ svn co svn+ssh://user@svn.example.com/var/svn/repos/C .
    D:\ svn co svn+ssh://user@svn.example.com/var/svn/repos/D .
    (note the "." at the end of the command)

4. Start adding folders and files to the SVN repository.

    C:\ svn add -N Data
    C:\ svn add -N Data\Logs
    C:\ svn ci -m "log folder"
