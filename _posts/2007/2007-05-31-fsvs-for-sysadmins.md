---
layout: post
title: 'FSVS for sysadmins'
date: '2007-05-31T10:09:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---



<b>Notes:</b> This entry was based on v1.1.4.  The 1.1.5 and later versions of FSVS also place a few files in /etc/fsvs.  

<b>Original post follows</b>

Okay, I'm heading back to trying FSVS again for doing system configuration management.  The [FSVS website](http://fsvs.tigris.org/) has some documentation, but for the full documentation you'll want to download the source tarball and look in the "doc/" folder.

<b>Resource links (and other useful information):</b>

[FSVS (fsvs.tigris.org)](http://fsvs.tigris.org/) - the home page for FSVS.  See also the [Purpose of FSVS](http://fsvs.tigris.org/purpose.html) and [Backup](http://fsvs.tigris.org/doxygen/html/group__howto__backup.html) pages.

[Subversion (software)](http://en.wikipedia.org/wiki/Subversion_(software)) - The SubVersion explanatory page over at Wikipedia.

[SSH tricks](http://svn.collab.net/repos/svn/trunk/notes/ssh-tricks) - One of the most important documents to read if you want to setup secure SSH access to your SVN server.  It specifies how to lock things down so that "/usr/bin/svnserve" is the only thing they can do with a particular public key.  

[Setting up Subversion in Linux](http://www.section6.net/wiki/index.php/Setting_up_Subversion_in_Linux)

[Creating Subversion Repositories](http://www.inf.ufpr.br/renato/repository.html)

<b>Now, here's what I do know about FSVS:</b>

- It uses SubVersion for the backend storage.  Which means that if you already have a SVN server up and running, you can use it for the FSVS storage.  This also means that you could pull configuration files down onto your laptop with SVN to take a gander at the revision history of a particular file.

- FSVS doesn't pollute your directories with ".svn" folders.  Instead, it keeps a central storage database elsewhere (by default this goes in /var/spool/fsvs, but you can move it).  This WAA (Working copy Administrative Area) directory only contains file lists and hashes.  It does not contain "pristine copies" of any files, so it will use up a lot less space then ".svn" folders.

- FSVS will keep track of file metadata (such as timestamps, chmod flags, etc. - see the FSVS website for particulars).  I'm not sure whether this includes information needed by SELinux.

- You can use FSVS to push changes to machines.  Not something that I'm interested in (yet), but I might use it down the road.

- And most (all?) tricks you can use in SVN repositories apply to FSVS.  Such as cloning a machine from another's configuration using "svn cp" or comparing files between two machines.  Or creating a branch for a new configuration.

- FSVS allows you to make "empty" commits to the repository.  If nothing has changed in the system and you do a <b>fsvs ci -m "commit message"</b> then FSVS will create a new revision in the repository, but with no actual changes.  That may come in handy in certain circumstances.

<b>The method to my madness</b>

My preference for system administration is to have a separate user account and SSH key for each machine that I manage.  This allows me to use a no-password SSH key on the machine so that I can do svn/fsvs commands easily (or script svn/fsvs commands).  Because the SSH server is locked down, and the keys are locked down with the "command=" syntax of SSH - I'm not terribly worried about keys that don't have passwords.  Since SVN doesn't allow you to permanently delete files from a repository, there's a limited amount of damage that an attacker could do if they swipe the private key.

(Lastly, because the SSH private key is stored inside of /root/, it means they've cracked the server security already.  We're just trying to limit the damage and keep them from being able to erase things on the central SVN server.)

Naturally, after talking about SSH keys, I'm only using the "svn+ssh" method of accessing the central repositories.

<b>SSH Security considerations</b>

On the SVN server, you should edit /etc/ssh/sshd_config and verify that the following are enforced in the SSH daemon configuration:

    AllowTcpForwarding no
    X11Forwarding no
    PermitTunnel no 

That eliminates most abuses that are possible, even if someone edits their ~/.ssh/authorized_key file on the SVN server.

<b>Creating a user account on the SSH server</b>

Make sure you have a naming scheme in place.  For us, regular developers and administrators get normal looking usernames (i.e. "thomas" or "tgh" or "haroldt").  For machine accounts, we prefix the server name with "sys-" to create the username (i.e. "sys-fw1", "sys-mail1", "sys-gracie").  Which should make it easy to see if a machine has been added to groups that it shouldn't be in.  Any groups that are used to control access to SVN directories are prefixed with "svn-repositoryname" such as "svn-sys-fw" (which owns the "sys-fw" repository).

A) On the client machine:

Login as root (or "su" to root).

    # cd /root/
    (skip the next 2 commands if the .ssh subfolder already exists)
    # mkdir .ssh
    # chmod .ssh 700
    # cd .ssh
    # /usr/bin/ssh-keygen -N '' -C 'svn key for root@hostname' -t rsa -b 2048 -f root@hostname
    # cp /root/.ssh/root@svn /root/.ssh/id_rsa
    # cat root@hostname.pub
    (copy this into the clipboard or send it to the SVN server or the SVN server administrator)

B) On the SVN server

Note: You should use some sort of random password creator (or the output of /dev/random or /dev/urandom) to create a long password that can be copied and pasted into the password prompt.  Since we're using SSH keys, the account doesn't need a password that anyone knows.

(I know there's a better way to do make an account with an unguessable password, yet still allow SSH access via pub keys, but I can't find it at the moment.)

    # useradd -m username
    (i.e. "useradd -m sys-fw1-pri")
    # passwd username
    (paste in a super-long randomized password, such as a few bytes from /dev/urandom shoved through md5sum)
    # cd /home/username
    # su username
    $ mkdir .ssh
    $ chmod 700 .ssh
    $ cd .ssh
    $ cat &gt; root@hostname.pub
    (paste in the public key file from the client system)
    $ cat root@hostname.pub &gt;&gt; authorized_keys
    $ chmod 600 *

Now to lock the key down, edit the ~/.ssh/authorized_keys file and put the following on the front of the key line that will be used by the client machine:

    command="/usr/bin/svnserve -t -r /var/svn",no-agent-forwarding,no-pty 

This forces the connection to run the "svnserve" command in tunnel mode.  So this SSH key cannot be used to login or run any other commands on the server.  It also changes the SVN root path to /var/svn.  You will want to also add "no-port-forwarding" and "no-X11-forwarding" if you have not disabled those in your /etc/ssh/sshd_config file.

We now have a user account that can be used with SVN.  Go ahead and [Ctrl-D] to escape the "su username" session and get back into the root account.

<b>Setting up the repository (on the SVN server)</b>

Reasons to use a common repository for all similar machines:
- Ability to do a svn diff between two different machines
- Ability to clone machines ("svn cp")
- Backup scripts are less complex (fewer repositories)
- You can "svn diff" between machines

Reasons to use individual repositories
- Easy to secure using chmod/chown
- Easy to get report sizes on how much space a machine is using on the repository server
- Easy to dump/load an individual machine's repository
- Easy to take a machine offline and remove the repository to save space
- A machine's SSH key can only be used to look at their repository (unless you configure per-directory authentication in SVN)

Note: I'm using "username", "hostname" and "machinename" fairly interchangeably on this page.  (Someday I'll go back and clean it up.)

On the SVN server:

    # cd /var/svn
    (your repositories may be stored elsewhere)
    # svnadmin create /var/svn/sys-machinename
    # chmod -R 770 sys-machinename
    # chmod -R g+s sys-machinename/db
    # chown -R sys-machinename:sys-machinename sys-machinename

Notes: 
- A chmod of "770" allows read/write access to everyone in the same group.
- A chmod of "700" only allows read/write to the owner account.
- The third octet should probably always be "0" to prevent the repository from being world-readable.

<b>Verifying the connection (on the client)</b>

You will need to customize the following URL to point at your SVN repository location.

    # svn info svn+ssh://sys-machinename@svn.intra.example.com/sys-machinename/

That should prompt you to accept the server's public key, then display a response fron the SVN server.  If things don't work, then you've got connectivity (firewall), account (wrong name? wrong key?) or permissions (chmod or chown goofs?).

<b>Installing FSVS (on the client)</b>

Notes:

In order for the install to succeed, you must have installed the "subversion", "subversion-devel" "apr", "apr-devel", "gcc" and "ctags" packages.  Two others that you need are "gdbm" and "pcre" (and the associated developer packages).  There may be other dependencies that will also be installed that are required by those packages.  The following command worked for me on CentOS5:

    # yum install subversion subversion-devel ctags apr apr-devel gcc gdbm gdbm-devel pcre pcre-devel

Head on over to the official [project page](http://freshmeat.net/projects/fsvs/) at freshmeat.net and download the tarball.  This is currently "fsvs-1.14.tar.gz".  Extract the tarball to a folder somewhere (i.e. /root/fsvs-1.14.tar.gz) and use a terminal session to go to that folder.

    # cat README
    (look for the section that talks about the install)
    # cd src
    # make
    (you will receive a message that the Makefile has now been updated and that you need to run make again)
    # make
    (you should see a large stream of gcc output with the following at the end)
    -rwxr-xr-x 1 root root 201510 May 31 09:54 fsvs
    (you must see the above line to know that you got a good compile)
    # cp fsvs /usr/local/bin

At this point, FSVS *should* be installed correctly.

<b>Getting started with FSVS</b>

By default, FSVS will want to use /var/spool/fsvs unless you define the "WAA" variable and point it somewhere else.  So according to the README you will need to create that folder and then initialize it (which lets FSVS create the administrative files it needs).

Note #1: I'm not sure how large /var/spool/fsvs will get.  You may eventually want to break it off into a separate LVM volume of its own.  Since it is mostly file lists and hashes, it shouldn't get too large, but you may want to put it on an ext3 volume with more inodes then normal.  

Note #2: You should read both the README and the output of "fsvs help urls".

    # mkdir -p /var/spool/fsvs
    # chmod 700 /var/spool/fsvs
    # cd /
    # fsvs urls svn+ssh://username@machine/path/to/repos
    (The "fsvs urls" won't display any confirmation text.)

The above will connect the root folder to the repository path.  You could also do multiple URLs and only link sub-folders (such as /etc, /usr, /home) up against the SVN repository.

<b>Setting up ignore filters</b>

After telling FSVS that we want to use "/" as our working copy, we'll want to also tell it to ignore various directories and files.  While this tends to be somewhat similar across Linux distributions, you should also plan on modifying this list to match your distribution.

Make sure you read "fsvs-*/doc/IGNORING" and the output of "# fsvs help ignore".

    # fsvs ignore ./backup
    # fsvs ignore ./dev
    # fsvs ignore ./mnt
    # fsvs ignore './proc/*'
    # fsvs ignore ./sys
    # fsvs ignore ./tmp
    # fsvs ignore ./var/tmp
    # fsvs ignore ./var/spool

In addition you may wish to initially ignore all of the binary file directories (such as ./lib, ./lib64, ./sbin, ./usr, ./var) and focus solely on /etc, /home, /boot and /root.  That will give you a much slimmer listing when you "fsvs status" from the root directory.

You can use the "fsvs ignore dump" and "fsvs ignore load" commands to backup your listing, edit it, then load it back into FSVS.  Note that you <b>must</b> be in the base directory of your working copy, otherwise "fsvs ignore dump" will return an empty listing.

    # cd /
    # fsvs ignore dump &gt; ~/fsvs-ignore.txt
    # vi ~/fsvs-ignore.txt
    # sort ~/fsvs-ignore.txt | fsvs ignore load

My initial listing on CentOS5 is:

<code>./backup
./dev
./lost+found
./media
./mnt
./proc/*
./selinux
./sys
./tmp
./var/named/chroot/proc
./var/spool
./var/tmp</code>

<b>Putting /etc under version control</b>

Assuming that you setup FSVS where "/" (root) is the base of the working copy, we can now add the contents of /etc to SVN.

    # cd /
    # fsvs commit -m "Base check-in of /etc" /etc
    # fsvs commit -m "Base check-in of /boot" /boot

If you want to deep-commit a single folder (such as /usr/local/sbin) without doing the intervening folders:

    # cd /
    # fsvs commit -m "Base check-in" /usr/local/sbin

<b>Working with FSVS</b>

Create a test file in /etc

    # cat &gt; /etc/testfile.txt
    foo
    # fsvs commit -m "Checking in a test file" /etc/testfile.txt

Now delete the test file

<code># rm testfile.txt
# fsvs status .
D...         4  ./etc/testfile
.mC.       dir  ./etc
# fsvs commit -m "Removed test file" .
Committing to svn+ssh://sys-fw1-pri@svn.example.com/sys-fw1-pri
.mC.       dir  ./etc
D...         4  ./etc/testfile
committed revision      7 on 2007-06-04T00:17:13.808327Z as sys-fw1-pri</code>

That just scratches the surface, but covers the majority of day-to-day use.  Unlike SVN, FSVS knows (assumes) that when a file is missing that it should implicity do a "delete" operation in the repository to make the repository match the file system.

Other useful commands to know are "fsvs unversion" and "fsvs diff".
