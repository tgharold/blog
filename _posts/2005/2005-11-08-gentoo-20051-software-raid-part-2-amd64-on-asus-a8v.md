---
layout: post
title: 'Gentoo 2005.1 Software RAID (part 2) AMD64 on Asus A8V'
date: '2005-11-08T17:06:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


This is a record of the kernel flags that I'm going to use for my AMD64 system.  It's an Asus A8V (K8T800Pro and VT8237) with an Athlon64 3200+ chip along with 2GB of RAM.  Hard drives are hooked up to the onboard Promise controller (PDC20378), the onboard SATA controller and the onboard IDE controller.  Plus the motherboard has an onboard gigabit ethernet NIC (Marvell 88E8001).

In addition, I have even more hard drives hooked up to a Promise Ultra133 TX2 PCI card (PDC20269) and some HighPoint Rocket133SB PCI cards (HPT302).

```
# emerge mdadm
# emerge lvm2
# cd /usr/src/linux
# make menuconfig
```

Linux Kernel v2.6.13-gentoo-r5 Configuration
(C)ode maturity level options
(G)eneral setup
(L)oadable module support
(P)rocessor type and features
--> (P)rocessor family (changed to "AMD-Opteron/Athlon64")
--> (S)ymetric multi-processing support (turned this one OFF)
(P)ower management options (ACPI, APM)
(B)us options (PCI, etc.)
(E)xecutable file formats
(D)evice drivers
--> ATA/ATAPI/MFM/RLL support
--> --> (g)eneric/default IDE chipset support (should already be ON)
--> (S)CSI device support
--> --> (S)CSI generic support (turn this ON)
--> --> (S)CSI low-level drivers
--> --> --> (S)erial ATA (SATA) support (should already be ON)
--> --> --> --> (I)ntel PIIX/ICH SATA support (turn OFF)
--> --> --> --> (P)romise SATA TX2/TX4 support (turn ON as BUILT-IN)
--> M(u)lti-device support (should already be ON)
--> --> (R)AID support (turn it ON as BUILT-IN)
--> --> --> (R)AID-1 mirroring mode (turn it ON as BUILT-IN)
--> --> (D)evice mapper support (set to MODULE or BUILT-IN)
--> N(e)tworking support
--> --> (E)thernet (10 or 100Mbit)
--> --> --> (E)thernet (10 or 100Mbit) (Turn OFF)
--> --> (E)thernet (1000Mbit)
--> --> --> (I)ntel(R) PRO/1000 Gigabit Ethernet support (turn OFF)
--> --> --> N(e)w SysKonnect GigaEthernet support (EXPERIMENTAL) (turn ON as BUILT-IN)
--> --> --> (B)roadcom Tigon3 support (turn OFF)
--> (C)haracter Devices
--> --> (I)ntel/AMD/VIA HW Random Number Generator (should be ON)
--> --> (I)ntel 440LX/BX/GX, I8xx and E7x05 chipset support (turn it OFF)
--> (S)ound
--> --> (S)ound card support (turn OFF)
(F)ile systems
--> N(e)twork File Systems
--> --> (S)MB file system support (turn ON as BUILT-IN)
--> --> (C)IFS support (turn ON as BUILT-IN)
(P)rofiling support
(K)ernel hacking
(S)ecurity options
(C)ryptographic options
--> (C)ryptographic API (turn ON)
--> --> HM(A)C support (NEW) (turn ON as BUILT-IN)
--> --> (turn ON all other options as MODULE)
(L)ibrary routines

Exit and save your configuration. Then build the kernel (the following command is for 2.6 kernels). Expect the compile to take almost no time at all on an AMD64 chip.  I used to wait an hour for all this to happen on my old VIA EPIA.

```
# make && make modules_install
```

Once the code finishes compiling, you need to copy the kernel to your /boot partition.

```
# mount /boot
# ls -l /boot
# ls -l arch/x86_64/boot
# df
# cp arch/x86_64/boot/bzImage /boot/kernel-2.6.13-9Nov2005
# cp System.map /boot/System.map-2.6.13-9Nov2005
# cp .config /boot/config-2.6.13-9Nov2005
# ls -l /boot
# nano -w /boot/grub/grub.conf
```

Add your new kernel.  I'd recommend always leaving the configuration for your old kernel in place and inserting the new config above the old one.  That way you get (2) benefits:

1) The "default 0" command will boot the new kernel automatically (because it appears first in the grub.conf file).

2) Your old kernel is still in place, in case the new kernel doesn't boot.  There's probably no reason to remove old kernels from the system unless you are running out of space on the /boot partition.  (Which is why I use the "df" command to check space.)

<b>Bugs and goofs</b>:

1) The disks attached to the onboard Promise PDC20378 RAID controller are not recognized by my first kernel (although they show up when I booted the LiveCD).  So I'm missing a kernel option.  Possibly I haven't [turned SCSI on](http://www.gentoo-wiki.com/index.php?title=HARDWARE_SATA&redirect=no) which allows me to pick the Promise SATA driver.

This is fixed by adding:

(D)evice drivers
--> (S)CSI device support
--> --> (S)CSI low-level drivers
--> --> --> (S)erial ATA (SATA) support (should already be ON)
--> --> --> --> (P)romise SATA TX2/TX4 support (turn ON as BUILT-IN)

1b) However, once you've turned on that particular driver (CONFIG_SCSI_SATA_PROMISE=y), your system will slow down and become very sluggish anytime that mdadm is rebuilding an array with drives attached to that controller.  You will also start to see the following messages in your "dmesg" output:

```
warning: many lost ticks.
Your time source seems to be instable or some driver is hogging interupts
rip __do_softirq+0x48/0xb0
```

2) The disks attached to the PCI Rocket133 cards did not show up after the first boot.  Same deal as #1, worked with the LiveCD, but I didn't get the driver selection right when I built the first kernel.  On the upside, it allowed me to identify the (2) disks that are attached to the Promise PCI controller without any effort (hde and hdg are on the Promise card).

(I'm still troubleshooting the Rocket133.)

Key things to look for in menuconfig for Rocket133 might be:

(D)evice drivers
--> ATA/ATAPI/MFM/RLL support                                                                     
--> --> SCSI emulation support                                                                    
--> --> generic/default IDE chipset support                                                       
--> --> PCI IDE chipset support                                                                   
--> --> Generic PCI IDE Chipset Support

Probably the only one that matters is (CONFIG_BLK_DEV_HPT366=y):

--> --> HPT36X/37X chipset support (turn this ON as BUILT-IN)

Yes, the Rocket 133SB (Rocket133SB) HPT302 chip is apparently supported by the HPT366.c file.  You can find this by grepping the kernel sources:

```
# cd /usr/src/linux
# find . -print | xargs grep -i 'hpt302'
# grep -i 'hpt366' .config
```

...

So, after turning on the two drivers I have all 8 drives showing up against in /proc/partitions:

hde / hdg -- Promise PCI card
hdk, hdo, hds -- Highpoint Rocket133 cards
hda -- motherboard IDE
sda -- Promise motherboard RAID PATA
sdb -- motherboard SATA

Performance is still slow, so now I'm digging through the kernel configs trying to find lines that contain "irq".

One key line that look interesting:

Sharing PCI IDE interrupts support (CONFIG_IDEPCI_SHARE_IRQ)

Turned that on, but still haven't fixed the sluggishness or the lost ticks issue.  I'm very tempted to give up on the PDC20378 chip, except that I know it worked on the LiveCD.
