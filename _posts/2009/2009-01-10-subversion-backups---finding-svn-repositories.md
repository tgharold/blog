---
layout: post
title: 'Subversion Backups - Finding SVN repositories'
date: '2009-01-10T07:59:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


The first trick when backing up SVN repositories is finding them so that you can run the svnadmin hotcopy command.  Well, you *could* just setup a list of export DIRS in your backup script - but as you add new SVN repositories, you have to constantly edit that script.

Caveat #1: This setup probably only works for FSFS repositories.  I don't use BerkleyDB repositories (a.k.a. BDB) so I can't guarantee that it correctly locates them.  I've chosen to look for folders that contain the "db/uuid" file as our "marker" file.  Which should result in zero false-positives or mis-identified repositories.

Caveat #2: I'm making the assumption that all of your repositories are stored in a central location (/var/svn), but they do *not* all have to be at the same depth.

<b>Step #1 - Find the uuid files</b>

This is pretty simple, we're just going to use find and grep.

# find /var/svn -name uuid | grep "db/uuid"

/var/svn/tgh-photo/db/uuid
/var/svn/tgh-dev/db/uuid
/var/svn/tgh-web/db/uuid

<b>Step #2 - Clean up the pathnames</b>

Even better, we can tack a sed command onto the end to trim off the "/db/uuid" portion, which gets us exactly what we need for passing to the "svnadmin hotcopy" command.

# find /var/svn -name uuid | grep "db/uuid" | sed 's/\/db\/uuid//'

/var/svn/tgh-photo
/var/svn/tgh-dev
/var/svn/tgh-web

(Make sure that you get all of the "\" and "/" in the right places.)

<b>Step #3 - Strip off the base directory</b>

Since I'm going to create a script variable called "BASE" that equals "/var/svn/", I'm also going to strip that off of the front of the paths.

However, we'll need to convert the BASE variable into something that sed can properly deal with.  Otherwise the slashes won't be escaped properly for the sed replacement.

# echo "/var/svn/" | sed 's/\//\\\//g'
\/var\/svn\/

# find /var/svn -name uuid | grep "db/uuid" | sed 's/\/db\/uuid//' | sed 's/^\/var\/svn\///'
tgh-photo
tgh-dev
tgh-web

Or, even better, we can use a different delimiter for sed.  That gives us a search line of:

DIRS=`find ${BASE} -name uuid | grep 'db/uuid$' | sed 's:/db/uuid$::' | sed 's:^/var/svn/::'`

Which puts a list of directory names into the DIRS varaible in our bash script.

<b>Step #4 - Putting it all together</b>

Here's our basic script.

<pre>#!/bin/bash
BASE="/var/svn/"
HOTCOPY="/var/svn-hotcopy/"
DIRS=`find ${BASE} -name uuid | grep 'db/uuid$' | sed 's:/db/uuid$::' | sed 's:^/var/svn/::'`

for DIR in ${DIRS}
do
    echo "svnadmin hotcopy ${BASE}${DIR} to ${HOTCOPY}${DIR}"
    rm -r ${HOTCOPY}${DIR}
    svnadmin hotcopy ${BASE}${DIR} ${HOTCOPY}${DIR}
done</pre>

However, we're not quite done yet because the svn hotcopy command doesn't like it when the destination folder does not exist.  So let's add the following scrap of code into the loop.

<pre>if ! test -d ${HOTCOPY}${DIR}
then
    mkdir -p ${HOTCOPY}${DIR}
fi</pre>

<b>The final script</b>

<pre>#!/bin/bash

BASE="/var/svn/"
HOTCOPY="/var/svn-hotcopy/"

FIND=/usr/bin/find
GREP=/bin/grep
RM=/bin/rm
SED=/bin/sed
SVNADMIN=/usr/bin/svnadmin

DIRS=`find ${BASE} -name uuid | $GREP 'db/uuid$' | $SED 's:/db/uuid$::' | $SED 's:^/var/svn/::'`

for DIR in ${DIRS}
do  
    echo "svnadmin hotcopy ${BASE}${DIR} to ${HOTCOPY}${DIR}"

    if ! test -d ${HOTCOPY}${DIR}
    then
        mkdir -p ${HOTCOPY}${DIR}
    fi

    $RM -r ${HOTCOPY}${DIR}
    $SVNADMIN hotcopy ${BASE}${DIR} ${HOTCOPY}${DIR}
done

# insert rdiff-backup line here</pre>

Hopefully that works out.  Note the use of "rm -r", which could cause data loss if there are errors in the script.  You will want  to be very careful while working on the script.
