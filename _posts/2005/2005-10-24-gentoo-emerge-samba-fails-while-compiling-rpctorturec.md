---
layout: post
title: 'Gentoo: emerge samba fails while compiling rpctorture.c'
date: '2005-10-24T12:59:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Got the following error while trying to emerge samba into my Gentoo box.

```
Compiling torture/rpctorture.c
make: *** Waiting for unfinished jobs....
torture/rpctorture.c:27: error: `global_myname' redeclared as different kind of symbol
include/proto.h:1019: error: previous declaration of `global_myname'
torture/rpctorture.c:57: warning: `struct client_info' declared inside parameter list
torture/rpctorture.c:57: warning: its scope is only this definition or declaration, which is probably not what you want
torture/rpctorture.c: In function `rpcclient_connect':
torture/rpctorture.c:62: error: dereferencing pointer to incomplete type
torture/rpctorture.c:62: error: dereferencing pointer to incomplete type
torture/rpctorture.c:63: error: dereferencing pointer to incomplete type
torture/rpctorture.c:66: error: dereferencing pointer to incomplete type
torture/rpctorture.c:66: error: dereferencing pointer to incomplete type
torture/rpctorture.c:68: error: dereferencing pointer to incomplete type
torture/rpctorture.c:68: error: dereferencing pointer to incomplete type
torture/rpctorture.c: At top level:
torture/rpctorture.c:90: warning: `struct client_info' declared inside parameter list
torture/rpctorture.c: In function `run_enums_test':
torture/rpctorture.c:96: warning: passing arg 1 of `rpcclient_connect' from incompatible pointer type
torture/rpctorture.c:102: error: dereferencing pointer to incomplete type
torture/rpctorture.c:102: error: dereferencing pointer to incomplete type
torture/rpctorture.c: At top level:
torture/rpctorture.c:134: warning: `struct client_info' declared inside parameter list
torture/rpctorture.c: In function `run_ntlogin_test':
torture/rpctorture.c:140: warning: passing arg 1 of `rpcclient_connect' from incompatible pointer type
torture/rpctorture.c:146: error: dereferencing pointer to incomplete type
torture/rpctorture.c:146: error: dereferencing pointer to incomplete type
torture/rpctorture.c: At top level:
torture/rpctorture.c:167: warning: `struct client_info' declared inside parameter list
torture/rpctorture.c: In function `main':
torture/rpctorture.c:233: error: storage size of `cli_info' isn't known
torture/rpctorture.c:377: error: `scope' undeclared (first use in this function)
torture/rpctorture.c:377: error: (Each undeclared identifier is reported only once
torture/rpctorture.c:377: error: for each function it appears in.)
torture/rpctorture.c:535: warning: passing arg 5 of `create_procs' from incompatible pointer type
torture/rpctorture.c:539: warning: passing arg 5 of `create_procs' from incompatible pointer type
make: *** [torture/rpctorture.o] Error 1
 * rpctorture didn't build
running build
running build_py
running build_ext
--------------------------- ACCESS VIOLATION SUMMARY ---------------------------
LOG FILE = "/var/log/sandbox/sandbox-net-fs_-_samba-3.0.14a-r2-21241.log"

access_wr: /etc/krb5.conf
--------------------------------------------------------------------------------
# 
```

Here are my current USE flags:

```
# cat /etc/make.conf

# These settings were set by the catalyst build script that automatically built this stage
# Please consult /etc/make.conf.example for a more detailed example
CFLAGS="-Os -mcpu=i686"
CHOST="i386-pc-linux-gnu"
CXXFLAGS="${CFLAGS}"
MAKEOPTS="-j2"

GENTOO_MIRRORS="http://gentoo.osuosl.org/"
SYNC="rsync://rsync.namerica.gentoo.org/gentoo-portage"

USE="apache2 kerberos ldap postgres samba -alsa -apm -arts -bitmap-fonts -gnome -gtk -gtk2 -kde -mad -mikmod -motif -opengl -oss -qt -quicktime -sdl -truetype -truetype-fonts -type1-fonts -X -xmms -xv"

# cat /etc/make.profile/make.defaults

# Copyright 1999-2005 Gentoo Foundation
# Distributed under the terms of the GNU General Public License v2
# $Header: /var/cvsroot/gentoo-x86/profiles/default-linux/x86/2005.1/make.defaults,v 1.4 2005/08/29 22:20:25 wolf31o2 Exp $

USE="alsa apm arts avi berkdb bitmap-fonts crypt cups eds emboss encode fortran foomaticdb gdbm gif gnome gpm gstreamer gtk gtk2 imlib ipv6 jpeg kde libg++ libwww mad mikmod motif mp3 mpeg ncurses nls ogg oggvorbis opengl oss pam pdflib perl png python qt quicktime readline sdl spell ssl tcpd truetype truetype-fonts type1-fonts vorbis X xml2 xmms xv zlib"
#
```

