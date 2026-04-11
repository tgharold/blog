---
layout: post
title: 'SELinux - troubleshooting file labeling issues'
date: '2009-02-05T07:03:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


This is a follow-up to [SELinux - dealing with exceptions](/blog/2008-09-30-selinux---dealing-with-exceptions/).

First off, a few basics:

<b>chcon</b> should only be used for <b>temporary</b> changes.  See [SELinux Contexts - Labeling Files](http://docs.fedoraproject.org/selinux-user-guide/f10/en-US/sect-Security-Enhanced_Linux-Working_with_SELinux-SELinux_Contexts_Labeling_Files.html).  Changes made with <b>chcon</b> will not survive a file system relabeling or use of the <b>restorecon</b> command.

<b>/usr/sbin/semanage fcontext</b> will <b>permanently</b> change the file context in a manner that will survive a relabel or restorecon. See [5.7.2. Persistent Changes: semanage fcontext](http://docs.fedoraproject.org/selinux-user-guide/f10/en-US/sect-Security-Enhanced_Linux-SELinux_Contexts_Labeling_Files-Persistent_Changes_semanage_fcontext.html) in the Fedora 10 documentation.

<b>How do I find out what file labels were defined already for a package?</b>

This is a bit trickier, but the key lies in looking under the following directory tree:

/etc/selinux/targeted/contexts/

For file labels, look at the file_context* files under:

/etc/selinux/targeted/contexts/files/

For example, I want to see what file contexts are defined for Nagios:

```
# grep -h "nagios" /etc/selinux/targeted/contexts/files/file_contexts*
/usr/lib(64)?/nagios/cgi(/.*)?  system_u:object_r:httpd_nagios_script_exec_t:s0
/usr/lib(64)?/nagios/plugins(/.*)?      system_u:object_r:bin_t:s0
/usr/lib(64)?/nagios/cgi-bin(/.*)?      system_u:object_r:httpd_nagios_script_exec_t:s0
/usr/lib(64)?/cgi-bin/nagios(/.+)?      system_u:object_r:httpd_nagios_script_exec_t:s0
/usr/lib(64)?/cgi-bin/netsaint(/.*)?    system_u:object_r:httpd_nagios_script_exec_t:s0
/etc/nagios(/.*)?       system_u:object_r:nagios_etc_t:s0
/var/log/nagios(/.*)?   system_u:object_r:nagios_log_t:s0
/var/log/netsaint(/.*)? system_u:object_r:nagios_log_t:s0
/var/spool/nagios(/.*)? system_u:object_r:nagios_spool_t:s0
/usr/bin/nagios --      system_u:object_r:nagios_exec_t:s0
/etc/nagios/nrpe\.cfg   --      system_u:object_r:nrpe_etc_t:s0
```

You can also use the <b>seinfo</b> tool:

```
# seinfo -t | grep "nagios"
Rule loading disabled
   nagios_spool_t
   httpd_nagios_script_ra_t
   httpd_nagios_script_ro_t
   httpd_nagios_script_rw_t
   nagios_t
   httpd_nagios_script_t
   nagios_tmp_t
   httpd_nagios_htaccess_t
   nagios_var_run_t
   httpd_nagios_content_t
   nagios_exec_t
   httpd_nagios_script_exec_t
   nagios_etc_t
   nagios_log_t
```

Another tool is sesearch, i.e.: 

```
# sesearch -a | grep "nagios" | sort | uniq
```

<b>Troubleshooting and fixing things</b>

Thus, step #1 is generally that we need to figure out whether (A) the AVC denial was caused by a mislabeled file.  And if so, we need to change the file label.

Here's an example of what setroubleshoot log messages look like in the /var/log/messages file.

```
# grep "setroubleshoot" /var/log/messages
setroubleshoot: SELinux is preventing the status.cgi from using potentially mislabeled files ./objects.cache (var_t). For complete SELinux messages. run sealert -l ce49f540-0b35-412c-862c-b901a274a421

setroubleshoot: SELinux is preventing ping (ping_t) "read write" to /var/nagios/spool/checkresults/checkZKmcmr (var_t). For complete SELinux messages. run sealert -l cf227199-1595-4775-9970-3935fc761b38

setroubleshoot: SELinux is preventing ping (ping_t) "read write" to /var/nagios/spool/checkresults/checke4tQgY (var_t). For complete SELinux messages. run sealert -l dbdc707e-193a-4f64-9bf2-0bb0d0a807e9
```

And here's what they look like in /var/log/audit:

```
# grep "AVC" /var/log/audit/audit.log | tail

type=AVC msg=audit(1233836684.122:15494): avc:  denied  { read } for  pid=12081 comm="status.cgi" name="objects.cache" dev=md1 ino=1306897 scontext=system_u:system_r:httpd_nagios_script_t:s0 tcontext=user_u:object_r:var_t:s0 tclass=file

type=AVC msg=audit(1233836426.120:15476): avc:  denied  { read write } for  pid=7518 comm="ping" path="/var/nagios/spool/checkresults/checkZKmcmr" dev=md1 ino=1306899 scontext=user_u:system_r:ping_t:s0 tcontext=user_u:object_r:var_t:s0 tclass=file

type=AVC msg=audit(1233836366.097:15454): avc:  denied  { read write } for  pid=20671 comm="ping" path="/var/nagios/spool/checkresults/checke4tQgY" dev=md1 ino=1306899 scontext=user_u:system_r:ping_t:s0 tcontext=user_u:object_r:var_t:s0 tclass=file
```

In this particular case, the fact that the target context is "var_t" generally indicates a labeling issue.  The "var_t" file context is pretty generic and we don't want to give the source context (httpd_nagios_script_t) for status.cgi permissions to all files labeled with var_t (which would be most of /var).

This means that using audit2allow is the <b>wrong</b> fix for this particular issue.

The correct solution is to either find out what file context should be used, or create a context and grant nagios access to those files.

References:

[Fedora 10 Security-Enhanced Linux User Guide](http://docs.fedoraproject.org/selinux-user-guide/f10/en-US/index.html)

[Top three things to understand in fixing SELinux problems. Reposted](http://danwalsh.livejournal.com/22347.html)

[Fedora SELinux Project Pages (wiki)](http://fedoraproject.org/wiki/SELinux)

[Red Hat Enterprise Linux 4: Red Hat SELinux Guide](http://www.redhat.com/docs/manuals/enterprise/RHEL-4-Manual/selinux-guide/rhlcommon-chapter-0007.html)

[How to: Install and Setup XEN Virtualization Software on CentOS Linux 5](http://www.cyberciti.biz/tips/rhel-centos-xen-virtualization-installation-howto.html) - Covers how to use semanage to grant the Xen process access to a directory where it will store the DomU storage as files.
