---
layout: post
title: 'SNMP: Finding OIDs and MIBs'
date: '2009-09-07T18:45:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>The key tool in the toolbox for exploring MIBs and finding things in SNMP is either "snmpwalk" or looking at the actual MIB text definitions.  On CentOS 5 (and RHEL 5), the net-snmp package installs a default set of MIBs to "/usr/share/snmp/mibs/".

<code># snmpwalk -v 2c -c public localhost diskIONReadX</code>

That particular command uses version "2c" of the SNMP protocol to talk to the "public" community on the localhost and looks for "diskIONReadX" (which is a 64bit counter value column from the diskIOTable).

<code># snmptranslate -m +ALL -IR -Td diskIONReadX</code>

Here, we use "snmptranslate" to report on full details (-Td) of the diskIONReadX property.  When looking up SNMP attributes by labels, you'll want to use the above format, but you can change "-Td" to other "-T" options or a "-O" option.  Some common choices are:

<code># snmptranslate -m +ALL -IR <b>-Td</b> diskIONReadX
UCD-DISKIO-MIB::diskIONReadX
diskIONReadX OBJECT-TYPE
  -- FROM       UCD-DISKIO-MIB
  SYNTAX        Counter64
  MAX-ACCESS    read-only
  STATUS        current
  DESCRIPTION   "The number of bytes read from this device since boot."
::= { iso(1) org(3) dod(6) internet(1) private(4) enterprises(1) ucdavis(2021) ucdExperimental(13) ucdDiskIOMIB(15) diskIOTable(1) diskIOEntry(1) 12 }

# snmptranslate -m +ALL -IR <b>-On</b> diskIONReadX
.1.3.6.1.4.1.2021.13.15.1.1.12

# snmptranslate -m +ALL -IR <b>-Of</b> diskIONReadX
.iso.org.dod.internet.private.enterprises.ucdavis.ucdExperimental.
    ucdDiskIOMIB.diskIOTable.diskIOEntry.diskIONReadX

# snmptranslate -m +ALL -IR <b>-Ou</b> diskIONReadX
enterprises.ucdavis.ucdExperimental.ucdDiskIOMIB.diskIOTable.
    diskIOEntry.diskIONReadX</code><div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2009.shtml">2009</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/SNMP.shtml">SNMP</a>
		<div class="Byline">
			posted by Thomas at 
			[18:45](http://www.tgharold.com/techblog/2009/09/snmp-finding-oids-and-mibs.shtml)

		</div>