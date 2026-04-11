---
layout: post
title: 'Forcing users to use public SSH keys to authenticate'
date: '2007-01-05T06:32:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Here are the steps I use when I create a new user account on a secure SSH server (where only public keys are allowed).

    # useradd -m username
    # passwd username
    (paste in a super-long randomized password)
    # cd /home/username
    # su username
    $ mkdir .ssh
    $ chmod 700 .ssh
    $ cd .ssh
    $ cat &gt; username@linux.pub
    (paste in the public key file from SecureCRT)
    $ ssh-keygen -i -f username@linux.pub &gt;&gt; authorized_keys
    $ chmod 600 *

At this point, the user should be able to login via SecureCRT using their private/public key pair.  There's no need for them to know the password that you assigned to them on the server (so use something random and at least 30+ characters).
