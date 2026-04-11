---
layout: post
title: 'Gentoo Next Steps (ssh)'
date: '2004-04-29T20:56:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---



[Setting up SSHD on Gentoo](http://www.gentoo.org/proj/en/infrastructure/config-ssh.xml) (which just covers the basics, also see the [sshd manpage](http://www.cs.usyd.edu.au/cgi-bin/man.cgi?section=8&amp;topic=sshd) and [OpenSSH.org](http://www.openssh.com/)).

I have a book called "Building Secure Servers with Linux", and it's extremely poor with regards to actually setting up the sshd system.  (Specifically, it completely ignores the topic of how to create the public/private DSA key for the sshd process.)  Googling around for [how to create the ssh_host_dsa_key](http://www.google.com/search?hl=en&amp;lr=&amp;ie=UTF-8&amp;oe=UTF-8&amp;c2coff=1&amp;q=%2Bsshd+%2Bkeygen+%2Bssh_host_dsa_key&amp;btnG=Search) netted me a few useful articles.

[NCSA OpenSSH Installation Guide](http://www.ncsa.uiuc.edu/UserInfo/Resources/Software/ssh/openssh_install.html)
[20020124: setting up sshd on Linux](http://www.unidata.ucar.edu/projects/coohl/mhonarc/MailArchives/platforms/msg00389.html)

The NCSA link is probably the most useful, except that on my gentoo linux system, configuration stuff is under /etc/ssh  instead of /etc/openssh.

    # /usr/bin/ssh-keygen -t dsa -b 1024 -f /etc/ssh/ssh_host_dsa_key -N ""
    # chmod 600 /etc/ssh/ssh_host_dsa_key
    # chmod 644 /etc/ssh/ssh_host_dsa_key.pub

(the two chmod commands weren't really necessary on my gentoo box, they had no effect on the permissions)

To add sshd so it runs at startup (I think the following is correct):
rc-update add sshd default 

Now I can administer the box from the laptop (using SecureCRT software), getting it off of my desk and into the server rack where it belongs.  Things to do include getting PostgreSQL up and running, Samba, backing up the system, setting up recurring backups and checkout SubVersion as a replacement for Visual SourceSafe / SourceOffSite.
