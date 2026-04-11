---
layout: post
title: 'Very basic rsync / cp backup rotation with hardlinks'
date: '2009-01-07T05:12:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Here's a very basic script that I use with RSync that makes use of hard links to reduce the overall size of the backup folder.  The limitations are:

- Every morning, a server copies the current version of all files across SSH (using scp) into a "current" folder.  There are two folders on the source server that get backed up daily (/home and /local).

- Later on that day, we run the following script to rsync any new files into a daily folder (daily.0 through daily.6).  

- In order to bootstrap those daily.# folders, you have to use "cp -al current/* daily.2/" on each, which fills out the seven daily backup folders with hardlinks.  Change the number in "daily.2" to 0-6 and run the command once for each of the seven days.  Do this after the "current" folder has been populated with data pushed by the source server.

- Ideally, the source server should be pushing changes to the "current" folder using rsync.  But in our case, the current server is an old Solaris 9 server without rsync.  Which means that our backups are likely to be about 2x to 3x larger then they should be.

- RDiff-Backup may have been a better solution for this particular problem (and we may switch).

- This shows a good example of how to calculate the current day of week number (0-6) as well as calculating what the previous day number was (using modulus arithmetic).

- I make no guarantees that permissions or ownership will be preserved.  But since the source server strips all of that information in the process of sending the files over the wire with scp, it's a moot point for our current situation.  (rdiff-backup is probably a better choice for that.)

```
#!/bin/bash
# DAILY BACKUPS (writes to a daily folder each day)
DAYNR=`date +%w`
echo DAYNR=${DAYNR}
let "PREVDAYNR = ((DAYNR + 6) % 7)"
echo PREVDAYNR=${PREVDAYNR}
DIRS="home local"

for DIR in ${DIRS}
do
    echo "----- ----- ----- -----"
    echo "Backup:" ${DIR}
    SRCDIR=/backup/cfmc1/$DIR/current/
    DESTDIR=/backup/cfmc1/$DIR/daily.${DAYNR}/
    PREVDIR=/backup/cfmc1/$DIR/daily.${PREVDAYNR}/
    echo SRCDIR=${SRCDIR}
    echo DESTDIR=${DESTDIR}
    echo PREVDIR=${PREVDIR}

    cp -al ${PREVDIR}* ${DESTDIR}
    rsync -a --delete-after ${SRCDIR} ${DESTDIR}

    echo "Done." 
done
```

It's not pretty, but it will work better once the source server starts pushing the daily changes via rsync instead of completely overwriting the "current" directory every day.

The code should be pretty self explanatory but I'll explain the two key lines.

cp -al ${PREVDIR}* ${DESTDIR}

This overwrites all files in ${DESTDIR}, which is today, with the files from yesterday, but does it by creating hard links of all files.  Old files which were deleted since last week will be left behind until the rsync step.

rsync -a --delete-after ${SRCDIR} ${DESTDIR}

This then brings today's folder up to date with any changes as compared to the source directory (a.k.a. "current").  It also deletes any file in today's folder that don't exist in the source directory.

References:

[Easy Automated Snapshot-Style Backups with Linux and Rsync](http://www.mikerubel.org/computers/rsync_snapshots/)

[Local incremental snap shots with rsync](http://www.synology.at/enu/forum/viewtopic.php?f=9&t=11471&p=48163)
