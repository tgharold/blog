---
layout: post
title: 'Postgresql 8.1 under a nondefault directory with SELinux'
date: '2008-03-10T13:42:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>So I like to keep my PostgreSQL install in a non-standard location.  Normally, this is as easy as setting PGDATA= in the /etc/sysconfig/pgsql/postgresql file.  But when SELinux is installed, you also have to deal with system context issues.

One symptom of this is that /etc/init.d/postgresql start will fail, but starting the database interactively using the "su postgres" and pg_ctl commands will work.  This is because SELinux is a lot stricter with programs started in the startup scripts vs programs that are started from an interactive shell.

If you dig through the pgsql-general mail archives, you'll find a thread titled "[GENERAL] Using an alternate PGDATA on RHEL4 with SELinux enabled" from July 2006.  Unfortunately, nobody posted the answer for how to work around this issue and the original poster merely disabled SELinux.  Tom Lane in particular says:

<i>The default selinux policy prevents postgres from writing anywhere except under /var/lib/pgsql.  If you want a nondefault PGDATA location then you have to tweak the policy.</i>

However, I've stumbled across this "[Just Someone Re: SELinux + CREATE TABLESPACE = ?](http://grokbase.com/profile/id:i205zPwbOTvfCFLTORsztb0iwVOTD_1h0v-YgVItCSg)" which gives some insights into the issue.  It was also posted to the pgsql-general mailing list, but about a week later. I quote "Just Someone":

<i>If you rather keep SELinux on, you can still set the SELinux context
on the directory where you want the tablespaces to one postgres will
like.

To find what is the permissions you need, you can use ls -Z. It will
list the SELinux context. Check /var/lib/pgsql/data (or wherever
postgres data is pointing to), and then set this same permission on
the target dir using chcon.

For example, on my FC4 system all subdirectories on the data directory have:
root:object_r:postgresql_db_t or user_u:object_r:postgresql_db_t

So if you want to chage /path/to/foo/which/is/not/under/pgdata, run
(as root or sudo):

chcon root:object_r:postgresql_db_t /path/to/foo/which/is/not/under/pgdata

This way postgres can access it, and you get the SELinux security.

Bye,

Guy. </i>

So basically, we need to look at the context of the existing /var/lib/pgsql folder and then make our new directories to match that.  We'll start by looking at /var/lib/pgsql:

<pre># ls -Z /var/lib/
drwx------  postgres  postgres system_u:object_r:var_lib_t      pgsql</pre>

Let's compare this to our new location:

<pre># ls -Z /var/
drwxr-xr-x  root   root   system_u:object_r:file_t         pgsql</pre>

Yeah, that's definitely not correct.  So let's fix it:

<pre># chown postgres:postgres /var/pgsql
# chmod 700 /var/pgsql
# chcon system_u:object_r:var_t /var/pgsql
# ls -Z /var/
drwx------  postgres postgres system_u:object_r:var_lib_t      pgsql</pre>

Which now matches exactly what we saw for /var/lib/pgsql.  Now we need to do the same thing for the contents of /var/pgsql as compared to /var/lib/pgsql.

<pre># ls -Z /var/lib/pgsql
drwx------  postgres postgres system_u:object_r:var_lib_t      backups
drwx------  postgres postgres system_u:object_r:postgresql_db_t data
-rw-------  postgres postgres system_u:object_r:postgresql_log_t pgstartup.log</pre>

As compared to:

<pre># ls -Z /var/pgsql
drwx------  postgres postgres user_u:object_r:var_log_t        data
drwx------  root     root     system_u:object_r:file_t         lost+found</pre>

Once again, things need to be fixed up.

<pre># su postgres
$ mkdir /var/pgsql/backups
$ chmod 700 /var/pgsql/backups
$ chcon system_u:object_r:var_t /var/pgsql/backups
$ chcon system_u:object_r:postgresql_db_t /var/pgsql/data
$ touch /var/pgsql/pgstartup.log
$ chmod 600 /var/pgsql/pgstartup.log
$ chcon system_u:object_r:postgresql_log_t /var/pgsql/pgstartup.log
$ ls -Z /var/pgsql
drwx------  postgres postgres system_u:object_r:var_t        backups
drwx------  postgres postgres system_u:object_r:postgresql_db_t data
drwx------  root     root     system_u:object_r:file_t         lost+found
-rw-------  postgres postgres system_u:object_r:postgresql_log_t pgstartup.log
$ ls -Z /var/lib/pgsql
drwx------  postgres postgres system_u:object_r:var_lib_t      backups
drwx------  postgres postgres system_u:object_r:postgresql_db_t data
-rw-------  postgres postgres system_u:object_r:postgresql_log_t pgstartup.log</pre>

