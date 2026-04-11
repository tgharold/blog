---
layout: post
title: 'Setting up FreeNX/NX on CentOS 5'
date: '2009-01-06T14:29:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Quick guide to setting up FreeNX/NX.  This the approximate minimums on a fresh CentOS 5.1 box.  We're limiting things to using public-key authentication from the outside and we already have a second ssh daemon running (listening on localhost, allowing password authentication).

Note: If you have ATRPMs configured as a repository, make sure that you exclude nx* and freenx*.  (Add/edit the exclude= line in the ATRPMs .repo file.)

    # yum install nx freenx
    # cp /etc/nxserver/node.conf.sample /etc/nxserver/node.conf
    # vi /etc/nxserver/node.conf

Change the following lines in the node.conf file:

    ENABLE_SSH_AUTHENTICATION="1"
    -- remove the '#' at the start of the line

    ENABLE_SU_AUTHENTICATION="1"
    -- remove the '#' at the start of the line
    -- change the zero to a one

    ENABLE_FORCE_ENCRYPTION="1"
    -- remove the '#' at the start of the line
    -- change the zero to a one

Change the server's public/private key pair:

    # mv /etc/nxserver/client.id_dsa.key /etc/nxserver/client.id_dsa.key.OLD
    # mv /etc/nxserver/server.id_dsa.pub.key /etc/nxserver/server.id_dsa.pub.key.OLD
    # ssh-keygen -t dsa -N '' -f /etc/nxserver/client.id_dsa.key
    # mv /etc/nxserver/client.id_dsa.key.pub /etc/nxserver/server.id_dsa.pub.key
    # cat /etc/nxserver/client.id_dsa.key

You'll need to give the DSA Private Key information to people who should be allowed to use FreeNX/NX to access the server.

You'll also need to put the new public key into the authorized_keys2 file:

    # cat /etc/nxserver/server.id_dsa.pub.key >> /var/lib/nxserver/home/.ssh/authorized_keys2

    # vi /var/lib/nxserver/home/.ssh/authorized_keys2

Comment out the old key, put the following at the start of the good key line.

no-port-forwarding,no-X11-forwarding,no-agent-forwarding,command="/usr/bin/nxserver" 

Restart the FreeNX/NX service:

    # service freenx-server restart

You should now be able to connect (assuming that you specify the proper SSH port and paste the private key into the configuration).
