---
layout: post
title: 'Gentoo: Setting up PostgreSQL'
date: '2004-07-09T00:12:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Getting PostgreSQL installed really isn't that difficult on Gentoo Linux.
```
# emerge -s postgresql
# emerge postgresql
(install takes a while, didn't time it)
# ebuild /var/db/pkg/dev-db/postgresql-7.4.2-r1/postgresql-7.4.2-r1.ebuild config
(a few messages later)
 * The current value of SHMMAX is too low for postgresql to run.
 * Please edit /etc/sysctl.conf and set this value to at least 134217728.
 * 
 *   kernel.shmmax = 134217728
 * 
```

Fire up nano... see [for an explanation of why we need to edit sysctl.conf](http://developer.postgresql.org/docs/postgres/kernel-resources.html).  The short version is that the 2.6 linux kernel has a default value (shared memory limits) that is too small to be compatible with PostgreSQL.
```
# nano -w /etc/sysctl.conf
```

(add the following lines)
```
#Kernel parameters for PostgreSQL
#default is 32MB, PostGreSQL needs 128MB
kernel.shmmax = 134217728
kernel.shmall = 134217728
```

Now manually update the current values and start the server.
```
# echo 134217728 &gt;/proc/sys/kernel/shmall
# echo 134217728 &gt;/proc/sys/kernel/shmmax
# rc-update add postgresql default
# /etc/init.d/postgresql start
```

Now I'm off to explore the [PostgreSQL documentation](http://www.postgresql.org/docs/7.4/interactive/).

The default Gentoo install seems to already include a "postgres" user in /etc/passwd.  To get logged in as the postgres user account, you will (I think) first need to switch to root.  
```
# su
# cd /usr/local
# su - postgres
```

Now you can continue with [section 16](http://www.postgresql.org/docs/7.4/interactive/creating-cluster.html).  Skip the page about creating the database cluster, it's already been created in "<b>/var/lib/postgresql/data</b>" back when you ran the "ebuild config" command.  You can verify this by looking at the config file ("<b>cat /etc/conf.d/postgresql</b>"), where the <b>PGDATA=</b> line indicates the location of the database.  

In fact, skip straight to [chapter 16.4 - Run-time Configuration](http://www.postgresql.org/docs/7.4/interactive/runtime-config.html), because the server is already running.  To verify that the server is running, "<b>cat /var/lib/postgresql/data/postmaster.pid</b>".  Make a note of the PID on the first line (second line is the database location), then "<b>cat /proc/nnnn/status</b>" (replacing "nnnn" with the PID).