Which looks correct.  At least our ownership, file attributes and file context all match the original.  Note that I left the context of some things as system_u:object_r:var_t instead of system_u:object_r:var_lib_t.

Now for the hard part, we have to look at ALL of the subdirectory contents under /var/lib/pgsql and match them up in the new location:

<pre>$ cd /var/lib/pgsql ; ls -RZ
.:
drwx------  postgres postgres system_u:object_r:var_lib_t      backups
drwx------  postgres postgres system_u:object_r:postgresql_db_t data
-rw-------  postgres postgres system_u:object_r:postgresql_log_t pgstartup.log

./backups:

./data:
drwx------  postgres postgres user_u:object_r:postgresql_db_t  base
drwx------  postgres postgres user_u:object_r:postgresql_db_t  global
drwx------  postgres postgres user_u:object_r:postgresql_db_t  pg_clog
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  pg_hba.conf
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  pg_ident.conf
drwx------  postgres postgres user_u:object_r:postgresql_db_t  pg_log
drwx------  postgres postgres user_u:object_r:postgresql_db_t  pg_multixact
drwx------  postgres postgres user_u:object_r:postgresql_db_t  pg_subtrans
drwx------  postgres postgres user_u:object_r:postgresql_db_t  pg_tblspc
drwx------  postgres postgres user_u:object_r:postgresql_db_t  pg_twophase
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  PG_VERSION
drwx------  postgres postgres user_u:object_r:postgresql_db_t  pg_xlog
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  postgresql.conf
-rw-------  postgres postgres system_u:object_r:postgresql_db_t postmaster.opts

./data/base:
drwx------  postgres postgres user_u:object_r:postgresql_db_t  1
drwx------  postgres postgres user_u:object_r:postgresql_db_t  10792
drwx------  postgres postgres user_u:object_r:postgresql_db_t  10793

./data/base/1:
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10287
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10289
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10293
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10295
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10299
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10301
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10302
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10304
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10305
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10307
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10308
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10310
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10723
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10725
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10727
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10728
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10730
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10732
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10733
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10735
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10737
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10738
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10740
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10742
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10743
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10745
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10747
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10748
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10750
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10752
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1247
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1248
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1249
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1250
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1255
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1259
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2600
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2601
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2602
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2603
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2604
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2605
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2606
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2607
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2608
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2609
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2610
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2611
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2612
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2613
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2614
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2615
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2616
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2617
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2618
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2619
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2620
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2650
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2651
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2652
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2653
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2654
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2655
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2656
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2657
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2658
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2659
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2660
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2661
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2662
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2663
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2664
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2665
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2666
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2667
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2668
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2669
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2670
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2673
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2674
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2675
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2678
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2679
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2680
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2681
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2682
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2683
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2684
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2685
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2686
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2687
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2688
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2689
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2690
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2691
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2692
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2693
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2696
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2699
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2700
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2701
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2702
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2703
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2704
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  PG_VERSION

./data/base/10792:
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10287
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10289
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10293
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10295
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10299
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10301
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10302
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10304
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10305
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10307
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10308
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10310
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10723
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10725
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10727
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10728
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10730
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10732
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10733
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10735
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10737
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10738
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10740
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10742
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10743
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10745
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10747
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10748
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10750
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10752
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1247
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1248
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1249
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1250
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1255
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1259
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2600
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2601
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2602
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2603
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2604
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2605
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2606
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2607
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2608
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2609
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2610
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2611
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2612
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2613
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2614
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2615
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2616
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2617
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2618
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2619
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2620
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2650
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2651
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2652
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2653
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2654
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2655
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2656
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2657
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2658
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2659
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2660
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2661
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2662
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2663
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2664
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2665
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2666
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2667
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2668
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2669
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2670
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2673
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2674
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2675
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2678
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2679
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2680
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2681
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2682
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2683
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2684
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2685
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2686
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2687
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2688
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2689
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2690
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2691
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2692
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2693
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2696
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2699
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2700
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2701
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2702
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2703
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2704
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  PG_VERSION

