---
layout: post
title: 'SELinux is preventing named from write access'
date: '2007-07-05T20:55:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>It seems like the SELinux profile in CentOS5 may not be correct by default.  In my /var/log/messages file, I have thousands of entries per month consisting of:

Jul  4 05:01:04 fw1-hosho setroubleshoot:      SELinux is preventing /usr/sbin/named (named_t) "write" access to named (named_conf_t).      For complete SELinux messages. run sealert -l 663ea169-d194-4c49-a5bb-a6a4bb707990

Here's the output of the sealert command:

<pre># sealert -l 663ea169-d194-4c49-a5bb-a6a4bb707990
Summary
    SELinux is preventing /usr/sbin/named (named_t) "write" access to named
    (named_conf_t).

Detailed Description
    SELinux denied access requested by /usr/sbin/named. It is not expected that
    this access is required by /usr/sbin/named and this access may signal an
    intrusion attempt. It is also possible that the specific version or
    configuration of the application is causing it to require additional access.
    Please file a http://bugzilla.redhat.com/bugzilla/enter_bug.cgi against this
    package.

Allowing Access
    Sometimes labeling problems can cause SELinux denials.  You could try to
    restore the default system file context for named, restorecon -v named.
    There is currently no automatic way to allow this access. Instead, you can
    generate a local policy module to allow this access - see
    http://fedora.redhat.com/docs/selinux-faq-fc5/#id2961385 - or you can
    disable SELinux protection entirely for the application. Disabling SELinux
    protection is not recommended. Please file a
    http://bugzilla.redhat.com/bugzilla/enter_bug.cgi against this package.
    Changing the "named_disable_trans" boolean to true will disable SELinux
    protection this application: "setsebool -P named_disable_trans=1."

    The following command will allow this access:
    setsebool -P named_disable_trans=1

Additional Information        

Source Context                system_u:system_r:named_t
Target Context                root:object_r:named_conf_t
Target Objects                named [ dir ]
Affected RPM Packages         bind-9.3.3-8.el5 [application]
Policy RPM                    selinux-policy-2.4.6-30.el5
Selinux Enabled               True
Policy Type                   targeted
MLS Enabled                   True
Enforcing Mode                Enforcing
Plugin Name                   plugins.disable_trans
Host Name                     fw1-shimo.hq.example.org.
Platform                      Linux fw1-shimo.hq.example.org.
                              2.6.18-8.1.6.el5 #1 SMP Thu Jun 14 17:29:04 EDT
                              2007 x86_64 x86_64
Alert Count                   70481
Line Numbers                  

Raw Audit Messages            

avc: denied { write } for comm="named" dev=md1 egid=25 euid=25
exe="/usr/sbin/named" exit=-13 fsgid=25 fsuid=25 gid=25 items=0 name="named"
pid=2628 scontext=system_u:system_r:named_t:s0 sgid=25
subj=system_u:system_r:named_t:s0 suid=25 tclass=dir
tcontext=root:object_r:named_conf_t:s0 tty=(none) uid=25</pre>

The most helpful web page that I've found so far is the thread "[Permissions Issue starting Bind 9.3.1](http://www.webservertalk.com/message1323968.html)".  The gist seems to be that RedHat (and CentOS) are using a chroot bind installation in conjunction with an SELinux policy that expects the bind configuration files to be in a non-chroot setup.  But there aren't very clear instructions there on fixing it.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2007.shtml">2007</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/BIND9.shtml">BIND9</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/CentOS5.shtml">CentOS5</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/SELinux.shtml">SELinux</a>
		<div class="Byline">
			posted by Thomas at 
			[20:55](http://www.tgharold.com/techblog/2007/07/selinux-is-preventing-named-from-write.shtml)

		</div>