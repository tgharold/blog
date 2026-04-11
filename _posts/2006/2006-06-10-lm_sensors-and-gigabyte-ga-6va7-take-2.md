---
layout: post
title: 'lm_sensors and Gigabyte GA-6VA7+ (take 2)'
date: '2006-06-10T21:11:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


A while back I had tried to [configure lm_sensors on an old Gigabyte GA-6VA7+ motherboard](/blog/2005-11-28-lm_sensors-and-gigabyte-ga-6va7/).  That didn't work out so well, so I'm going to give it another shot.  Which is important because I had a drive overheat this week due to a failed fan.

There's a new version of lm_sensors out (2.10) while I'm still running the old 2.09.  Most of the steps are the same, I'm simply emerging the new version and then following the instructions.  On my slow little 566Mhz Celeron box, this takes a while.  Especially since I'm also rebuilding a failed raid element (thank goodness for Software RAID).

Output of the end of the emerge process:

```
&gt;&gt;&gt; /etc/init.d/fancontrol
 * 
 * Next you need to run:
 *   /usr/sbin/sensors-detect
 * to detect the I2C hardware of your system and create the file:
 *   /etc/conf.d/lm_sensors
 * 
 * You will also need to run the above command if you're upgrading from
 * &lt;=lm_sensors-2.9.0, as the needed entries in /etc/conf.d/lm_sensors has
 * changed.
 * 
 * Be warned, the probing of hardware in your system performed by
 * sensors-detect could freeze your system. Also make sure you read
 * the documentation before running lm_sensors on IBM ThinkPads.
 * 
 * Please see the lm_sensors documentation and website for more information.
 * 
&gt;&gt;&gt; Regenerating /etc/ld.so.cache...
&gt;&gt;&gt; sys-apps/lm_sensors-2.10.0 merged.

 sys-apps/lm_sensors
    selected: 2.9.2
   protected: 2.10.0
     omitted: none

&gt;&gt;&gt; 'Selected' packages are slated for removal.
&gt;&gt;&gt; 'Protected' and 'omitted' packages will not be removed.

&gt;&gt;&gt; Waiting 5 seconds before starting...
&gt;&gt;&gt; (Control-C to abort)...
&gt;&gt;&gt; Unmerging in: 5 4 3 2 1 
&gt;&gt;&gt; Unmerging sys-apps/lm_sensors-2.9.2...
No package files given... Grabbing a set.
--- !mtime obj /usr/share/man/man8/sensors-detect.8.gz
...
(snip)
...
--- !targe sym /usr/lib/libsensors.so
&gt;&gt;&gt; Regenerating /etc/ld.so.cache...
&gt;&gt;&gt; Regenerating /etc/ld.so.cache...
&gt;&gt;&gt; Auto-cleaning packages ...

&gt;&gt;&gt; No outdated packages were found on your system.

 * GNU info directory index is up-to-date.
 * IMPORTANT: 14 config files in /etc need updating.
 * Type emerge --help config to learn how to update config files.

#
```

Output of the sensors-detect phase:

```
# /usr/sbin/sensors-detect
# sensors-detect revision 1.413 (2006/01/19 20:28:00)

This program will help you determine which I2C/SMBus modules you need to
load to use lm_sensors most effectively. You need to have i2c and
lm_sensors installed before running this program.
Also, you need to be `root', or at least have access to the /dev/i2c-*
files, for most things.
If you have patched your kernel and have some drivers built in, you can
safely answer NO if asked to load some modules. In this case, things may
seem a bit confusing, but they will still work.

It is generally safe and recommended to accept the default answers to all
questions, unless you know what you're doing.

 We can start with probing for (PCI) I2C or SMBus adapters.
 You do not need any special privileges for this.
 Do you want to probe now? (YES/no): Yes
Probing for PCI bus adapters...
Use driver `i2c-matroxfb' for device 01:00.0: MGA G200 AGP
Use driver `i2c-viapro' for device 00:07.3: VIA Technologies VT82C596 Apollo ACPI
Probe succesfully concluded.

