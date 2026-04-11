---
layout: post
title: 'Installing Angband on CentOS 5'
date: '2007-08-15T10:35:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Installation of Angband 3.0.9 on RedHat or CentOS5.

1) Grab the latest source release from [http://rephial.org/release](http://rephial.org/release)

# cd /root
# wget http://rephial.org/downloads/3.0/angband-3.0.9-src.tar.gz
# tar xzf angband-3.0.9-src.tar.gz

2) Compile the source code (the following is for running angband from the location where you unpacked the source, see [Compiling](http://rephial.org/wiki/Compiling) for other options)

# cd angband-3.0.9
# ./configure
# make
# make install

3a) Errors: Make can't find "ncurses.h" (see also [Compiling](http://rephial.org/wiki/Compiling))

# make
        CC     main-gcu.c          
main-gcu.c:63:22: error: ncurses.h: No such file or directory

Which indicates that you need to install the ncurses library.  You can fix that by installing the "ncurses-devel" and re-running "./configure".

# yum install ncurses-devel
# ./configure

4) If you do a system install (making Angband available for all users on the system), make sure you add the users to the "games" group.  Otherwise, when your users attempt to run Angband, they will get error messages about not being able to write to various files in the /usr/local/games/lib/angband folders.

# ./configure --with-setgid=games --with-libpath=/usr/local/games/lib/angband                --bindir=/usr/local/games
# make
# make install
