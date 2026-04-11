---
layout: post
title: 'lm_sensors and Gigabyte GA-6VA7+'
date: '2005-11-28T20:47:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Working on setting up lm_sensors on my Gigabyte GA-6VA7+ (Intel Celeron Coppermine 566Mhz CPU) system.  [First step](http://secure.netroedge.com/~lm78/kernel26.html) is to turn on I2C support in the 2.6 kernel configuration.

```
# cd /usr/src/linux
# make menuconfig
```

Device drivers
--> I2C Support
--> --> I2C Support (turn ON as BUILT-IN)
--> --> --> I2C device interface
--> --> --> --> (turn all sub-options on as MODULE)
--> --> --> I2C Algorithms
--> --> --> --> (turn all sub-options on as MODULE)
--> --> --> I2C Hardware Bus support  
--> --> --> --> (turn all sub-options on as MODULE)
--> --> Miscellaneous I2C Chip support
--> --> --> (turn all sub-options on as MODULE)
--> --> I2C Core debugging messages (turn ON as BUILT-IN)
--> --> I2C Algorithm debugging messages (turn ON as BUILT-IN)
--> --> I2C Bus debugging messages (turn ON as BUILT-IN)
--> --> I2C Chip debugging messages (turn ON as BUILT-IN)

Now, make sure that /boot is mounted, then compile your new kernel.

```
# make &amp;&amp; make modules_install
# mount /boot
# cp arch/i386/boot/bzImage /boot/kernel-2.6.13-28Nov2005-2037
# cp System.map /boot/System.map-2.6.13-28Nov2005-2037
# cp .config /boot/config-2.6.13-28Nov2005-2037
# nano -w /boot/grub/grub.conf
```

Now, this is just a testing configuration and not my final configuration.  After the boot, I'll have to figure out what sensors are actually available and which ones I need to keep.

```
# emerge -pv lm_sensors
# emerge lm_sensors
```

While that's compiling, read the [lm_sensors FAQ](http://www2.lm-sensors.nu/~lm78/cvs/lm_sensors2/doc/lm_sensors-FAQ.html).  Section 3.1 (Why so many modules, and how do I cope with them?) explains the basics of how to get started with lm_sensors.

(Notice the warnings at the end of the ebuild.)

```
>>> /etc/init.d/lm_sensors
 * 
 * Next you need to run:
 *   /usr/sbin/sensors-detect
 * to detect the I2C hardware of your system and create the file:
 *   /etc/conf.d/lm_sensors
 * 
 * You will also need to run the above command if you're upgrading from
 * <=lm_sensors-2.9.0, as the needed entries in /etc/conf.d/lm_sensors has
 * changed.
 * 
 * Be warned, the probing of hardware in your system performed by
 * sensors-detect could freeze your system. Also make sure you read
 * the documentation before running lm_sensors on IBM ThinkPads.
 * 
 * Please see the lm_sensors documentation and website for more information.
 * 
>>> Regenerating /etc/ld.so.cache...
>>> sys-apps/lm_sensors-2.9.2 merged.
(snip)

# /usr/sbin/sensors-detect
```

The following is output from my Gigabyte motherboard:

```
# sensors-detect revision 1.393 (2005/08/30 18:51:18)

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
 Do you want to probe now? (YES/no): yes
Probing for PCI bus adapters...
Use driver `i2c-matroxfb' for device 01:00.0: MGA G200 AGP
Use driver `i2c-viapro' for device 00:07.3: VIA Technologies VT82C596 Apollo ACPI
Probe succesfully concluded.

We will now try to load each adapter module in turn.
Load `i2c-matroxfb' (say NO if built into your kernel)? (YES/no): yes
FATAL: Module i2c_matroxfb not found.
Loading failed... skipping.
Load `i2c-viapro' (say NO if built into your kernel)? (YES/no): yes
Module loaded succesfully.
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
Client found at address 0x50
Probing for `SPD EEPROM'... Success!
    (confidence 8, driver `eeprom')
Probing for `DDC monitor'... Failed!
Probing for `Maxim MAX6900'... Failed!
Client found at address 0x51
Probing for `SPD EEPROM'... Success!
    (confidence 8, driver `eeprom')
Client found at address 0x52
Probing for `SPD EEPROM'... Success!
    (confidence 8, driver `eeprom')
Client found at address 0x69

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
Probing for `Winbond W83697HF'
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

 Now follows a summary of the probes I have just done.
 Just press ENTER to continue: 

Driver `eeprom' (should be inserted):
  Detects correctly:
  * Bus `SMBus Via Pro adapter at 5000'
    Busdriver `i2c-viapro', I2C address 0x50
    Chip `SPD EEPROM' (confidence: 8)
  * Bus `SMBus Via Pro adapter at 5000'
    Busdriver `i2c-viapro', I2C address 0x51
    Chip `SPD EEPROM' (confidence: 8)
  * Bus `SMBus Via Pro adapter at 5000'
    Busdriver `i2c-viapro', I2C address 0x52
    Chip `SPD EEPROM' (confidence: 8)

 I will now generate the commands needed to load the I2C modules.
 Sometimes, a chip is available both through the ISA bus and an I2C bus.
 ISA bus access is faster, but you need to load an additional driver module
 for it. If you have the choice, do you want to use the ISA bus or the
 I2C/SMBus (ISA/smbus)? isa

If you want to load the modules at startup, generate a config file
below and make sure lm_sensors gets started; e.g
$ rc-update add lm_sensors default.

To make the sensors modules behave correctly, add these lines to
/etc/modules.conf:

#----cut here----
# I2C module options
alias char-major-89 i2c-dev
#----end cut here----

WARNING! If you have some things built into your kernel, the list above
will contain too many modules. Skip the appropriate ones! You really should
try these commands right now to make sure everything is working properly.
Monitoring programs won't work until it's done.
To load everything that is needed, execute the commands above...

#----cut here----
# I2C adapter drivers
modprobe i2c-viapro
# I2C chip drivers
modprobe eeprom
# sleep 2 # optional
/usr/bin/sensors -s # recommended

Do you want to generate /etc/conf.d/lm_sensors? Enter s to specify other file name?
  (YES/no/s): yes
Done.
```

I had to add the rc-update command, but the /etc/modules.conf file already had the proper I2C line.

Hmm... got the "No sensors found!" error message.  Yet I'm 95% sure that I did everything according to directions.  Well, it is an older motherboard so I might be better off retrying setting up lm_sensors on a newer system.

Output from dmesg:

```
vt596_smbus 0000:00:07.3: using Interrupt SMI# for SMBus.
vt596_smbus 0000:00:07.3: SMBREV = 0x0
vt596_smbus 0000:00:07.3: VT596_smba = 0x5000
i2c_adapter i2c-0: registered as adapter #0
i2c-core: driver eeprom registered.
i2c_adapter i2c-0: found normal i2c entry for adapter 0, addr 50
i2c_adapter i2c-0: Transaction (pre): CNT=00, CMD=3f, ADD=a0, DAT0=06, DAT1=00
i2c_adapter i2c-0: SMBus busy (0x02). Resetting...
i2c_adapter i2c-0: Successfull!
i2c_adapter i2c-0: Transaction (post): CNT=00, CMD=3f, ADD=a0, DAT0=06, DAT1=00
i2c_adapter i2c-0: Transaction (pre): CNT=00, CMD=3f, ADD=a0, DAT0=06, DAT1=00
i2c_adapter i2c-0: Transaction (post): CNT=00, CMD=3f, ADD=a0, DAT0=06, DAT1=00
i2c_adapter i2c-0: client [eeprom] registered to adapter
registering 0-0050
i2c_adapter i2c-0: found normal i2c entry for adapter 0, addr 51
i2c_adapter i2c-0: Transaction (pre): CNT=00, CMD=3f, ADD=a2, DAT0=06, DAT1=00
i2c_adapter i2c-0: Transaction (post): CNT=00, CMD=3f, ADD=a2, DAT0=06, DAT1=00
i2c_adapter i2c-0: Transaction (pre): CNT=00, CMD=3f, ADD=a2, DAT0=06, DAT1=00
i2c_adapter i2c-0: Transaction (post): CNT=00, CMD=3f, ADD=a2, DAT0=06, DAT1=00
i2c_adapter i2c-0: client [eeprom] registered to adapter
registering 0-0051
i2c_adapter i2c-0: found normal i2c entry for adapter 0, addr 52
i2c_adapter i2c-0: Transaction (pre): CNT=00, CMD=3f, ADD=a4, DAT0=06, DAT1=00
i2c_adapter i2c-0: Transaction (post): CNT=00, CMD=3f, ADD=a4, DAT0=06, DAT1=00
i2c_adapter i2c-0: Transaction (pre): CNT=00, CMD=3f, ADD=a4, DAT0=06, DAT1=00
i2c_adapter i2c-0: Transaction (post): CNT=00, CMD=3f, ADD=a4, DAT0=06, DAT1=00
i2c_adapter i2c-0: client [eeprom] registered to adapter
registering 0-0052
i2c_adapter i2c-0: found normal i2c entry for adapter 0, addr 53
i2c_adapter i2c-0: Transaction (pre): CNT=00, CMD=3f, ADD=a6, DAT0=06, DAT1=00
i2c_adapter i2c-0: Error: no response!
i2c_adapter i2c-0: Transaction (post): CNT=00, CMD=3f, ADD=a6, DAT0=06, DAT1=00
i2c_adapter i2c-0: found normal i2c entry for adapter 0, addr 54
i2c_adapter i2c-0: Transaction (pre): CNT=00, CMD=3f, ADD=a8, DAT0=06, DAT1=00
i2c_adapter i2c-0: Error: no response!
i2c_adapter i2c-0: Transaction (post): CNT=00, CMD=3f, ADD=a8, DAT0=06, DAT1=00
i2c_adapter i2c-0: found normal i2c entry for adapter 0, addr 55
i2c_adapter i2c-0: Transaction (pre): CNT=00, CMD=3f, ADD=aa, DAT0=06, DAT1=00
i2c_adapter i2c-0: Error: no response!
i2c_adapter i2c-0: Transaction (post): CNT=00, CMD=3f, ADD=aa, DAT0=06, DAT1=00
i2c_adapter i2c-0: found normal i2c entry for adapter 0, addr 56
i2c_adapter i2c-0: Transaction (pre): CNT=00, CMD=3f, ADD=ac, DAT0=06, DAT1=00
i2c_adapter i2c-0: Error: no response!
i2c_adapter i2c-0: Transaction (post): CNT=00, CMD=3f, ADD=ac, DAT0=06, DAT1=00
i2c_adapter i2c-0: found normal i2c entry for adapter 0, addr 57
i2c_adapter i2c-0: Transaction (pre): CNT=00, CMD=3f, ADD=ae, DAT0=06, DAT1=00
i2c_adapter i2c-0: Error: no response!
i2c_adapter i2c-0: Transaction (post): CNT=00, CMD=3f, ADD=ae, DAT0=06, DAT1=00
```

Output from lsmod:

```
# lsmod
Module                  Size  Used by
eeprom                  5528  - 
i2c_sensor              2984  - 
i2c_viapro              7640  - 
dm_mod                 45340  - 
```