./data/base/10793:
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10287
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10289
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10293
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10295
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10299
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10301
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10302
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10304
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10305
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10307
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10308
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10310
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10723
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10725
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10727
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10728
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10730
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10732
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10733
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10735
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10737
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10738
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10740
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10742
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10743
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10745
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10747
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10748
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10750
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10752
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1247
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1248
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1249
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1250
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1255
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1259
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2600
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2601
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2602
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2603
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2604
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2605
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2606
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2607
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2608
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2609
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2610
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2611
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2612
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2613
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2614
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2615
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2616
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2617
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2618
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2619
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2620
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2650
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2651
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2652
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2653
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2654
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2655
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2656
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2657
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2658
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2659
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2660
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2661
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2662
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2663
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2664
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2665
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2666
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2667
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2668
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2669
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2670
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2673
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2674
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2675
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2678
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2679
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2680
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2681
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2682
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2683
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2684
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2685
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2686
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2687
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2688
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2689
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2690
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2691
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2692
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2693
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2696
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2699
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2700
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2701
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2702
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2703
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2704
-rw-------  postgres postgres system_u:object_r:postgresql_db_t pg_internal.init
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  PG_VERSION

./data/global:
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10290
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10292
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10296
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  10298
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1136
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1137
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1213
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1214
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1232
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1233
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1260
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1261
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  1262
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2671
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2672
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2676
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2677
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2694
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2695
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2697
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  2698
-rw-------  postgres postgres system_u:object_r:postgresql_db_t pg_auth
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  pg_control
-rw-------  postgres postgres system_u:object_r:postgresql_db_t pg_database
-rw-------  postgres postgres system_u:object_r:postgresql_db_t pg_fsm.cache
-rw-------  postgres postgres system_u:object_r:postgresql_db_t pgstat.stat

./data/pg_clog:
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  0000

./data/pg_log:
-rw-------  postgres postgres system_u:object_r:postgresql_db_t postgresql-Mon.log
-rw-------  postgres postgres system_u:object_r:postgresql_db_t postgresql-Sat.log
-rw-------  postgres postgres system_u:object_r:postgresql_db_t postgresql-Sun.log
-rw-------  postgres postgres system_u:object_r:postgresql_db_t postgresql-Tue.log

./data/pg_multixact:
drwx------  postgres postgres user_u:object_r:postgresql_db_t  members
drwx------  postgres postgres user_u:object_r:postgresql_db_t  offsets

./data/pg_multixact/members:
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  0000

./data/pg_multixact/offsets:
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  0000

./data/pg_subtrans:
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  0000

./data/pg_tblspc:

./data/pg_twophase:

./data/pg_xlog:
-rw-------  postgres postgres user_u:object_r:postgresql_db_t  000000010000000000000000
drwx------  postgres postgres user_u:object_r:postgresql_db_t  archive_status

./data/pg_xlog/archive_status:
$</pre>

Keep that list open in a text editor, or something else because you'll need to refer to it frequently.  We can fix most of it by making everything set to context "user_u:object_r:postgresql_db_t" to start.  Which is a brute-force approach.

$ chcon -R user_u:object_r:postgresql_db_t *

Now we can go and start fixing things that should not be that particular context.  Now, it's quite probable that this is overkill, but I believe in being thorough.

<pre>$ chcon system_u:object_r:postgresql_db_t postmaster.opts
$ find . -name pg_internal.init -exec chcon system_u:object_r:postgresql_db_t {} \;
$ chcon system_u:object_r:postgresql_db_t global/pg_auth
$ chcon system_u:object_r:postgresql_db_t global/pg_database
$ chcon system_u:object_r:postgresql_db_t global/pg_fsm.cache
(file may not exist)
$ chcon system_u:object_r:postgresql_db_t global/pgstat.stat
$ chcon system_u:object_r:postgresql_db_t pg_log/postgresql-*.log</pre>

At this point, your postgresql data directory SHOULD be configured correctly.  (No guarantees!)  So now you can restart postgresql (/etc/init.d/postgresql start) and it will work properly in the new location.

Notes:

- Tested on CentOS 5 (or CentOS 5.1), it should also work on RedHat Linux.

- If you ever re-tag the entire filesystem with SELinux, you will (probably) have to go back and re-tag your postgresql data directory.

- Because of the above note, it may be better to mount the LVM or SAN partition for PostgreSQL at the default location of /var/lib/pgsql instead of forcing it into another location.  On the other hand, as long as you know how to fix it and don't re-tag indiscriminately, SELinux should never get in the way again.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2008.shtml">2008</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/PostgreSQL.shtml">PostgreSQL</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/SELinux.shtml">SELinux</a>
		<div class="Byline">
			posted by Thomas at 
			[13:42](http://www.tgharold.com/techblog/2008/03/postgresql-81-under-nondefault.shtml)

		</div>