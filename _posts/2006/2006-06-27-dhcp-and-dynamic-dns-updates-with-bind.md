---
layout: post
title: 'DHCP and Dynamic DNS Updates with BIND'
date: '2006-06-27T15:46:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


After a few hours last night (and a lot of help from <i>DNS & BIND Cookbook</i>) I finally got my DHCP server on the Gentoo box to automatically add records to my local LAN's DNS zone.  It's not terribly difficult to do, just a little tricky until you get all the ducks in a row and put everything in the right place.

First off, I can't recommend enough making use of SubVersion to keep track of configuration / zone file changes.  It greatly simplifies things in case you have to revert to a previous version.  It's also a good way to get comfortable with SVN command-line usage because you're not doing anything complex (mostly 'svn add' and 'svn ci' commands).

Requirements (I will assume the following):
<ul>

<li>net-misc/dhcp-3.0.1-r1 or later 

</li>
<li>net-dns/bind-9.3.2 or later 

</li>
<li>net-dns/bind-tools-9.2.5 or later

</li>
<li>Simple network configuration using a single Class-C private network range

</li>
<li>You have SubVersion configured

</li>
<li>You have configured symbolic links to map /etc/named to /etc/bind (or vice-versa),  /var/named to /var/bind (or vice-versa), and /var/log/named to /var/log/bind (or vice-versa).

</li>
</ul>

Most home / small office networks use the DHCP server on the router (usually a LinkSys, D-Link, NetGear, etc. appliance between the internet and the internal LAN) and make use of their ISPs DNS servers.  This works well until you want to reference other machines on your local network by name.  Once you need that you should look into setting up DNS services and DHCP services on your Gentoo/Linux server.

A. The first step is to define your address range for your home network.  One suggestion that I make to ALL of my clients is that they use anything other then "0" in the 3rd octet (i.e. 192.168.0.XXX) of the network address range.  Having zero (or one) in the 3rd octet causes problems later if you want to link two network together using a VPN tunnel.  So while you're making the change-over to a new DHCP/DNS server you may as well change your network address assignments.

For the example network, I will be using an address range of: 192.168.102.XXX.  In addition, I've defined:

192.168.102.1 - The default gateway (internal address of the router)
192.168.102.2 - Static address of our Linux server
192.168.102.100 to .199 - DHCP address range

The DNS zone for my internal network is "lan.example.com", so each machine will get a DNS name of "machine-a.lan.example.com" when it gets assigned a DHCP address.  This makes it easy for one machine to contact another machine on the same network segment.

B. Make sure /etc/bind and /etc/dhcp are in SubVersion

```
# cd /etc
etc # svn add -N bind
etc # svn add -N named
etc # svn add -N dhcp
etc # svn ci -m "initial entry of dynamic DNS configuration"
etc # svn add bind/*
etc # svn add dhcp/*
etc # svn ci -m "initial entry of dynamic DNS configuration"
etc # cd /var
etc # svn add -N bind
etc # svn add -N named
etc # svn ci -m "initial entry of dynamic DNS configuration"
etc # cd /var/bind
bind # svn add *
bind # svn ci -m "initial entry of dynamic DNS configuration"
```

C. Create a symetric encryption (authentication?) key

