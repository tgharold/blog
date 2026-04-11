---
layout: post
title: 'Setup sshd to run a second instance'
date: '2009-01-06T09:57:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


In order to lock down the servers like I prefer to, yet still allow FreeNX/NX to work, I have to setup a second copy of the sshd daemon.  The FreeNX/NX client requires that you have sshd running with password access (not just public key), but we prefer to only allow public-key access to our servers.

I did the following on CentOS 5, it should also work for Fedora or Red Hat Enterprise Linux (RHEL).  But proceed at your own risk.

1) Create a hard link to the sshd program.  This allows us to distinguish it in the process list.  It also makes sure that our cloned copy stays up to date as the sshd program is patched.

    # ln /usr/sbin/sshd /usr/sbin/sshd_nx

2) Copy /etc/init.d/sshd to a new name

This is the startup / shutdown script for the base sshd daemon.  Make a copy of this script:

    # cp -p /etc/init.d/sshd /etc/init.d/sshd<b>_nx</b>
    # vi /etc/init.d/sshd_nx

Change the following lines:

    # processname: sshd<b>_nx</b>
    # config: /etc/ssh/sshd<b>_nx</b>_config
    # pidfile: /var/run/sshd<b>_nx</b>.pid
    prog="sshd<b>_nx</b>"
    SSHD=/usr/sbin/sshd<b>_nx</b>
    PID_FILE=/var/run/sshd<b>_nx</b>.pid
    OPTIONS="-f /etc/ssh/sshd_nx_config -o PidFile=${PID_FILE} ${OPTIONS}"
    [ "$RETVAL" = 0 ] && touch /var/lock/subsys/sshd<b>_nx</b>
    [ "$RETVAL" = 0 ] && rm -f /var/lock/subsys/sshd<b>_nx</b>
    if [ -f /var/lock/subsys/sshd<b>_nx</b> ] ; then

Note: The OPTIONS= line is probably new and will have to be added right after the PID_FILE= line in the file.  There are also multiple lines that reference /var/lock/subsys/sshd, you will need to change all of them.

3) Copy the old sshd configuration file.

    # cp -p /etc/ssh/sshd_config /etc/ssh/sshd<b>_nx</b>_config

4) Edit the new sshd configuration file and make sure that it uses a different port number.

    Port 28822

5) Clone the PAM configuration file.

    # cp -p /etc/pam.d/sshd /etc/pam.d/sshd<b>_nx</b>

6) Set the new service to startup automatically.

    # chkconfig --add sshd<b>_nx</b>

...

Test it out

    # service sshd_nx start 
    # ssh -p 28222 username@localhost 

Check for errors in the log file:

    # tail -n 25 /var/log/secure

...

At this point, I would go back and change the secondary configuration to only listen on the localhost ports:

    ListenAddress 127.0.0.1
    ListenAddress ::1

...

References:

[How to Add a New "sshd_adm" Service on Red Hat Advanced Server 2.1](http://blog.thilelli.net/post/2005/07/04/How-to-Add-a-New-sshd_adm-Service-on-Red-Hat-Advanced-Server-21)

[How to install NX server and client under Ubuntu/Kubuntu Linux (revised)](http://michigantelephone.wordpress.com/2007/10/15/how-to-install-nx-server-and-client-under-ubuntukubuntu-linux/)
