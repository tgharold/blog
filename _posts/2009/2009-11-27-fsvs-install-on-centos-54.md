---
layout: post
title: 'FSVS: Install on CentOS 5.4'
date: '2009-11-27T20:28:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


(Also see my older post on this: [FSVS - Install on CentOS 5](/blog/2008-06-28-fsvs-install-on-centos-5).  Or the original post where I explained the power of [FSVS for sysadmins](/blog/2007-05-31-fsvs-for-sysadmins).)

I'm going to start with the assumption that this is a base CentOS 5.4 install without *any* package groups selected during the initial install.  In my case, this is a DomU that I'm setting up under Xen to serve as testing server for web development.  The only thing I've done so far is setting the root password and configuring it to use a static IP address.

The basic steps will be:
<ol>

<li>Setup the RPMForge repository

</li>
<li>Install the packages needed for FSVS

</li>
<li>Download and compile [FSVS](http://fsvs.tigris.org/)

</li>
<li>Configure ignore patterns

</li>
<li>Do the base check-ins

</li>
</ol>

<b>Setting up RPMForge</b>

In order to get the latest Subversion packages for your system, you'll have to [add RPMForge as a source repository](http://rpmrepo.org/RPMforge/Using).  The CentOS base repository only has Subversion 1.4.2 and the latest is currently 1.6.6.  I recommend doing this in conjunction with the yum-priorities package.

<code># yum install yum-priorities</code>

After installing the yum-priorities package, you should edit the CentOS-Base.repo file found under /etc/yum.repos.d/.  For the base repositories, I recommend setting them to priority values of 1 through 3.  For example:

<code>[base]
name=CentOS-$releasever - Base
mirrorlist=http://mirrorlist.centos.org/?release=$releasever&amp;arch=$basearch&amp;repo=os
#baseurl=http://mirror.centos.org/centos/$releasever/os/$basearch/
gpgcheck=1
gpgkey=http://mirror.centos.org/centos/RPM-GPG-KEY-CentOS-5
priority=1
exclude=subversion-*</code>

I generally give the [base], [updates], [addons], [extras] repositories a priority of "1", with [centosplus] and [contrib] getting a priority of "3".

In addition, you'll need to add or edit the "exclude=" line in the [base] repository section to exclude Subversion from being sourced from that repository.  This will allow the Yum package manager to look in other repositories to find Subversion.

Now we can install the RPMForge repository (see [Using RPMForge](http://rpmrepo.org/RPMforge/Using)).

<code># cd /root/
# wget http://packages.sw.be/rpmforge-release/rpmforge-release-0.3.6-1.el5.rf.x86_64.rpm
# rpm -Uhv rpmforge-release-0.3.6-1.el5.rf.x86_64.rpm
# cd /etc/yum.repos.d/</code>

Now you should edit the rpmforge.repo file and insert a priority= line.  I recommend a value of 10 or 25.

You can now verify that you'll pull in the latest Subversion package by the following command:

<code># yum info subversion
Available Packages
Name       : subversion
Arch       : x86_64
Version    : 1.6.6
Release    : 0.1.el5.rf
Size       : 6.8 M
Repo       : rpmforge</code>

<b>Install the packages needed for FSVS</b>

<code># yum install subversion subversion-devel ctags apr apr-devel gcc gdbm gdbm-devel pcre pcre-devel apr-util-devel</code>

<b>Download and compile FSVS</b>

As always, you shouldn't compile code as the root user.

<code># su username
$ mkdir ~/fsvs
$ cd ~/fsvs
$ wget http://download.fsvs-software.org/fsvs-1.2.1.tar.bz2
$ tar xjf fsvs-1.2.1.tar.bz2
$ cd fsvs-1.2.1
$ ./configure
$ make
$ exit
# cp /home/username/fsvs/fsvs-1.2.1/src/fsvs /usr/local/bin/
# chmod 755 /usr/local/bin/fsvs</code>

<b>Creating the repository on the SVN server</b>

This is how we setup users on our SVN server.  Machine accounts are prefixed as "sys-" in front of the machine name.  The SVN repository name matches the name of the machine.  In general, only the machine account should have write access to the repository, although you may wish to add other users to the group so that they can gain read-only access.

<code># useradd -m sys-www-test
# passwd sys-www-test
# svnadmin create /var/svn/sys-www-test
# chmod -R 740 sys-www-test
# chmod -R g+s sys-www-test/db
# chown -R sys-www-test:sys-www-test sys-www-test</code>

Back on the source machine (our test machine), we'll need to create an SSH key that can be used on our SVN server.  You may wish to use a slightly larger RSA key (3200 bits or 4096 bits) if you're working on an extra sensitive server.  But a key size of 2048 bits should be secure for another decade for this purpose.

<code># cd /root/
# mkdir .ssh
# chmod .ssh 700
# cd .ssh
# /usr/bin/ssh-keygen -N '' -C 'svn key for root@hostname' -t rsa -b 2048 -f root@hostname
# cat root@hostname.pub</code>

Copy this key into the clipboard or send it to the SVN server or the SVN server administrator.  Then we'll need to create a ~/.ssh/config file to tell the user what account name, port and key file to use when talking to the SVN server.

<code># vi /root/.ssh/config
Host svn.tgharold.com
Port 22
User sys-www-test
IdentityFile /root/.ssh/root@hostname</code>

Back on the SVN server, you'll need to finish configuration of the user that will add files to the SVN repository.

<code># su username
$ cd ~/
$ mkdir .ssh
$ chmod 700 .ssh
$ cd .ssh
$ cat &gt;&gt; authorized_keys
(paste in the SSH key from the other server)
$ chmod 600 authorized_keys</code>

Now you'll want to prepend the following in front of the key line in the authorized_keys file.

<code>command="/usr/bin/svnserve -t -r /var/svn",no-agent-forwarding,no-pty,no-port-forwarding,no-X11-forwarding</code>

That ensures (mostly) that the key can only be used to run the svnserve command and that it can't be used to access a command shell on the SVN server.

Test the configuration back on the original server by issuing the "svn info" command.  Alternately, you can try to ssh to the SVN repository server.  Errors will usually either be logged in /var/log/secure on the source server or in the same log file on the SVN repository server.

Here's an example of a successful connection:

<code># ssh svn.tgharold.com
( success ( 2 2 ( ) ( edit-pipeline svndiff1 absent-entries commit-revprops depth log-revprops partial-replay ) ) )</code>

This shows that they key is running the "svnserve" command automatically.

<b>Connect the system to the SVN repository</b>

The very first command that you'll need to issue for FSVS is the "urls" (or "initialize") command.  This tells FSVS what repository will be used to store the files.

<code># cd /
# mkdir /var/spool/fsvs
# mkdir /etc/fsvs/
# fsvs urls svn+ssh://svn.tgharold.com/sys-www-test/</code>

You may see the following error, which means you need to create the /var/spool/fsvs folder, then reissue the fsvs urls command.

<code>stat() of waa-path "/var/spool/fsvs/" failed. Does your local WAA storage area exist?</code>

The following error means that you forgot to create the /etc/fsvs/ folder.

<code>Cannot write to the FSVS_CONF path "/etc/fsvs/".</code>

<b>Configure ignore patterns and doing the base check-in</b>

When constructing ignore patterns, generally work on adding a few directories at a time to the SVN repository.  Everyone has different directories that they won't want to version, so you'll need to tailor the following to match your configuration.  However, I generally recommend starting with the following:

<code># cd /
# fsvs ignore group:ignore,./dev
# fsvs ignore group:ignore,./etc/fsvs/
# fsvs ignore group:ignore,./etc/gconf/
# fsvs ignore group:ignore,./etc/gdm/
# fsvs ignore group:ignore,./home/
# fsvs ignore group:ignore,./lost+found
# fsvs ignore group:ignore,./media/
# fsvs ignore group:ignore,./mnt/
# fsvs ignore group:ignore,./proc
# fsvs ignore group:ignore,./root/.gconf
# fsvs ignore group:ignore,./root/.nautilus
# fsvs ignore group:ignore,./selinux/
# fsvs ignore group:ignore,./srv
# fsvs ignore group:ignore,./sys
# fsvs ignore group:ignore,./tmp/
# fsvs ignore group:ignore,./usr/tmp/
# fsvs ignore group:ignore,./var/gdm/
# fsvs ignore group:ignore,./var/lib/mlocate/
# fsvs ignore group:ignore,./var/lock/
# fsvs ignore group:ignore,./var/log/
# fsvs ignore group:ignore,./var/mail/
# fsvs ignore group:ignore,./var/run/
# fsvs ignore group:ignore,./var/spool/
# fsvs ignore group:ignore,./var/tmp/
</code>

Then you'll either want to ignore (or encrypt) the SSH key files.

<code># cd /
# fsvs ignore group:ignore,./root/.ssh
# fsvs ignore group:ignore,./etc/ssh/shadow*
# fsvs ignore group:ignore,./etc/ssh/ssh_host_key
# fsvs ignore group:ignore,./etc/ssh/ssh_host_dsa_key
# fsvs ignore group:ignore,./etc/ssh/ssh_host_rsa_key</code>

You can check what FSVS is going to version by using the "fsvs status pathname" command (such as "fsvs status /etc").  Once you are happy with the selection in a particular path, you can do the following command:

<code># fsvs ci -m "base check-in" /etc</code>

Repeat this for the various top level trees until you have checked everything in.  Then you should do one last check-in at the root level that catches anything you might have missed.