In order for the DHCP server to update the DNS zone files in a secure manner, you need to create a symetric key using the "dnssec-keygen" command.  This key can be anywhere from 1 to 512 bits but I would recommend at least 128 bits if not 256 bits.  The "dnssec-keygen" command will create a pair of files that contain the key (since it's symetric encryption both files will have the same key).

```
# cd /etc/bind
bind # dnssec-keygen -a HMAC-MD5 -b 256 -n HOST dhcp.lan.example.com
Kdhcp.lan.example.com.+157+20479
bind # ls -l Kdhcp*
-rw-------  1 root root  84 Jun 27 16:24 Kdhcp.lan.example.com.+157+20479.key
-rw-------  1 root root 101 Jun 27 16:24 Kdhcp.lan.example.com.+157+20479.private
bind # cat Kdhcp.lan.example.com.+157+20479.key
dhcp.lan.example.com. IN KEY 512 3 157 swxJJ6mo6tAoSlAlUv6yGxvbCz5DKCLX1FF3U4Jl4Qc=
bind # cat Kdhcp.lan.example.com.+157+20479.private
Private-key-format: v1.2
Algorithm: 157 (HMAC_MD5)
Key: swxJJ6mo6tAoSlAlUv6yGxvbCz5DKCLX1FF3U4Jl4Qc=
bind # svn add K*
A         Kdhcp.lan.example.com.+157+20479.key
A         Kdhcp.lan.example.com.+157+20479.private
bind # svn ci -m "created DDNS update key"
Adding         bind/Kdhcp.lan.example.com.+157+20479.key
Adding         bind/Kdhcp.lan.example.com.+157+20479.private
Transmitting file data ..
Committed revision 10.
bind #
```

Nothing terribly complicated here.  Just make sure that you replace "dhcp.lan.example.com" with the name of your DHCP server's FQDN (fully qualified domain name).

D. Now we can construct the named.conf file.  I use a semi-complex method with sub-files in order to make things simpler in the long run.

You'll need to replace 192.168.102.XXX with your local LAN address as well as changing "dhcp.lan.example.com" to match the name of your DHCP server's FQDN.

```
bind # vim named.conf
options {
        directory "/var/named"; // sets root dir, use full path to escape
        statistics-file "/var/named/named.stats"; // stats are your friend
        dump-file "/var/named/named.dump";
        zone-statistics yes;
        allow-recursion { 127.0.0.1; 192.168.102.0/24; }; // allow recursive lookups
        // allow-transfer { 192.168.102.3; }; // allow transfers to these IP's
        // notify yes; // notify the above IP's when a zone is updated
        // location of pid file:
        pid-file "/var/run/named/named.pid";
        transfer-format many-answers; // Generates more efficient zone transfers
};

key dhcp.lan.example.com. {
        algorithm hmac-md5;
        secret "swxJJ6mo6tAoSlAlUv6yGxvbCz5DKCLX1FF3U4Jl4Qc=";
};

// Include logging config file
include "/var/named/conf/logging.conf";

// Include to ACLs
include "/var/named/conf/acls.conf";

// Include custom
include "/var/named/conf/lan.conf";
include "/var/named/conf/reverse.conf";
bind # svn ci -m "updating for DDNS"
```

E. Create the logging.conf and acls.conf files in /var/bind/conf.

```
# cd /var/bind/conf
conf # vim logging.conf
logging {

  channel default_file { file "/var/log/named/default.log" versions 3 size 5m; severity dynamic; print-time yes; };
  channel general_file { file "/var/log/named/general.log" versions 3 size 5m; severity dynamic; print-time yes; };
  channel database_file { file "/var/log/named/database.log" versions 3 size 5m; severity dynamic; print-time yes; };
  channel security_file { file "/var/log/named/security.log" versions 3 size 5m; severity dynamic; print-time yes; };
  channel config_file { file "/var/log/named/config.log" versions 3 size 5m; severity dynamic; print-time yes; };
  channel resolver_file { file "/var/log/named/resolver.log" versions 3 size 5m; severity dynamic; print-time yes; };
  channel xfer-in_file { file "/var/log/named/xfer-in.log" versions 3 size 5m; severity dynamic; print-time yes; };
  channel xfer-out_file { file "/var/log/named/xfer-out.log" versions 3 size 5m; severity dynamic; print-time yes; };
  channel notify_file { file "/var/log/named/notify.log" versions 3 size 5m; severity dynamic; print-time yes; };
  channel client_file { file "/var/log/named/client.log" versions 3 size 5m; severity dynamic; print-time yes; };
  channel unmatched_file { file "/var/log/named/unmatched.log" versions 3 size 5m; severity dynamic; print-time yes; };
  channel queries_file { file "/var/log/named/queries.log" versions 3 size 5m; severity dynamic; print-time yes; };
  channel network_file { file "/var/log/named/network.log" versions 3 size 5m; severity dynamic; print-time yes; };
  channel update_file { file "/var/log/named/update.log" versions 3 size 5m; severity dynamic; print-time yes; };
  channel dispatch_file { file "/var/log/named/dispatch.log" versions 3 size 5m; severity dynamic; print-time yes; };
  channel dnssec_file { file "/var/log/named/dnssec.log" versions 3 size 5m; severity dynamic; print-time yes; };
  channel lame-servers_file { file "/var/log/named/lame-servers.log" versions 3 size 5m; severity dynamic; print-time yes; };

  category default { default_file; };
  category general { general_file; };
  category database { database_file; };
  category security { security_file; };
  category config { config_file; };
  category resolver { resolver_file; };
  category xfer-in { xfer-in_file; };
  category xfer-out { xfer-out_file; };
  category notify { notify_file; };
  category client { client_file; };
  category unmatched { unmatched_file; };
  category queries { queries_file; };
  category network { network_file; };
  category update { update_file; };
  category dispatch { dispatch_file; };
  category dnssec { dnssec_file; };
  category lame-servers { lame-servers_file; };

};
conf # vim acls.conf
acl "our-networks" {
        192.168.102.0/24;
        127.0.0.1;
};
conf #
```

F. Create the two config files for the LAN and the reverse DNS.

```
# cd /var/bind/conf
conf # vim lan.conf
zone "lan.example.com" { 
        type master; 
        file "lan/lan.example.com"; 
        update-policy {
                grant dhcp.lan.example.com. wildcard *.lan.example.com. A TXT;
        };
};
conf # vim reverse.conf
zone "102.168.192.in-addr.arpa" { 
        type master; 
        file "reverse/192.168.102.0"; 
        update-policy {
                grant dhcp.lan.example.com. wildcard *.102.168.192.in-addr.arpa. PTR;
        };
};
conf # svn add *
conf # svn ci -m "updating config for DDNS"
```

Make sure that you set the user/group ownership of the config files to "named"

```
conf # ls -l *.conf
total 16
-rw-r--r--  1 named named   70 Dec 12  2005 acls.conf
-rw-r--r--  1 named named  214 Jun 27 18:28 lan.conf
-rw-r--r--  1 named named 2662 Dec 12  2005 logging.conf
-rw-r--r--  1 root  root   224 Jun 27 18:28 reverse.conf
conf # chown named *.conf
conf # chgrp named *.conf
```

G. Create the zone files for the forward and reverse DNS zones

Note: Remember to add folders and files to SubVersion and to assign the user/group to "named".

```
# cd /var/bind/lan
lan # vim lan.example.com
$ORIGIN .
$TTL 600        ; 10 minutes
lan.example.com         IN SOA  dhcp.lan.example.com. dns.example.com. (
                                2006062604 ; serial
                                3600       ; refresh (1 hour)
                                900        ; retry (15 minutes)
                                1209600    ; expire (2 weeks)
                                3600       ; minimum (1 hour)
                                )
                        NS      dhcp.lan.example.com.
                        A       192.168.102.2
$ORIGIN lan.example.com.
dhcp                    A       192.168.102.2
router                  A       192.168.102.1
localhost               A       127.0.0.1
lan # cd /var/bind/reverse
reverse # vim 192.168.102.0
$TTL 600
; 192.168.102.0 (reverse DNS)
@       IN      SOA     dhcp.lan.example.com. (
                        dns.example.com.
                        2006062602      ; serial
                        1h              ; refresh
                        15m             ; retry
                        2w              ; expire
                        1h              ; minimum
                        )
        IN      NS      dhcp.lan.example.com.

; static PTR records
2.102.168.192.in-addr.arpa.     IN      PTR     servername.lan.example.com.
2.102.168.192.in-addr.arpa.     IN      PTR     dhcp.lan.example.com.
reverse #
```

H. That should be it

That should be everything that is needed.  If not, leave me a note in a comment and I'll re-examine my notes.
