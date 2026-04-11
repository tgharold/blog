---
layout: post
title: 'SNMP and MRTG: Interesting OIDs in net-snmp'
date: '2009-12-06T18:26:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


These can all be found via the "snmpwalk" command in CentOS 5.4 (or RHEL 5.4).

```
# snmp -v 1 -c public localhost | less
```

The above assumes that you have configured the SNMP agent on the server to allow read-only access to SNMP v1 clients via the "public" community string.

<b>Approximate number of users logged in</b>

```
HOST-RESOURCES-MIB::hrSystemNumUsers.0 = Gauge32: 3
```

Number of logged in users.  As you can see, this is a gauge value which means (in SNMP terms) that it is a value that can increase or decrease over time.  By default, MRTG assumes that the value is monotonically increasing.

Note: Since MRTG only samples once every 5 minutes, this value is very approximate.

<b>Approximate number of system processes</b>

```
HOST-RESOURCES-MIB::hrSystemProcesses.0 = Gauge32: 171
```

Current number of processes running.  This often makes a good second number to pair up with the number of users.  Or you could choose to display them on separate graphs.

Note: Same issue as logging the number of users, MRTG only samples every 5 minutes which makes this an estimation at best.

<b>MRTG: Reporting on processes and users</b>

Here's a fragment from my MRTG configuration file that shows how I reported on the number of users and processes.  I could not get MRTG to resolve the plain names to OIDs automatically, so I had to put in the full numeric OIDs.

```
### PROCESSES &amp; USERS
Options[_]: gauge, integer, noborder, noinfo, nolegend, noo, nopercent, pngdate, printrouter, transparent
WithPeak[_]: ymw
Legend2[_]:
Legend3[_]:
Legend4[_]:

#Target[localhost.system.users]: hrSystemNumUsers.0&amp;hrSystemNumUsers.0:public@localhost
Target[localhost.system.users]: .1.3.6.1.2.1.25.1.5.0&amp;.1.3.6.1.2.1.25.1.5.0:public@localhost
MaxBytes[localhost.system.users]: 50
YLegend[localhost.system.users]: Users
LegendI[localhost.system.users]: Users
Legend1[localhost.system.users]: Approximate number of users logged in
ShortLegend[localhost.system.users]: ~
Title[localhost.system.users]: firewall:Users - Approximate System Users
PageTop[localhost.system.users]: &lt;h1&gt;firewall: Approximate System Users&lt;/h1&gt;
&#160;&#160;&#160;&#160;&lt;div id="sysdetails"&gt;
&#160;&#160;&#160;&#160;&lt;/div&gt;

#Target[localhost.system.processes]: hrSystemProcesses.0&amp;hrSystemProcesses.0:public@localhost
Target[localhost.system.processes]: .1.3.6.1.2.1.25.1.6.0&amp;.1.3.6.1.2.1.25.1.6.0:public@localhost
MaxBytes[localhost.system.processes]: 5000
YLegend[localhost.system.processes]: Processes
LegendI[localhost.system.processes]: Processes
Legend1[localhost.system.processes]: Approximate number of processes
ShortLegend[localhost.system.processes]: ~
Title[localhost.system.processes]: firewall:Procs - Approximate System Processes
PageTop[localhost.system.processes]: &lt;h1&gt;firewall: Approximate System Processes&lt;/h1&gt;
&#160;&#160;&#160;&#160;&lt;div id="sysdetails"&gt;
&#160;&#160;&#160;&#160;&lt;/div&gt;
```

<b>Real Memory in Use</b>

```
HOST-RESOURCES-MIB::hrStorageType.2 = OID: HOST-RESOURCES-TYPES::hrStorageRam
HOST-RESOURCES-MIB::hrStorageDescr.2 = STRING: Real Memory
HOST-RESOURCES-MIB::hrStorageAllocationUnits.2 = INTEGER: 1024 Bytes
HOST-RESOURCES-MIB::hrStorageSize.2 = INTEGER: 8043628
HOST-RESOURCES-MIB::hrStorageUsed.2 = INTEGER: 7962536
```

<b>Swap (Virtual) Memory in Use</b>

```
HOST-RESOURCES-MIB::hrStorageType.3 = OID: HOST-RESOURCES-TYPES::hrStorageVirtualMemory
HOST-RESOURCES-MIB::hrStorageDescr.3 = STRING: Swap Space
HOST-RESOURCES-MIB::hrStorageAllocationUnits.3 = INTEGER: 1024 Bytes
HOST-RESOURCES-MIB::hrStorageSize.3 = INTEGER: 4021814
HOST-RESOURCES-MIB::hrStorageUsed.3 = INTEGER: 8292
```

<b>Processor Utilization</b>

First, we need to find the OIDs of the CPUs.

```
# snmpwalk -v 1 -c public localhost | grep "HOST-RESOURCES" | egrep "hrDeviceProcessor"
HOST-RESOURCES-MIB::hrDeviceType.768 = OID: HOST-RESOURCES-TYPES::hrDeviceProcessor
HOST-RESOURCES-MIB::hrDeviceType.769 = OID: HOST-RESOURCES-TYPES::hrDeviceProcessor
HOST-RESOURCES-MIB::hrSWRunParameters.32755 = STRING: "hrDeviceProcessor"
```

That gives us 768 and 769 to look at.

```
# snmpwalk -v 1 -c public localhost | grep "HOST-RESOURCES" | egrep "(768|769)"        
HOST-RESOURCES-MIB::hrDeviceIndex.768 = INTEGER: 768
HOST-RESOURCES-MIB::hrDeviceIndex.769 = INTEGER: 769
HOST-RESOURCES-MIB::hrDeviceType.768 = OID: HOST-RESOURCES-TYPES::hrDeviceProcessor
HOST-RESOURCES-MIB::hrDeviceType.769 = OID: HOST-RESOURCES-TYPES::hrDeviceProcessor
HOST-RESOURCES-MIB::hrDeviceDescr.768 = STRING: AuthenticAMD: AMD Athlon(tm) 64 X2 Dual Core Processor 4200+
HOST-RESOURCES-MIB::hrDeviceDescr.769 = STRING: AuthenticAMD: AMD Athlon(tm) 64 X2 Dual Core Processor 4200+
HOST-RESOURCES-MIB::hrDeviceID.768 = OID: SNMPv2-SMI::zeroDotZero
HOST-RESOURCES-MIB::hrDeviceID.769 = OID: SNMPv2-SMI::zeroDotZero
HOST-RESOURCES-MIB::hrProcessorFrwID.768 = OID: SNMPv2-SMI::zeroDotZero
HOST-RESOURCES-MIB::hrProcessorFrwID.769 = OID: SNMPv2-SMI::zeroDotZero
HOST-RESOURCES-MIB::hrProcessorLoad.768 = INTEGER: 1
HOST-RESOURCES-MIB::hrProcessorLoad.769 = INTEGER: 1
```

So by looking at the hrProcessorLoad for nodes 768 &amp; 769, we can track the CPU utilization on this PC.  But unless you can get MRTG to load the MIBs, you'll need to use the numeric OID format.

```
# snmpwalk -v 1 -c public localhost -On | egrep "(768|769)" | grep "INTEGER"
.1.3.6.1.2.1.25.3.3.1.2.768 = INTEGER: 9
.1.3.6.1.2.1.25.3.3.1.2.769 = INTEGER: 17
```