We will now try to load each adapter module in turn.
Load `i2c-matroxfb' (say NO if built into your kernel)? (YES/no): yes
FATAL: Module i2c_matroxfb not found.
Loading failed... skipping.
Module `i2c-viapro' already loaded.
If you have undetectable or unsupported adapters, you can have them
scanned by manually loading the modules before running this script.

 To continue, we need module `i2c-dev' to be loaded.
 If it is built-in into your kernel, you can safely skip this.
 i2c-dev is not loaded. Do you want to load it now? (YES/no): yes
 Module loaded succesfully.

 We are now going to do the adapter probings. Some adapters may hang halfway
 through; we can't really help that. Also, some chips will be double detected;
 we choose the one with the highest confidence value in that case.
 If you found that the adapter hung after probing a certain address, you can
 specify that address to remain unprobed. That often
 includes address 0x69 (clock chip).

Next adapter: SMBus Via Pro adapter at 5000
Do you want to scan it? (YES/no/selectively): yes
Client at address 0x50 can not be probed - unload all client drivers first!
Client at address 0x51 can not be probed - unload all client drivers first!
Client at address 0x52 can not be probed - unload all client drivers first!
Client found at address 0x69

Next adapter: ISA main adapter
Do you want to scan it? (YES/no/selectively): yes

Some chips are also accessible through the ISA bus. ISA probes are
typically a bit more dangerous, as we have to write to I/O ports to do
this. This is usually safe though.

Do you want to scan the ISA bus? (YES/no): yes
Probing for `National Semiconductor LM78'
  Trying address 0x0290... Failed!
Probing for `National Semiconductor LM78-J'
  Trying address 0x0290... Failed!
Probing for `National Semiconductor LM79'
  Trying address 0x0290... Failed!
Probing for `Winbond W83781D'
  Trying address 0x0290... Failed!
Probing for `Winbond W83782D'
  Trying address 0x0290... Failed!
Probing for `Winbond W83627HF'
  Trying address 0x0290... Failed!
Probing for `Winbond W83627EHF'
  Trying address 0x0290... Failed!
Probing for `Silicon Integrated Systems SIS5595'
  Trying general detect... Failed!
Probing for `VIA Technologies VT82C686 Integrated Sensors'
  Trying general detect... Failed!
Probing for `VIA Technologies VT8231 Integrated Sensors'
  Trying general detect... Failed!
Probing for `ITE IT8712F'
  Trying address 0x0290... Failed!
Probing for `ITE IT8705F / SiS 950'
  Trying address 0x0290... Failed!
Probing for `IPMI BMC KCS'
  Trying address 0x0ca0... Failed!
Probing for `IPMI BMC SMIC'
  Trying address 0x0ca8... Failed!

Some Super I/O chips may also contain sensors. Super I/O probes are
typically a bit more dangerous, as we have to write to I/O ports to do
this. This is usually safe though.

Do you want to scan for Super I/O sensors? (YES/no): yes
Probing for `ITE 8702F Super IO Sensors'
  Failed! (skipping family)
Probing for `Nat. Semi. PC87351 Super IO Fan Sensors'
  Failed! (skipping family)
Probing for `SMSC 47B27x Super IO Fan Sensors'
  Failed! (skipping family)
Probing for `VT1211 Super IO Sensors'
  Failed! (skipping family)
Probing for `Winbond W83627EHF/EHG Super IO Sensors'
  Failed! (skipping family)

Do you want to scan for secondary Super I/O sensors? (YES/no): yes
Probing for `ITE 8702F Super IO Sensors'
  Failed! (skipping family)
Probing for `Nat. Semi. PC87351 Super IO Fan Sensors'
  Failed! (skipping family)
Probing for `SMSC 47B27x Super IO Fan Sensors'
  Failed! (skipping family)
Probing for `VT1211 Super IO Sensors'
  Failed! (skipping family)
Probing for `Winbond W83627EHF/EHG Super IO Sensors'
  Failed! (skipping family)

 Sorry, no chips were detected.
 Either your sensors are not supported, or they are
 connected to an I2C bus adapter that we do not support.
 See doc/FAQ, doc/lm_sensors-FAQ.html, or
 http://www2.lm-sensors.nu/~lm78/cvs/lm_sensors2/doc/lm_sensors-FAQ.html
 (FAQ #4.24.3) for further information.
 If you find out what chips are on your board, see
 http://secure.netroedge.com/~lm78/newdrivers.html for driver status.
#
```

Mmm, doesn't look good, does it?

The chips that I know are on this motherboard (VIA Apollo chipset series) are:

Winbond 83977 (I/O chipset)
VIA VT82C596B
VIA VT82C693A

Hmm... those VIA chips are [supposedly supported](http://secure.netroedge.com/~lm78/supported.html) via the [i2c-viapro](http://www2.lm-sensors.nu/~lm78/cvs/lm_sensors2/doc/busses/i2c-viapro) module.  I'll need to reboot at some point and check out my BIOS settings to make sure the proper things are turned on.