I'm still searching for a solution to this issue.  I've heard it has to do with trying to use the kerberos USE flag (which is not an optional flag for me).  The closest possible solution in Google is on the Gentoo forums ([Problems upgrading to Samba 3.0.14a-r2!](http://forums.gentoo.org/viewtopic-t-367341.html)).  The user, "jpnag", posts a solution.

The solution involves editing the ebuild file for Samba.  This is where you will need to become a bit more knowledgeable about how portage and emerge works (see "<b>man make.conf</b>" for details on some of this along with "<b>man portage</b>").  

By default, portage downloads and installs packages under the "/usr/portage/" tree (defined by "PORTDIR=" in your "/etc/make.conf" file or "/etc/make.profile/make.defaults" file).  There is also an optional define, "PORTDIR_OVERLAY=", which you can use to point at a tree containing user-built ebuild files that are not updated by "emerge --sync".  Essentially, the second tree will overlay the first.  So if you have "package X" in both trees, only the one in the overlay tree will get compiled.

Now to create the backup copy of the broken Samba ebuild.  If you have not already added "PORTDIR_OVERLAY=" to your "make.conf" file, you should also do this.

```
# cd /etc
etc # echo 'PORTDIR_OVERLAY="/usr/local/portage"' &gt;&gt; /etc/make.conf
etc # cd /usr/local
local # ls /usr/portage/net-fs/samba/
local # mkdir portage ; cd portage
portage # mkdir net-fs ; cd net-fs
net-fs # mkdir samba ; cd samba
samba # cp -a /usr/portage/net-fs/samba/* .
samba # ls -l samba-3.0.14a-r2.ebuild
samba # nano -w samba-3.0.14a-r2.ebuild
```

Now hit [Ctrl-W] and type "src_compile", which will take you straight to the following code block:

```
rc_compile() {
        ebegin "Running autoconf"
                autoconf
        eend $?

        local myconf
        local mymods
        local mylangs

        if use xml || use xml2 ;
        then   
                mymods="xml,${mymods}"
        fi
```

Somewhere towards the start of the funciton, add the line "addpredict /etc/krb5.conf".

```
src_compile() {
        ebegin "Running autoconf"
                autoconf
        eend $?

        local myconf
        local mymods
        local mylangs

        addpredict /etc/krb5.conf

        if use xml || use xml2 ;
        then
                mymods="xml,${mymods}"
        fi
```

Create the ebuild digest (MD5 signatures) for the patched package.

```
samba # ebuild /usr/local/portage/net-fs/samba/samba-3.0.14a-r2.ebuild digest 
&gt;&gt;&gt; Generating digest file...
&lt;&lt;&lt; samba-3.0.14a.tar.gz
&lt;&lt;&lt; samba-vscan-0.3.6.tar.bz2
&lt;&lt;&lt; samba-3-gentoo-0.3.3.tar.bz2
&gt;&gt;&gt; Generating manifest file...
&lt;&lt;&lt; ChangeLog
&lt;&lt;&lt; metadata.xml
&lt;&lt;&lt; samba-3.0.14a-r2.ebuild
&lt;&lt;&lt; samba-3.0.14a-r3.ebuild
&lt;&lt;&lt; samba-3.0.20-r1.ebuild
&lt;&lt;&lt; samba-3.0.20a.ebuild
&lt;&lt;&lt; samba-3.0.20b.ebuild
&lt;&lt;&lt; files/digest-samba-3.0.14a-r2
&lt;&lt;&lt; files/README.gentoo
&lt;&lt;&lt; files/digest-samba-3.0.14a-r3
&lt;&lt;&lt; files/digest-samba-3.0.20-r1
&lt;&lt;&lt; files/digest-samba-3.0.20a
&lt;&lt;&lt; files/digest-samba-3.0.20b
&gt;&gt;&gt; Computed message digests.

samba # emerge -pv samba

These are the packages that I would merge, in order:

Calculating dependencies ...done!
[ebuild  N    ] net-fs/samba-3.0.14a-r2  -acl +cups -doc +kerberos +ldap -libclamav -mysql -oav +pam +postgres +python -quotas +readline (-selinux) -winbind -xml +xml2 0 kB [1] 

Total size of downloads: 0 kB
Portage overlays:
 [1] /usr/local/portage

samba # emerge samba
```

(crosses fingers)
