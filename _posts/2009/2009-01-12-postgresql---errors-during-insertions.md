---
layout: post
title: 'PostgreSQL - Errors during insertions'
date: '2009-01-12T11:43:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


ERROR:  could not access status of transaction 84344832
DETAIL:  Could not open file "pg_clog/0050": No such file or directory.

ERROR:  could not access status of transaction 84344832
DETAIL:  Could not open file "pg_clog/0050": No such file or directory.

Running into this issue while doing heavy inserts on a table.  The error also shows up when doing a "vacuum analyze" on the table.  This is with PostgreSQL 8.3.5.

Well, troubleshooting steps.

1) `# grep "was terminated" /var/lib/pgsql/data/pg_log/*.log`

<code>postgresql-2008-12-23_125649.log:LOG:  server process (PID 15996) was terminated by signal 6: Aborted

postgresql-2008-12-28_131324.log:LOG:  server process (PID 25745) was terminated by signal 6: Aborted

postgresql-2009-01-01_212245.log:LOG:  startup process (PID 27003) was terminated by signal 6: Aborted

postgresql-2009-01-01_212334.log:LOG:  startup process (PID 27097) was terminated by signal 6: Aborted</code>

All of my terminate statements are due to "signal 6: aborted", so I don't think there's anything to be seen there.

2) Going to look for "Could not open file" in the log files.  The command is: 

    # grep "Could not open file" /var/lib/pgsql/data/pg_log/*.log

<pre>postgresql-2009-01-11_000000.log:DETAIL:  Could not open file "pg_clog/0050": No such file or directory.

postgresql-2009-01-11_000000.log:DETAIL:  Could not open file "pg_clog/0050": No such file or directory.

postgresql-2009-01-11_170257.log:DETAIL:  Could not open file "pg_clog/0050": No such file or directory.

postgresql-2009-01-11_172436.log:DETAIL:  Could not open file "pg_clog/0050": No such file or directory.

postgresql-2009-01-12_000000.log:DETAIL:  Could not open file "pg_clog/0050": No such file or directory.</pre>

Which is the errors that I'm seeing.  They started on Jan 11th.

...

Fix attempt #1

A) Shutdown the database, make sure you have good backups.

B) Find out the size of the pg_clog files.  The following shows that ours are 256KB in size.

    # ls -lk /var/lib/pgsql/data/pg_clog/ | head

    -rw------- 1 postgres postgres 256 Dec 29 17:56 007E
    -rw------- 1 postgres postgres 256 Dec 29 19:05 007F
    -rw------- 1 postgres postgres 256 Dec 29 20:15 0080
    -rw------- 1 postgres postgres 256 Dec 29 21:23 0081
    -rw------- 1 postgres postgres 256 Dec 29 22:29 0082
    -rw------- 1 postgres postgres 256 Dec 29 23:23 0083
    -rw------- 1 postgres postgres 256 Dec 30 00:15 0084
    -rw------- 1 postgres postgres 256 Dec 30 01:08 0085

C) Create the missing clog file:

    # dd if=/dev/zero of=/var/lib/pgsql/data/pg_clog/0050 bs=1k count=256
    # chmod 600 /var/lib/pgsql/data/pg_clog/0050
    # chown postgres:postgres /var/lib/pgsql/data/pg_clog/0050

D) Restart the pgsql service.

...

Final notes.  This is probably absolutely NOT the proper way to fix this error.  Proceed at your own risk.  The chance of lost data is VERY HIGH.

For us, it was a table that was append only, that we were filling out with test data.  So I'm not all that concerned.
