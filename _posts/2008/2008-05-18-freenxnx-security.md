---
layout: post
title: 'FreeNX/NX Security'
date: '2008-05-18T18:55:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


After mucking around with NX/FreeNX, I have a general understanding of how it works, how to lock down your server and what some of the security ramifications are.

<b>First line of defense - NX user key pair</b>

NX/FreeNX clients connect to your Linux server using a special user account (always named "nx") via your SSH service.  This user can login using a SSH public/private key pair, which means better security and control over who can attempt to connect to the NX server daemon.   However, the default NX server ships with a pre-defined public key pair, which renders this line of defense useless.

(That statement is based on the freenx.x86_64 package (v0.7) currently available as an RPM.)

The server's key files are located under the following names on CentOS/RedHat:

    Public Key: /etc/nxserver/server.id_dsa.pub.key
    Private Key: /etc/nxserver/client.id_dsa.key

The <b>private</b> key is what needs to be handed out to your users.  They will then place this private key into their NX client configurations in order to login and talk to the NX server.

The official NX server has a "--keygen" command that can be used to create a new key pair for increased security.  But FreeNX 0.7 does not currently feature that ability.  Instead, we must use the ssh-keygen command (part of OpenSSH) to create new key files.  Make sure that you make backup copies of the above key files before using the following commands.

Note: DSA keys are always 1024 bits.

    # cd /etc/nxserver/
    # ssh-keygen -t dsa -f /etc/nxserver/new-dsa-key -N ''
    # mv client.id_dsa.key client.id_dsa.key.OLD
    # mv server.id_dsa.pub.key server.id_dsa.pub.key.OLD
    # mv new-dsa-key client.id_dsa.key
    # mv new-dsa-key.pub server.id_dsa.pub.key
    # service freenx-server restart
    # cat server.id_dsa.pub.key
    # /var/lib/nxserver/home/.ssh
    # vi authorized_keys2

You will then need to change the old key line to match the new public key.  At this point, until you update any clients with the new private key file (client.id_dsa.key), they will be unable to connect to the server.

    # cat /etc/nxserver/client.id_dsa.key

Note: FreeNX seemingly stores the client.id_dsa.key in two places (/etc/nxserver and under /var/lib/nxserver/home/.ssh).

<b>Second line of defense - sshd_config</b>

The default FreeNX install on CentOS/RedHat requires that your users can authenticate via passwords to SSH.  Obviously, not ideal, but we'll cover that in a few minutes.  For the moment, make sure that your /etc/ssh/sshd_config file contains the following settings:

    PermitRootLogin no
    PasswordAuthentication yes

You should now be able to login using the NX client software to your server.  The username should be an account in /etc/passwd for which you know the password.

<b>Locking down SSH #1 - use a non-standard port</b>

For servers that face the public internet, using the default SSH port of 22 is an open invitation for people to try and crack your SSH server (dictionary attacks, brute-force, overflows).  While SSH using only public keys is very secure, all of the attack attempts will generate entries in your logs and are basically a nuisance.

Probably one of the easiest fixes to avoid most brute-force attacks is to run SSH on a non-standard port.  This requires making two changes (and you'll need to let anyone else who talks to your servers via SSH know about the port change):

1) Change the port number in /etc/ssh/sshd_config:

    #Port 22
    Port 9822

2) Change /etc/nxserver/node.conf

    #SSHD_PORT=22
    SSHD_PORT=9822

3) Restart the two services

    # service freenx-server restart
    # service sshd restart

When you connect with the NX client, you will have to remember to specify the non-standard port number in the connection details.

<b>Re-locking SSH, closing the password authentication hole</b>

Key links:

[[FreeNX-kNX] FreeNX, SSH, and su](http://mail.kde.org/pipermail/freenx-knx/2005-July/001596.html)
[Re: [SLE] Resolved - Setting up NXfree to use ssh keys](http://lists.suse.de/opensuse/2006-04/msg01979.html)
[How to remote desktop using SSH and FreeNX ](http://ubuntuforums.org/showthread.php?t=467219)

Now that we've gotten NX working using password authentication, it's time to close that hole back up.  In order to do this, you have two choices:

...

(Someday I'll finish this post.  Probably have to run 2 copies of sshd, with different security settings.)
