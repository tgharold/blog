---
layout: post
title: 'Gentoo Samba (round 3)'
date: '2004-05-08T13:54:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


([previous post, samba round 2](/techblog/2004/05/gentoo-samba-round-2.shtml))

Well, after a busy week at work, I finally had time to log back into my little VIA EPIA server running Gentoo Linux.  In my previous post, I had re-emerged the latest version of samba (v3), but I never had time to go back and try things out again after the emerge finished.

The original problem was that I [couldn't find the "net" command](/techblog/2004/05/gentoo-samba-with-ads.shtml), which turns out to be because I was using Samba v2 instead of Samba v3.  I just logged into the box, su'd to root, and typed "net".

Bingo!  I now have a "net" command!

So now I need to add the box to the ADS domain, and do all that other config stuff that I hadn't figured out yet.  (Hint for newbies to a linux system, keep a running blog like this and use software like SecureCRT with logging enabled so that you can trace your steps.)

    # kinit administrator@intra.tgharold.org
    Password for administrator@intra.tgharold.org: ******
    kinit(v5): KDC reply did not match expectations while getting initial credentials

Whoops, back to the KDC error... my /etc/krb5kdc/kdc.conf file looks fine at first glance, so does my /etc/krb5.conf file.  Hmmm.... oh, wait, wrong kinit command, ADS domain must be in CAPS:

    # kinit administrator@INTRA.TGHAROLD.ORG
    Password for administrator@INTRA.TGHAROLD.ORG: ******
    #

That did it!  Next step is to join the ADS domain:

    # net ads join
    [2004/05/08 13:54:25, 0] param/loadparm.c:map_parameter(2410)
      Unknown parameter encountered: "realm"
    [2004/05/08 13:54:25, 0] param/loadparm.c:lp_do_parameter(3048)
      Ignoring unknown parameter "realm"
    [2004/05/08 13:54:25, 0] param/loadparm.c:map_parameter(2410)
      Unknown parameter encountered: "ads server"
    [2004/05/08 13:54:25, 0] param/loadparm.c:lp_do_parameter(3048)
      Ignoring unknown parameter "ads server"
    ADS support not compiled in

Looks like I missed another trick (no ADS support compiled in).  FYI, running the following command should've given me a hint that something was still not ready:

    # testparm /etc/samba/smb.conf
    Load smb config files from /etc/samba/smb.conf
    Unknown parameter encountered: "realm"
    Ignoring unknown parameter "realm"
    Unknown parameter encountered: "ads server"
    Ignoring unknown parameter "ads server"
    Loaded services file OK.
    Server role: ROLE_STANDALONE
    Press enter to see a dump of your service definitions

    # Global parameters
    [global]
            workgroup = INTRA
            netbios name = NAZUMI
            server string = Samba Server %v
            local master = No
            domain master = No

Heh, but being lazy, I ignored the error messages and pressed onward.  Back to google for a bit.  Found the answer on the samba website [9.3.1. Possible errors "ADS support not compiled in"](http://samba.rutgers.edu/samba/devel/docs/html/ads.html): Samba must be reconfigured (remove config.cache) and recompiled (make clean all install) after the kerberos libs and headers are installed.

    # find / -name config.cache
    /usr/portage/app-admin/puregui/files/config.cache

Okay, skip that for the moment... let's go investigate my USE flags.  A recommended tool for that is "ufed" (which if you don't have can be emerged by "emerge ufed").  It also shows one-liner descriptions of what each USE flag represents (or you can look at /usr/portage/profiles/use.desc).  The only file modified by ufed is /etc/make.conf (represented by the 3rd position in the 3-character indicator after each USE flag).

    # emerge info

    Portage 2.0.50-r6 (default-x86-2004.0, gcc-3.3.2, glibc-2.3.2-r9, 2.6.3)
    =================================================================
    System uname: 2.6.3 i686 VIA Samuel 2
    Gentoo Base System version 1.4.3.13
    Autoconf: sys-devel/autoconf-2.58-r1
    Automake: sys-devel/automake-1.7.7
    ACCEPT_KEYWORDS="x86"
    AUTOCLEAN="yes"
    CFLAGS="-Os -march=i586 -m3dnow -fomit-frame-pointer"
    CHOST="i586-pc-linux-gnu"
    COMPILER="gcc3"
    CONFIG_PROTECT="/etc /usr/kde/2/share/config /usr/kde/3/share/config /usr/share/config /var/qmail/control"
    CONFIG_PROTECT_MASK="/etc/gconf /etc/env.d"
    CXXFLAGS="-Os -march=i586 -m3dnow -fomit-frame-pointer"
    DISTDIR="/usr/portage/distfiles"
    FEATURES="autoaddcvs ccache sandbox"
    GENTOO_MIRRORS="http://gentoo.mirrors.pair.com/ http://212.219.247.19/sites/www.ibiblio.org/gentoo/ http://212.219.247.18/sites/www.ibiblio.org/gentoo/ http://212.219.247.20/sites/www.ibiblio.org/gentoo/"
    MAKEOPTS="-j2"
    PKGDIR="/usr/portage/packages"
    PORTAGE_TMPDIR="/var/tmp"
    PORTDIR="/usr/portage"
    PORTDIR_OVERLAY=""
    SYNC="rsync://rsync.gentoo.org/gentoo-portage"
    USE="X apm arts avi berkdb crypt cups encode foomaticdb gdbm gif gnome gpm gtk gtk2 imlib jpeg kde libg++ libwww mad mikmod motif mpeg ncurses nls oggvorbis opengl oss pam pdflib perl png python qt quicktime readline sdl slang spell ssl svga tcpd truetype x86 xml2 xmms xv zlib"

There's probably a good bit of stuff that I should remove from the USE= line, but I'm not entirely sure what's needed and what's not yet.  I don't think I need to add "samba" there because I'm not interested in accessing other samba shares on the network (yet).

Okay, back to the main thread... reading the samba guide a bit more, it indicates that I need the kerberos development libraries installed.  It looks like I have those installed:

    # ls -1 /usr/lib/*krb*
    /usr/lib/libgssapi_krb5.so
    /usr/lib/libgssapi_krb5.so.2
    /usr/lib/libgssapi_krb5.so.2.2
    /usr/lib/libkrb5.so
    /usr/lib/libkrb5.so.3
    /usr/lib/libkrb5.so.3.2

Okay, so I need to do some digging... a lot of places [recommend using "etcat" to query ebuild information](http://www.gentoo.org/news/en/gwn/20030623-newsletter.xml) to find out what use flags are available, what got used during the compile.  However, in order to use etcat, you need to "emerge gentoolkit".   Takes about 5 minutes to install (if that).

    # etcat versions samba
    [ Results for search key           : samba ]
    [ Candidate applications found : 7 ]
    Only printing found installed programs.
    *  net-fs/samba :
            [   ] 2.2.8a (0)
            [M~ ] 3.0.0-r1 (0)
            [M  ] 3.0.1 (0)
            [M~ ] 3.0.1-r1 (0)
            [M~ ] 3.0.2a (0)
            [M~ ] 3.0.2a-r1 (0)
            [  I] 3.0.2a-r2 (0)

Shows that I have 3.0.3a-r2 installed ("I").  All of the other v3 are masked ("M") and/or tagged as unstable ("~").  

    #etcat uses samba
    [ Colour Code : set unset ]
    [ Legend   : (U) Col 1 - Current USE flags        ]
    [          : (I) Col 2 - Installed With USE flags ]

    U I [ Found these USE variables in : net-fs/samba-3.0.2a-r2 ]
    - - kerberos : Adds kerberos support
    - - mysql    : Adds mySQL support
    - - xml      : Check/Support flag for XML library (version 1)
    - - acl      : Adds support for Access Control Lists
    + + cups     : Add support for CUPS (Common Unix Printing System)
    - - ldap     : Adds LDAP support (Lightweight Directory Access Protocol)
    + + pam      : Adds support PAM (Pluggable Authentication Modules)
    + + readline : enables support for libreadline, a GNU line-editing library that most everyone wants.
    + + python   : Adds support/bindings for the Python language
    - - oav      : Adds support for anti-virus from the openantivirus.org project

A bit uglier... samba doesn't have kerberos support included.  And looking back at the output of "emerge info" I see that the kerberos USE flag isn't listed there.  This would be changed by the /etc/make.conf file (or using "ufed" to edit).  The USE= line in my /etc/make.conf is empty, so I'll fire up ufed, tag kerberos, and save.  Now, run the "etcat uses samba" again and notice that the kerberos USE flag now has a '+' under the 'U' column, but a '-' under the 'I' (installed) column.  Since I can't find a config.cache file that looks like it belongs to samba, I'm just going to check the package status with emerge.

    # emerge -p samba
    (shows a "R" flag after the ebuild, looking at "man emerge" that indicates that the package is already installed, but that "emerge samba" again will recompile)
    # emerge samba
    (go away for a bit... samba takes a while to compile, 30-60 minutes or so)

    # etcat uses samba
    (now shows kerberos in green, as installed)

    # testparm /etc/samba/smb.conf
    (still complains about "realm" and "ads server" in the /etc/samba/smb.conf file)

Okay, so I'm not sure what the next step is... I'll have to google again later when I'm not as frustrated.  Samba is still complaining that "ADS support is not compiled in".  The only "config.cache" file on the system is from July 2001 and is not in the samba folder.

Update: The missing piece was that I hadn't configured both the kerberos and ldap USE flags in my make.conf file.
