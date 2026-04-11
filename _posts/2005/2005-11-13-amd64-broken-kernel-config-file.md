---
layout: post
title: 'AMD64 broken kernel config file'
date: '2005-11-13T20:25:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Current broken configuration.  Here is the diff between my current configuration and what was on the LiveCD.  Left side is the LiveCD config file, right side is my kernel's config file.

[AMD64 2005.1 Gentoo LiveCD Kernel Config](/techblog/Gentoo/AMD64/2005_1-LiveCDConfig.txt)

I'm still trying to puzzle out what is different on the LiveCD (which works, and which options are causing me grief on the installed kernel).  I've even tried adding the "noapic notsc" to my kernel line in grub.conf, but it doesn't fix the issue of sluggishness (it just hides the error).

3,4c3,4
&lt; # Linux kernel version: 2.6.12-gentoo-r6
&lt; # Mon Aug  1 14:21:03 2005
---
&gt; # Linux kernel version: 2.6.13-gentoo-r5
&gt; # Sun Nov 13 14:44:42 2005
22c22
&lt; CONFIG_LOCK_KERNEL=y
---
&gt; CONFIG_BROKEN_ON_SMP=y
31c31
&lt; # CONFIG_POSIX_MQUEUE is not set
---
&gt; CONFIG_POSIX_MQUEUE=y
35c35
&lt; CONFIG_HOTPLUG=y
---
&gt; # CONFIG_HOTPLUG is not set
39,41c39,42
&lt; CONFIG_CPUSETS=y
&lt; CONFIG_EMBEDDED=y
&lt; # CONFIG_KALLSYMS is not set
---
&gt; # CONFIG_EMBEDDED is not set
&gt; CONFIG_KALLSYMS=y
&gt; CONFIG_KALLSYMS_ALL=y
&gt; # CONFIG_KALLSYMS_EXTRA_PASS is not set
47d47
&lt; CONFIG_CC_OPTIMIZE_FOR_SIZE=y
61c61
&lt; # CONFIG_MODULE_FORCE_UNLOAD is not set
---
&gt; CONFIG_MODULE_FORCE_UNLOAD=y
63c63
&lt; CONFIG_MODVERSIONS=y
---
&gt; # CONFIG_MODVERSIONS is not set
65,66c65
&lt; CONFIG_KMOD=y
&lt; CONFIG_STOP_MACHINE=y
---
&gt; # CONFIG_KMOD is not set
71c70
&lt; # CONFIG_MK8 is not set
---
&gt; CONFIG_MK8=y
73,75c72,74
&lt; CONFIG_GENERIC_CPU=y
&lt; CONFIG_X86_L1_CACHE_BYTES=128
&lt; CONFIG_X86_L1_CACHE_SHIFT=7
---
&gt; # CONFIG_GENERIC_CPU is not set
&gt; CONFIG_X86_L1_CACHE_BYTES=64
&gt; CONFIG_X86_L1_CACHE_SHIFT=6
79,81c78,79
&lt; # CONFIG_X86_MSR is not set
&lt; # CONFIG_X86_CPUID is not set
&lt; CONFIG_X86_HT=y
---
&gt; CONFIG_X86_MSR=y
&gt; CONFIG_X86_CPUID=y
85,90c83,86
&lt; CONFIG_SMP=y
&lt; CONFIG_PREEMPT=y
&lt; CONFIG_PREEMPT_BKL=y
&lt; CONFIG_SCHED_SMT=y
&lt; # CONFIG_K8_NUMA is not set
&lt; # CONFIG_NUMA_EMU is not set
---
&gt; # CONFIG_SMP is not set
&gt; CONFIG_PREEMPT_NONE=y
&gt; # CONFIG_PREEMPT_VOLUNTARY is not set
&gt; # CONFIG_PREEMPT is not set
92,93c88,95
&lt; CONFIG_HAVE_DEC_LOCK=y
&lt; CONFIG_NR_CPUS=8
---
&gt; CONFIG_ARCH_FLATMEM_ENABLE=y
&gt; CONFIG_SELECT_MEMORY_MODEL=y
&gt; CONFIG_FLATMEM_MANUAL=y
&gt; # CONFIG_DISCONTIGMEM_MANUAL is not set
&gt; # CONFIG_SPARSEMEM_MANUAL is not set
&gt; CONFIG_FLATMEM=y
&gt; CONFIG_FLAT_NODE_MEM_MAP=y
&gt; CONFIG_HAVE_ARCH_EARLY_PFN_TO_NID=y
95,99c97,104
&lt; # CONFIG_X86_PM_TIMER is not set
&lt; # CONFIG_HPET_EMULATE_RTC is not set
&lt; # CONFIG_GART_IOMMU is not set
&lt; CONFIG_DUMMY_IOMMU=y
&lt; # CONFIG_X86_MCE is not set
---
&gt; CONFIG_X86_PM_TIMER=y
&gt; CONFIG_HPET_EMULATE_RTC=y
&gt; CONFIG_GART_IOMMU=y
&gt; CONFIG_SWIOTLB=y
&gt; CONFIG_X86_MCE=y
&gt; CONFIG_X86_MCE_INTEL=y
&gt; CONFIG_PHYSICAL_START=0x100000
&gt; # CONFIG_KEXEC is not set
100a106,109
&gt; # CONFIG_HZ_100 is not set
&gt; CONFIG_HZ_250=y
&gt; # CONFIG_HZ_1000 is not set
&gt; CONFIG_HZ=250
110c119,120
&lt; # CONFIG_SOFTWARE_SUSPEND is not set
---
&gt; CONFIG_SOFTWARE_SUSPEND=y
&gt; CONFIG_PM_STD_PARTITION=""
119,120c129,130
&lt; CONFIG_ACPI_AC=m
&lt; CONFIG_ACPI_BATTERY=m
---
&gt; # CONFIG_ACPI_AC is not set
&gt; # CONFIG_ACPI_BATTERY is not set
122a133
&gt; # CONFIG_ACPI_HOTKEY is not set
126,129c137,140
&lt; CONFIG_ACPI_ASUS=m
&lt; CONFIG_ACPI_IBM=m
&lt; CONFIG_ACPI_TOSHIBA=m
&lt; CONFIG_ACPI_BLACKLIST_YEAR=0
---
&gt; # CONFIG_ACPI_ASUS is not set
&gt; # CONFIG_ACPI_IBM is not set
&gt; # CONFIG_ACPI_TOSHIBA is not set
&gt; CONFIG_ACPI_BLACKLIST_YEAR=2001
136c147
&lt; CONFIG_ACPI_CONTAINER=m
---
&gt; # CONFIG_ACPI_CONTAINER is not set
142c153
&lt; CONFIG_CPU_FREQ_TABLE=m
---
&gt; CONFIG_CPU_FREQ_TABLE=y
144c155
&lt; CONFIG_CPU_FREQ_STAT=m
---
&gt; CONFIG_CPU_FREQ_STAT=y
149,152c160,163
&lt; CONFIG_CPU_FREQ_GOV_POWERSAVE=m
&lt; CONFIG_CPU_FREQ_GOV_USERSPACE=m
&lt; CONFIG_CPU_FREQ_GOV_ONDEMAND=m
&lt; CONFIG_CPU_FREQ_GOV_CONSERVATIVE=m
---
&gt; # CONFIG_CPU_FREQ_GOV_POWERSAVE is not set
&gt; # CONFIG_CPU_FREQ_GOV_USERSPACE is not set
&gt; # CONFIG_CPU_FREQ_GOV_ONDEMAND is not set
&gt; CONFIG_CPU_FREQ_GOV_CONSERVATIVE=y
157,161c168,170
&lt; CONFIG_X86_POWERNOW_K8=m
&lt; CONFIG_X86_POWERNOW_K8_ACPI=y
&lt; CONFIG_X86_SPEEDSTEP_CENTRINO=m
&lt; CONFIG_X86_SPEEDSTEP_CENTRINO_ACPI=y
&lt; CONFIG_X86_ACPI_CPUFREQ=m
---
&gt; CONFIG_X86_POWERNOW_K8=y
&gt; # CONFIG_X86_SPEEDSTEP_CENTRINO is not set
&gt; # CONFIG_X86_ACPI_CPUFREQ is not set
166,168c175
&lt; # CONFIG_X86_ACPI_CPUFREQ_PROC_INTF is not set
&lt; CONFIG_X86_P4_CLOCKMOD=m
&lt; CONFIG_X86_SPEEDSTEP_LIB=m
---
&gt; # CONFIG_X86_SPEEDSTEP_LIB is not set
177c184
&lt; CONFIG_PCIEPORTBUS=y
---
&gt; # CONFIG_PCIEPORTBUS is not set
186,198c193
&lt; CONFIG_PCCARD=m
&lt; # CONFIG_PCMCIA_DEBUG is not set
&lt; CONFIG_PCMCIA=m
&lt; CONFIG_CARDBUS=y
&lt; 
&lt; #
&lt; # PC-card bridges
&lt; #
&lt; CONFIG_YENTA=m
&lt; CONFIG_PD6729=m
&lt; CONFIG_I82092=m
&lt; CONFIG_TCIC=m
&lt; CONFIG_PCCARD_NONSTATIC=m
---
&gt; # CONFIG_PCCARD is not set
211c206
&lt; # CONFIG_IA32_AOUT is not set
---
&gt; CONFIG_IA32_AOUT=y
216a212,277
&gt; # Networking
&gt; #
&gt; CONFIG_NET=y
&gt; 
&gt; #
&gt; # Networking options
&gt; #
&gt; CONFIG_PACKET=y
&gt; # CONFIG_PACKET_MMAP is not set
&gt; CONFIG_UNIX=y
&gt; # CONFIG_NET_KEY is not set
&gt; CONFIG_INET=y
&gt; CONFIG_IP_MULTICAST=y
&gt; # CONFIG_IP_ADVANCED_ROUTER is not set
&gt; CONFIG_IP_FIB_HASH=y
&gt; # CONFIG_IP_PNP is not set
&gt; # CONFIG_NET_IPIP is not set
&gt; # CONFIG_NET_IPGRE is not set
&gt; # CONFIG_IP_MROUTE is not set
&gt; # CONFIG_ARPD is not set
&gt; # CONFIG_SYN_COOKIES is not set
&gt; # CONFIG_INET_AH is not set
&gt; # CONFIG_INET_ESP is not set
&gt; # CONFIG_INET_IPCOMP is not set
&gt; # CONFIG_INET_TUNNEL is not set
&gt; CONFIG_IP_TCPDIAG=y
&gt; CONFIG_IP_TCPDIAG_IPV6=y
&gt; # CONFIG_TCP_CONG_ADVANCED is not set
&gt; CONFIG_TCP_CONG_BIC=y
&gt; CONFIG_IPV6=y
&gt; # CONFIG_IPV6_PRIVACY is not set
&gt; # CONFIG_INET6_AH is not set
&gt; # CONFIG_INET6_ESP is not set
&gt; # CONFIG_INET6_IPCOMP is not set
&gt; # CONFIG_INET6_TUNNEL is not set
&gt; # CONFIG_IPV6_TUNNEL is not set
&gt; # CONFIG_NETFILTER is not set
&gt; 
&gt; #
&gt; # SCTP Configuration (EXPERIMENTAL)
&gt; #
&gt; # CONFIG_IP_SCTP is not set
&gt; # CONFIG_ATM is not set
&gt; # CONFIG_BRIDGE is not set
&gt; # CONFIG_VLAN_8021Q is not set
&gt; # CONFIG_DECNET is not set
&gt; # CONFIG_LLC2 is not set
&gt; # CONFIG_IPX is not set
&gt; # CONFIG_ATALK is not set
&gt; # CONFIG_X25 is not set
&gt; # CONFIG_LAPB is not set
&gt; # CONFIG_NET_DIVERT is not set
&gt; # CONFIG_ECONET is not set
&gt; # CONFIG_WAN_ROUTER is not set
&gt; # CONFIG_NET_SCHED is not set
&gt; # CONFIG_NET_CLS_ROUTE is not set
&gt; 
&gt; #
&gt; # Network testing
&gt; #
&gt; # CONFIG_NET_PKTGEN is not set
&gt; # CONFIG_HAMRADIO is not set
&gt; # CONFIG_IRDA is not set
&gt; # CONFIG_BT is not set
&gt; 
&gt; #
225c286
&lt; CONFIG_FW_LOADER=m
---
&gt; # CONFIG_FW_LOADER is not set
236,244c297
&lt; CONFIG_PARPORT=m
&lt; CONFIG_PARPORT_PC=m
&lt; CONFIG_PARPORT_SERIAL=m
&lt; CONFIG_PARPORT_PC_FIFO=y
&lt; CONFIG_PARPORT_PC_SUPERIO=y
&lt; CONFIG_PARPORT_PC_PCMCIA=m
&lt; CONFIG_PARPORT_NOT_PC=y
&lt; # CONFIG_PARPORT_GSC is not set
&lt; CONFIG_PARPORT_1284=y
---
&gt; # CONFIG_PARPORT is not set
260,295c313,317
&lt; CONFIG_BLK_DEV_FD=m
&lt; CONFIG_PARIDE=m
&lt; CONFIG_PARIDE_PARPORT=m
&lt; 
&lt; #
&lt; # Parallel IDE high-level drivers
&lt; #
&lt; CONFIG_PARIDE_PD=m
&lt; CONFIG_PARIDE_PCD=m
&lt; CONFIG_PARIDE_PF=m
&lt; CONFIG_PARIDE_PT=m
&lt; CONFIG_PARIDE_PG=m
&lt; 
&lt; #
&lt; # Parallel IDE protocol modules
&lt; #
&lt; CONFIG_PARIDE_ATEN=m
&lt; CONFIG_PARIDE_BPCK=m
&lt; CONFIG_PARIDE_COMM=m
&lt; CONFIG_PARIDE_DSTR=m
&lt; CONFIG_PARIDE_FIT2=m
&lt; CONFIG_PARIDE_FIT3=m
&lt; CONFIG_PARIDE_EPAT=m
&lt; CONFIG_PARIDE_EPATC8=y
&lt; CONFIG_PARIDE_EPIA=m
&lt; CONFIG_PARIDE_FRIQ=m
&lt; CONFIG_PARIDE_FRPW=m
&lt; CONFIG_PARIDE_KBIC=m
&lt; CONFIG_PARIDE_KTTI=m
&lt; CONFIG_PARIDE_ON20=m
&lt; CONFIG_PARIDE_ON26=m
&lt; CONFIG_BLK_CPQ_DA=m
&lt; CONFIG_BLK_CPQ_CISS_DA=m
&lt; # CONFIG_CISS_SCSI_TAPE is not set
&lt; CONFIG_BLK_DEV_DAC960=m
&lt; CONFIG_BLK_DEV_UMEM=m
---
&gt; CONFIG_BLK_DEV_FD=y
&gt; # CONFIG_BLK_CPQ_DA is not set
&gt; # CONFIG_BLK_CPQ_CISS_DA is not set
&gt; # CONFIG_BLK_DEV_DAC960 is not set
&gt; # CONFIG_BLK_DEV_UMEM is not set
299,300c321,322
&lt; CONFIG_BLK_DEV_NBD=m
&lt; CONFIG_BLK_DEV_SX8=m
---
&gt; # CONFIG_BLK_DEV_NBD is not set
&gt; # CONFIG_BLK_DEV_SX8 is not set
304c326
&lt; CONFIG_BLK_DEV_RAM_SIZE=8192
---
&gt; CONFIG_BLK_DEV_RAM_SIZE=4096
316c338
&lt; # CONFIG_IOSCHED_CFQ is not set
---
&gt; CONFIG_IOSCHED_CFQ=y
332d353
&lt; CONFIG_BLK_DEV_IDECS=m
335c356
&lt; CONFIG_BLK_DEV_IDEFLOPPY=m
---
&gt; # CONFIG_BLK_DEV_IDEFLOPPY is not set
343,345c364,365
&lt; CONFIG_BLK_DEV_CMD640=y
&lt; CONFIG_BLK_DEV_CMD640_ENHANCED=y
&lt; CONFIG_BLK_DEV_IDEPNP=y
---
&gt; # CONFIG_BLK_DEV_CMD640 is not set
&gt; # CONFIG_BLK_DEV_IDEPNP is not set
350,351c370,371
&lt; CONFIG_BLK_DEV_OPTI621=y
&lt; CONFIG_BLK_DEV_RZ1000=y
---
&gt; # CONFIG_BLK_DEV_OPTI621 is not set
&gt; # CONFIG_BLK_DEV_RZ1000 is not set
356,358c376,377
&lt; CONFIG_BLK_DEV_AEC62XX=y
&lt; CONFIG_BLK_DEV_ALI15X3=y
&lt; # CONFIG_WDC_ALI15X3 is not set
---
&gt; # CONFIG_BLK_DEV_AEC62XX is not set
&gt; # CONFIG_BLK_DEV_ALI15X3 is not set
360,367c379,385
&lt; CONFIG_BLK_DEV_ATIIXP=y
&lt; CONFIG_BLK_DEV_CMD64X=y
&lt; CONFIG_BLK_DEV_TRIFLEX=y
&lt; CONFIG_BLK_DEV_CY82C693=y
&lt; CONFIG_BLK_DEV_CS5520=y
&lt; CONFIG_BLK_DEV_CS5530=y
&lt; CONFIG_BLK_DEV_HPT34X=y
&lt; # CONFIG_HPT34X_AUTODMA is not set
---
&gt; # CONFIG_BLK_DEV_ATIIXP is not set
&gt; # CONFIG_BLK_DEV_CMD64X is not set
&gt; # CONFIG_BLK_DEV_TRIFLEX is not set
&gt; # CONFIG_BLK_DEV_CY82C693 is not set
&gt; # CONFIG_BLK_DEV_CS5520 is not set
&gt; # CONFIG_BLK_DEV_CS5530 is not set
&gt; # CONFIG_BLK_DEV_HPT34X is not set
369,374c387,391
&lt; CONFIG_BLK_DEV_SC1200=y
&lt; CONFIG_BLK_DEV_PIIX=y
&lt; CONFIG_BLK_DEV_IT821X=y
&lt; CONFIG_BLK_DEV_NS87415=y
&lt; CONFIG_BLK_DEV_PDC202XX_OLD=y
&lt; # CONFIG_PDC202XX_BURST is not set
---
&gt; # CONFIG_BLK_DEV_SC1200 is not set
&gt; # CONFIG_BLK_DEV_PIIX is not set
&gt; # CONFIG_BLK_DEV_IT821X is not set
&gt; # CONFIG_BLK_DEV_NS87415 is not set
&gt; # CONFIG_BLK_DEV_PDC202XX_OLD is not set
377,382c394,399
&lt; CONFIG_BLK_DEV_SVWKS=y
&lt; CONFIG_BLK_DEV_SIIMAGE=m
&lt; CONFIG_BLK_DEV_SIS5513=y
&lt; CONFIG_BLK_DEV_SLC90E66=y
&lt; CONFIG_BLK_DEV_TRM290=y
&lt; CONFIG_BLK_DEV_VIA82CXXX=y
---
&gt; # CONFIG_BLK_DEV_SVWKS is not set
&gt; # CONFIG_BLK_DEV_SIIMAGE is not set
&gt; # CONFIG_BLK_DEV_SIS5513 is not set
&gt; # CONFIG_BLK_DEV_SLC90E66 is not set
&gt; # CONFIG_BLK_DEV_TRM290 is not set
&gt; # CONFIG_BLK_DEV_VIA82CXXX is not set
401,403c418,420
&lt; CONFIG_BLK_DEV_SR=y
&lt; CONFIG_BLK_DEV_SR_VENDOR=y
&lt; CONFIG_CHR_DEV_SG=m
---
&gt; # CONFIG_BLK_DEV_SR is not set
&gt; # CONFIG_CHR_DEV_SG is not set
&gt; # CONFIG_CHR_DEV_SCH is not set
415,416c432,433
&lt; CONFIG_SCSI_SPI_ATTRS=m
&lt; CONFIG_SCSI_FC_ATTRS=m
---
&gt; # CONFIG_SCSI_SPI_ATTRS is not set
&gt; # CONFIG_SCSI_FC_ATTRS is not set
422,431c439,443
&lt; CONFIG_BLK_DEV_3W_XXXX_RAID=m
&lt; CONFIG_SCSI_3W_9XXX=m
&lt; CONFIG_SCSI_ACARD=m
&lt; CONFIG_SCSI_AACRAID=m
&lt; CONFIG_SCSI_AIC7XXX=m
&lt; CONFIG_AIC7XXX_CMDS_PER_DEVICE=32
&lt; CONFIG_AIC7XXX_RESET_DELAY_MS=5000
&lt; # CONFIG_AIC7XXX_DEBUG_ENABLE is not set
&lt; CONFIG_AIC7XXX_DEBUG_MASK=0
&lt; CONFIG_AIC7XXX_REG_PRETTY_PRINT=y
---
&gt; # CONFIG_BLK_DEV_3W_XXXX_RAID is not set
&gt; # CONFIG_SCSI_3W_9XXX is not set
&gt; # CONFIG_SCSI_ACARD is not set
&gt; # CONFIG_SCSI_AACRAID is not set
&gt; # CONFIG_SCSI_AIC7XXX is not set
433,443c445,447
&lt; CONFIG_SCSI_AIC79XX=m
&lt; CONFIG_AIC79XX_CMDS_PER_DEVICE=32
&lt; CONFIG_AIC79XX_RESET_DELAY_MS=5000
&lt; # CONFIG_AIC79XX_ENABLE_RD_STRM is not set
&lt; # CONFIG_AIC79XX_DEBUG_ENABLE is not set
&lt; CONFIG_AIC79XX_DEBUG_MASK=0
&lt; # CONFIG_AIC79XX_REG_PRETTY_PRINT is not set
&lt; CONFIG_MEGARAID_NEWGEN=y
&lt; CONFIG_MEGARAID_MM=m
&lt; CONFIG_MEGARAID_MAILBOX=m
&lt; CONFIG_MEGARAID_LEGACY=m
---
&gt; # CONFIG_SCSI_AIC79XX is not set
&gt; # CONFIG_MEGARAID_NEWGEN is not set
&gt; # CONFIG_MEGARAID_LEGACY is not set
445,484c449,472
&lt; CONFIG_SCSI_SATA_AHCI=m
&lt; CONFIG_SCSI_SATA_SVW=m
&lt; CONFIG_SCSI_ATA_PIIX=m
&lt; CONFIG_SCSI_SATA_NV=m
&lt; CONFIG_SCSI_SATA_PROMISE=m
&lt; CONFIG_SCSI_SATA_QSTOR=m
&lt; CONFIG_SCSI_SATA_SX4=m
&lt; CONFIG_SCSI_SATA_SIL=m
&lt; CONFIG_SCSI_SATA_SIS=m
&lt; CONFIG_SCSI_SATA_ULI=m
&lt; CONFIG_SCSI_SATA_VIA=m
&lt; CONFIG_SCSI_SATA_VITESSE=m
&lt; CONFIG_SCSI_BUSLOGIC=m
&lt; # CONFIG_SCSI_OMIT_FLASHPOINT is not set
&lt; CONFIG_SCSI_DMX3191D=m
&lt; CONFIG_SCSI_EATA=m
&lt; CONFIG_SCSI_EATA_TAGGED_QUEUE=y
&lt; CONFIG_SCSI_EATA_LINKED_COMMANDS=y
&lt; CONFIG_SCSI_EATA_MAX_TAGS=16
&lt; CONFIG_SCSI_FUTURE_DOMAIN=m
&lt; CONFIG_SCSI_GDTH=m
&lt; CONFIG_SCSI_IPS=m
&lt; CONFIG_SCSI_INITIO=m
&lt; CONFIG_SCSI_INIA100=m
&lt; CONFIG_SCSI_PPA=m
&lt; CONFIG_SCSI_IMM=m
&lt; # CONFIG_SCSI_IZIP_EPP16 is not set
&lt; # CONFIG_SCSI_IZIP_SLOW_CTR is not set
&lt; CONFIG_SCSI_SYM53C8XX_2=m
&lt; CONFIG_SCSI_SYM53C8XX_DMA_ADDRESSING_MODE=1
&lt; CONFIG_SCSI_SYM53C8XX_DEFAULT_TAGS=16
&lt; CONFIG_SCSI_SYM53C8XX_MAX_TAGS=64
&lt; # CONFIG_SCSI_SYM53C8XX_IOMAPPED is not set
&lt; CONFIG_SCSI_IPR=m
&lt; # CONFIG_SCSI_IPR_TRACE is not set
&lt; # CONFIG_SCSI_IPR_DUMP is not set
&lt; CONFIG_SCSI_QLOGIC_FC=m
&lt; # CONFIG_SCSI_QLOGIC_FC_FIRMWARE is not set
&lt; CONFIG_SCSI_QLOGIC_1280=m
&lt; CONFIG_SCSI_QLOGIC_1280_1040=y
---
&gt; # CONFIG_SCSI_SATA_AHCI is not set
&gt; # CONFIG_SCSI_SATA_SVW is not set
&gt; # CONFIG_SCSI_ATA_PIIX is not set
&gt; # CONFIG_SCSI_SATA_NV is not set
&gt; CONFIG_SCSI_SATA_PROMISE=y
&gt; # CONFIG_SCSI_SATA_QSTOR is not set
&gt; # CONFIG_SCSI_SATA_SX4 is not set
&gt; # CONFIG_SCSI_SATA_SIL is not set
&gt; # CONFIG_SCSI_SATA_SIS is not set
&gt; # CONFIG_SCSI_SATA_ULI is not set
&gt; CONFIG_SCSI_SATA_VIA=y
&gt; # CONFIG_SCSI_SATA_VITESSE is not set
&gt; # CONFIG_SCSI_BUSLOGIC is not set
&gt; # CONFIG_SCSI_DMX3191D is not set
&gt; # CONFIG_SCSI_EATA is not set
&gt; # CONFIG_SCSI_FUTURE_DOMAIN is not set
&gt; # CONFIG_SCSI_GDTH is not set
&gt; # CONFIG_SCSI_IPS is not set
&gt; # CONFIG_SCSI_INITIO is not set
&gt; # CONFIG_SCSI_INIA100 is not set
&gt; # CONFIG_SCSI_SYM53C8XX_2 is not set
&gt; # CONFIG_SCSI_IPR is not set
&gt; # CONFIG_SCSI_QLOGIC_FC is not set
&gt; # CONFIG_SCSI_QLOGIC_1280 is not set
486,493c474,482
&lt; CONFIG_SCSI_QLA21XX=m
&lt; CONFIG_SCSI_QLA22XX=m
&lt; CONFIG_SCSI_QLA2300=m
&lt; CONFIG_SCSI_QLA2322=m
&lt; CONFIG_SCSI_QLA6312=m
&lt; CONFIG_SCSI_LPFC=m
&lt; CONFIG_SCSI_DC395x=m
&lt; CONFIG_SCSI_DC390T=m
---
&gt; # CONFIG_SCSI_QLA21XX is not set
&gt; # CONFIG_SCSI_QLA22XX is not set
&gt; # CONFIG_SCSI_QLA2300 is not set
&gt; # CONFIG_SCSI_QLA2322 is not set
&gt; # CONFIG_SCSI_QLA6312 is not set
&gt; # CONFIG_SCSI_QLA24XX is not set
&gt; # CONFIG_SCSI_LPFC is not set
&gt; # CONFIG_SCSI_DC395x is not set
&gt; # CONFIG_SCSI_DC390T is not set
497,503d485
&lt; # PCMCIA SCSI adapter support
&lt; #
&lt; CONFIG_PCMCIA_FDOMAIN=m
&lt; CONFIG_PCMCIA_QLOGIC=m
&lt; CONFIG_PCMCIA_SYM53C500=m
&lt; 
&lt; #
507c489
&lt; CONFIG_BLK_DEV_MD=m
---
&gt; CONFIG_BLK_DEV_MD=y
510c492
&lt; CONFIG_MD_RAID1=m
---
&gt; CONFIG_MD_RAID1=y
516c498
&lt; CONFIG_BLK_DEV_DM=m
---
&gt; CONFIG_BLK_DEV_DM=y
528,531c510,512
&lt; CONFIG_FUSION=m
&lt; CONFIG_FUSION_MAX_SGE=40
&lt; CONFIG_FUSION_CTL=m
&lt; CONFIG_FUSION_LAN=m
---
&gt; # CONFIG_FUSION is not set
&gt; # CONFIG_FUSION_SPI is not set
&gt; # CONFIG_FUSION_FC is not set
536c517
&lt; CONFIG_IEEE1394=m
---
&gt; CONFIG_IEEE1394=y
543,544c524,525
&lt; CONFIG_IEEE1394_EXTRA_CONFIG_ROMS=y
&lt; CONFIG_IEEE1394_CONFIG_ROM_IP1394=y
---
&gt; # CONFIG_IEEE1394_EXTRA_CONFIG_ROMS is not set
&gt; # CONFIG_IEEE1394_EXPORT_FULL_API is not set
553c534
&lt; CONFIG_IEEE1394_OHCI1394=m
---
&gt; # CONFIG_IEEE1394_OHCI1394 is not set
558,565c539,542
&lt; CONFIG_IEEE1394_VIDEO1394=m
&lt; CONFIG_IEEE1394_SBP2=m
&lt; # CONFIG_IEEE1394_SBP2_PHYS_DMA is not set
&lt; CONFIG_IEEE1394_ETH1394=m
&lt; CONFIG_IEEE1394_DV1394=m
&lt; CONFIG_IEEE1394_RAWIO=m
&lt; CONFIG_IEEE1394_CMP=m
&lt; # CONFIG_IEEE1394_AMDTP is not set
---
&gt; # CONFIG_IEEE1394_SBP2 is not set
&gt; # CONFIG_IEEE1394_ETH1394 is not set
&gt; # CONFIG_IEEE1394_RAWIO is not set
&gt; # CONFIG_IEEE1394_CMP is not set
570,638c547
&lt; CONFIG_I2O=m
&lt; CONFIG_I2O_CONFIG=m
&lt; CONFIG_I2O_BLOCK=m
&lt; CONFIG_I2O_SCSI=m
&lt; CONFIG_I2O_PROC=m
&lt; 
&lt; #
&lt; # Networking support
&lt; #
&lt; CONFIG_NET=y
&lt; 
&lt; #
&lt; # Networking options
&lt; #
&lt; CONFIG_PACKET=y
&lt; # CONFIG_PACKET_MMAP is not set
&lt; CONFIG_UNIX=y
&lt; # CONFIG_NET_KEY is not set
&lt; CONFIG_INET=y
&lt; # CONFIG_IP_MULTICAST is not set
&lt; # CONFIG_IP_ADVANCED_ROUTER is not set
&lt; # CONFIG_IP_PNP is not set
&lt; # CONFIG_NET_IPIP is not set
&lt; # CONFIG_NET_IPGRE is not set
&lt; # CONFIG_ARPD is not set
&lt; # CONFIG_SYN_COOKIES is not set
&lt; # CONFIG_INET_AH is not set
&lt; # CONFIG_INET_ESP is not set
&lt; # CONFIG_INET_IPCOMP is not set
&lt; # CONFIG_INET_TUNNEL is not set
&lt; CONFIG_IP_TCPDIAG=y
&lt; # CONFIG_IP_TCPDIAG_IPV6 is not set
&lt; CONFIG_IPV6=m
&lt; CONFIG_IPV6_PRIVACY=y
&lt; CONFIG_INET6_AH=m
&lt; CONFIG_INET6_ESP=m
&lt; CONFIG_INET6_IPCOMP=m
&lt; CONFIG_INET6_TUNNEL=m
&lt; CONFIG_IPV6_TUNNEL=m
&lt; # CONFIG_NETFILTER is not set
&lt; CONFIG_XFRM=y
&lt; # CONFIG_XFRM_USER is not set
&lt; 
&lt; #
&lt; # SCTP Configuration (EXPERIMENTAL)
&lt; #
&lt; # CONFIG_IP_SCTP is not set
&lt; CONFIG_ATM=m
&lt; # CONFIG_ATM_CLIP is not set
&lt; # CONFIG_ATM_LANE is not set
&lt; # CONFIG_ATM_BR2684 is not set
&lt; # CONFIG_BRIDGE is not set
&lt; CONFIG_VLAN_8021Q=m
&lt; # CONFIG_DECNET is not set
&lt; CONFIG_LLC=y
&lt; # CONFIG_LLC2 is not set
&lt; # CONFIG_IPX is not set
&lt; # CONFIG_ATALK is not set
&lt; # CONFIG_X25 is not set
&lt; # CONFIG_LAPB is not set
&lt; # CONFIG_NET_DIVERT is not set
&lt; # CONFIG_ECONET is not set
&lt; # CONFIG_WAN_ROUTER is not set
&lt; 
&lt; #
&lt; # QoS and/or fair queueing
&lt; #
&lt; # CONFIG_NET_SCHED is not set
&lt; # CONFIG_NET_CLS_ROUTE is not set
---
&gt; # CONFIG_I2O is not set
641c550
&lt; # Network testing
---
&gt; # Network device support
643,675d551
&lt; # CONFIG_NET_PKTGEN is not set
&lt; # CONFIG_NETPOLL is not set
&lt; # CONFIG_NET_POLL_CONTROLLER is not set
&lt; # CONFIG_HAMRADIO is not set
&lt; # CONFIG_IRDA is not set
&lt; CONFIG_BT=m
&lt; CONFIG_BT_L2CAP=m
&lt; CONFIG_BT_SCO=m
&lt; CONFIG_BT_RFCOMM=m
&lt; CONFIG_BT_RFCOMM_TTY=y
&lt; CONFIG_BT_BNEP=m
&lt; CONFIG_BT_BNEP_MC_FILTER=y
&lt; CONFIG_BT_BNEP_PROTO_FILTER=y
&lt; # CONFIG_BT_CMTP is not set
&lt; CONFIG_BT_HIDP=m
&lt; 
&lt; #
&lt; # Bluetooth device drivers
&lt; #
&lt; CONFIG_BT_HCIUSB=m
&lt; CONFIG_BT_HCIUSB_SCO=y
&lt; CONFIG_BT_HCIUART=m
&lt; CONFIG_BT_HCIUART_H4=y
&lt; CONFIG_BT_HCIUART_BCSP=y
&lt; CONFIG_BT_HCIUART_BCSP_TXCRC=y
&lt; CONFIG_BT_HCIBCM203X=m
&lt; CONFIG_BT_HCIBPA10X=m
&lt; CONFIG_BT_HCIBFUSB=m
&lt; CONFIG_BT_HCIDTL1=m
&lt; CONFIG_BT_HCIBT3C=m
&lt; CONFIG_BT_HCIBLUECARD=m
&lt; CONFIG_BT_HCIBTUART=m
&lt; CONFIG_BT_HCIVHCI=m
680,681c556,557
&lt; # CONFIG_TUN is not set
&lt; CONFIG_NET_SB1000=m
---
&gt; CONFIG_TUN=y
&gt; # CONFIG_NET_SB1000 is not set
691,739c567
&lt; CONFIG_NET_ETHERNET=y
&lt; CONFIG_MII=m
&lt; CONFIG_HAPPYMEAL=m
&lt; CONFIG_SUNGEM=m
&lt; CONFIG_NET_VENDOR_3COM=y
&lt; CONFIG_VORTEX=m
&lt; CONFIG_TYPHOON=m
&lt; 
&lt; #
&lt; # Tulip family network device support
&lt; #
&lt; CONFIG_NET_TULIP=y
&lt; CONFIG_DE2104X=m
&lt; CONFIG_TULIP=m
&lt; CONFIG_TULIP_MWI=y
&lt; CONFIG_TULIP_MMIO=y
&lt; CONFIG_TULIP_NAPI=y
&lt; CONFIG_TULIP_NAPI_HW_MITIGATION=y
&lt; CONFIG_DE4X5=m
&lt; CONFIG_WINBOND_840=m
&lt; CONFIG_DM9102=m
&lt; CONFIG_PCMCIA_XIRCOM=m
&lt; CONFIG_HP100=m
&lt; CONFIG_NET_PCI=y
&lt; CONFIG_PCNET32=m
&lt; CONFIG_AMD8111_ETH=m
&lt; # CONFIG_AMD8111E_NAPI is not set
&lt; CONFIG_ADAPTEC_STARFIRE=m
&lt; # CONFIG_ADAPTEC_STARFIRE_NAPI is not set
&lt; CONFIG_B44=m
&lt; CONFIG_FORCEDETH=m
&lt; CONFIG_DGRS=m
&lt; # CONFIG_EEPRO100 is not set
&lt; CONFIG_E100=m
&lt; CONFIG_FEALNX=m
&lt; CONFIG_NATSEMI=m
&lt; CONFIG_NE2K_PCI=m
&lt; CONFIG_8139CP=m
&lt; CONFIG_8139TOO=m
&lt; # CONFIG_8139TOO_PIO is not set
&lt; CONFIG_8139TOO_TUNE_TWISTER=y
&lt; CONFIG_8139TOO_8129=y
&lt; # CONFIG_8139_OLD_RX_RESET is not set
&lt; CONFIG_SIS900=m
&lt; CONFIG_EPIC100=m
&lt; CONFIG_SUNDANCE=m
&lt; CONFIG_SUNDANCE_MMIO=y
&lt; CONFIG_VIA_RHINE=m
&lt; CONFIG_VIA_RHINE_MMIO=y
---
&gt; # CONFIG_NET_ETHERNET is not set
744,759c572,582
&lt; CONFIG_ACENIC=m
&lt; # CONFIG_ACENIC_OMIT_TIGON_I is not set
&lt; CONFIG_DL2K=m
&lt; CONFIG_E1000=m
&lt; # CONFIG_E1000_NAPI is not set
&lt; CONFIG_NS83820=m
&lt; CONFIG_HAMACHI=m
&lt; CONFIG_YELLOWFIN=m
&lt; CONFIG_R8169=m
&lt; # CONFIG_R8169_NAPI is not set
&lt; CONFIG_R8169_VLAN=y
&lt; CONFIG_SKGE=m
&lt; CONFIG_SK98LIN=m
&lt; CONFIG_VIA_VELOCITY=m
&lt; CONFIG_TIGON3=m
&lt; CONFIG_BNX2=m
---
&gt; # CONFIG_ACENIC is not set
&gt; # CONFIG_DL2K is not set
&gt; # CONFIG_E1000 is not set
&gt; # CONFIG_NS83820 is not set
&gt; # CONFIG_HAMACHI is not set
&gt; # CONFIG_YELLOWFIN is not set
&gt; # CONFIG_R8169 is not set
&gt; CONFIG_SKGE=y
&gt; # CONFIG_SK98LIN is not set
&gt; # CONFIG_TIGON3 is not set
&gt; # CONFIG_BNX2 is not set
764,765c587
&lt; CONFIG_IXGB=m
&lt; # CONFIG_IXGB_NAPI is not set
---
&gt; # CONFIG_IXGB is not set
773,778c595
&lt; CONFIG_TR=y
&lt; CONFIG_IBMOL=m
&lt; CONFIG_3C359=m
&lt; CONFIG_TMS380TR=m
&lt; CONFIG_TMSPCI=m
&lt; CONFIG_ABYSS=m
---
&gt; # CONFIG_TR is not set
783,828c600
&lt; CONFIG_NET_RADIO=y
&lt; 
&lt; #
&lt; # Obsolete Wireless cards support (pre-802.11)
&lt; #
&lt; CONFIG_STRIP=m
&lt; CONFIG_PCMCIA_WAVELAN=m
&lt; CONFIG_PCMCIA_NETWAVE=m
&lt; 
&lt; #
&lt; # Wireless 802.11 Frequency Hopping cards support
&lt; #
&lt; CONFIG_PCMCIA_RAYCS=m
&lt; 
&lt; #
&lt; # Wireless 802.11b ISA/PCI cards support
&lt; #
&lt; # CONFIG_HERMES is not set
&lt; CONFIG_ATMEL=m
&lt; CONFIG_PCI_ATMEL=m
&lt; 
&lt; #
&lt; # Wireless 802.11b Pcmcia/Cardbus cards support
&lt; #
&lt; CONFIG_AIRO_CS=m
&lt; CONFIG_PCMCIA_ATMEL=m
&lt; CONFIG_PCMCIA_WL3501=m
&lt; 
&lt; #
&lt; # Prism GT/Duette 802.11(a/b/g) PCI/Cardbus support
&lt; #
&lt; CONFIG_PRISM54=m
&lt; CONFIG_NET_WIRELESS=y
&lt; 
&lt; #
&lt; # PCMCIA network device support
&lt; #
&lt; CONFIG_NET_PCMCIA=y
&lt; CONFIG_PCMCIA_3C589=m
&lt; CONFIG_PCMCIA_3C574=m
&lt; CONFIG_PCMCIA_FMVJ18X=m
&lt; CONFIG_PCMCIA_PCNET=m
&lt; CONFIG_PCMCIA_NMCLAN=m
&lt; CONFIG_PCMCIA_SMC91C92=m
&lt; CONFIG_PCMCIA_XIRC2PS=m
&lt; CONFIG_PCMCIA_AXNET=m
---
&gt; # CONFIG_NET_RADIO is not set
833,893c605,610
&lt; CONFIG_WAN=y
&lt; CONFIG_DSCC4=m
&lt; CONFIG_DSCC4_PCISYNC=y
&lt; CONFIG_DSCC4_PCI_RST=y
&lt; CONFIG_LANMEDIA=m
&lt; CONFIG_SYNCLINK_SYNCPPP=m
&lt; CONFIG_HDLC=m
&lt; CONFIG_HDLC_RAW=y
&lt; CONFIG_HDLC_RAW_ETH=y
&lt; CONFIG_HDLC_CISCO=y
&lt; CONFIG_HDLC_FR=y
&lt; CONFIG_HDLC_PPP=y
&lt; 
&lt; #
&lt; # X.25/LAPB support is disabled
&lt; #
&lt; CONFIG_PCI200SYN=m
&lt; CONFIG_WANXL=m
&lt; CONFIG_PC300=m
&lt; CONFIG_PC300_MLPPP=y
&lt; CONFIG_FARSYNC=m
&lt; CONFIG_DLCI=m
&lt; CONFIG_DLCI_COUNT=24
&lt; CONFIG_DLCI_MAX=8
&lt; CONFIG_SBNI=m
&lt; CONFIG_SBNI_MULTILINE=y
&lt; 
&lt; #
&lt; # ATM drivers
&lt; #
&lt; # CONFIG_ATM_TCP is not set
&lt; # CONFIG_ATM_LANAI is not set
&lt; # CONFIG_ATM_ENI is not set
&lt; # CONFIG_ATM_FIRESTREAM is not set
&lt; # CONFIG_ATM_ZATM is not set
&lt; # CONFIG_ATM_IDT77252 is not set
&lt; # CONFIG_ATM_AMBASSADOR is not set
&lt; # CONFIG_ATM_HORIZON is not set
&lt; # CONFIG_ATM_FORE200E_MAYBE is not set
&lt; # CONFIG_ATM_HE is not set
&lt; CONFIG_FDDI=y
&lt; CONFIG_DEFXX=m
&lt; CONFIG_SKFP=m
&lt; CONFIG_HIPPI=y
&lt; CONFIG_ROADRUNNER=m
&lt; # CONFIG_ROADRUNNER_LARGE_RINGS is not set
&lt; CONFIG_PLIP=m
&lt; CONFIG_PPP=m
&lt; CONFIG_PPP_MULTILINK=y
&lt; CONFIG_PPP_FILTER=y
&lt; CONFIG_PPP_ASYNC=m
&lt; CONFIG_PPP_SYNC_TTY=m
&lt; CONFIG_PPP_DEFLATE=m
&lt; CONFIG_PPP_BSDCOMP=m
&lt; CONFIG_PPPOE=m
&lt; CONFIG_PPPOATM=m
&lt; CONFIG_SLIP=m
&lt; CONFIG_SLIP_COMPRESSED=y
&lt; CONFIG_SLIP_SMART=y
&lt; CONFIG_SLIP_MODE_SLIP6=y
&lt; CONFIG_NET_FC=y
---
&gt; # CONFIG_WAN is not set
&gt; # CONFIG_FDDI is not set
&gt; # CONFIG_HIPPI is not set
&gt; # CONFIG_PPP is not set
&gt; # CONFIG_SLIP is not set
&gt; # CONFIG_NET_FC is not set
895c612,616
&lt; # CONFIG_NETCONSOLE is not set
---
&gt; CONFIG_NETCONSOLE=y
&gt; CONFIG_NETPOLL=y
&gt; # CONFIG_NETPOLL_RX is not set
&gt; # CONFIG_NETPOLL_TRAP is not set
&gt; CONFIG_NET_POLL_CONTROLLER=y
900,941c621
&lt; CONFIG_ISDN=m
&lt; 
&lt; #
&lt; # Old ISDN4Linux
&lt; #
&lt; # CONFIG_ISDN_I4L is not set
&lt; 
&lt; #
&lt; # CAPI subsystem
&lt; #
&lt; CONFIG_ISDN_CAPI=m
&lt; # CONFIG_ISDN_DRV_AVMB1_VERBOSE_REASON is not set
&lt; CONFIG_ISDN_CAPI_MIDDLEWARE=y
&lt; CONFIG_ISDN_CAPI_CAPI20=m
&lt; CONFIG_ISDN_CAPI_CAPIFS_BOOL=y
&lt; CONFIG_ISDN_CAPI_CAPIFS=m
&lt; 
&lt; #
&lt; # CAPI hardware drivers
&lt; #
&lt; 
&lt; #
&lt; # Active AVM cards
&lt; #
&lt; CONFIG_CAPI_AVM=y
&lt; CONFIG_ISDN_DRV_AVMB1_B1PCI=m
&lt; CONFIG_ISDN_DRV_AVMB1_B1PCIV4=y
&lt; CONFIG_ISDN_DRV_AVMB1_B1PCMCIA=m
&lt; CONFIG_ISDN_DRV_AVMB1_AVM_CS=m
&lt; CONFIG_ISDN_DRV_AVMB1_T1PCI=m
&lt; CONFIG_ISDN_DRV_AVMB1_C4=m
&lt; 
&lt; #
&lt; # Active Eicon DIVA Server cards
&lt; #
&lt; CONFIG_CAPI_EICON=y
&lt; CONFIG_ISDN_DIVAS=m
&lt; CONFIG_ISDN_DIVAS_BRIPCI=y
&lt; CONFIG_ISDN_DIVAS_PRIPCI=y
&lt; CONFIG_ISDN_DIVAS_DIVACAPI=m
&lt; CONFIG_ISDN_DIVAS_USERIDI=m
&lt; CONFIG_ISDN_DIVAS_MAINT=m
---
&gt; # CONFIG_ISDN is not set
970,973c650,653
&lt; CONFIG_KEYBOARD_SUNKBD=m
&lt; CONFIG_KEYBOARD_LKKBD=m
&lt; CONFIG_KEYBOARD_XTKBD=m
&lt; CONFIG_KEYBOARD_NEWTON=m
---
&gt; # CONFIG_KEYBOARD_SUNKBD is not set
&gt; # CONFIG_KEYBOARD_LKKBD is not set
&gt; # CONFIG_KEYBOARD_XTKBD is not set
&gt; # CONFIG_KEYBOARD_NEWTON is not set
976c656
&lt; CONFIG_MOUSE_SERIAL=m
---
&gt; # CONFIG_MOUSE_SERIAL is not set
980,982c660
&lt; CONFIG_INPUT_MISC=y
&lt; CONFIG_INPUT_PCSPKR=m
&lt; # CONFIG_INPUT_UINPUT is not set
---
&gt; # CONFIG_INPUT_MISC is not set
989,992c667,669
&lt; CONFIG_SERIO_SERPORT=m
&lt; CONFIG_SERIO_CT82C710=m
&lt; CONFIG_SERIO_PARKBD=m
&lt; CONFIG_SERIO_PCIPS2=m
---
&gt; # CONFIG_SERIO_SERPORT is not set
&gt; # CONFIG_SERIO_CT82C710 is not set
&gt; # CONFIG_SERIO_PCIPS2 is not set
1010,1011c687
&lt; CONFIG_SERIAL_8250_CS=m
&lt; CONFIG_SERIAL_8250_ACPI=y
---
&gt; # CONFIG_SERIAL_8250_ACPI is not set
1013,1018c689
&lt; CONFIG_SERIAL_8250_EXTENDED=y
&lt; CONFIG_SERIAL_8250_MANY_PORTS=y
&lt; CONFIG_SERIAL_8250_SHARE_IRQ=y
&lt; # CONFIG_SERIAL_8250_DETECT_IRQ is not set
&lt; CONFIG_SERIAL_8250_MULTIPORT=y
&lt; CONFIG_SERIAL_8250_RSA=y
---
&gt; # CONFIG_SERIAL_8250_EXTENDED is not set
1027,1030c698,699
&lt; # CONFIG_LEGACY_PTYS is not set
&lt; # CONFIG_PRINTER is not set
&lt; CONFIG_PPDEV=m
&lt; # CONFIG_TIPAR is not set
---
&gt; CONFIG_LEGACY_PTYS=y
&gt; CONFIG_LEGACY_PTY_COUNT=256
1041,1042c710,711
&lt; # CONFIG_HW_RANDOM is not set
&lt; CONFIG_NVRAM=m
---
&gt; CONFIG_HW_RANDOM=y
&gt; # CONFIG_NVRAM is not set
1050c719,722
&lt; # CONFIG_AGP is not set
---
&gt; # CONFIG_FTAPE is not set
&gt; CONFIG_AGP=y
&gt; CONFIG_AGP_AMD64=y
&gt; # CONFIG_AGP_INTEL is not set
1052,1059c724,729
&lt; 
&lt; #
&lt; # PCMCIA character devices
&lt; #
&lt; # CONFIG_SYNCLINK_CS is not set
&lt; CONFIG_MWAVE=m
&lt; # CONFIG_RAW_DRIVER is not set
&lt; # CONFIG_HPET is not set
---
&gt; # CONFIG_MWAVE is not set
&gt; CONFIG_RAW_DRIVER=y
&gt; CONFIG_HPET=y
&gt; # CONFIG_HPET_RTC_IRQ is not set
&gt; CONFIG_HPET_MMAP=y
&gt; CONFIG_MAX_RAW_DEVS=256
1070a741
&gt; # CONFIG_I2C_SENSOR is not set
1077a749,754
&gt; # Hardware Monitoring support
&gt; #
&gt; CONFIG_HWMON=y
&gt; # CONFIG_HWMON_DEBUG_CHIP is not set
&gt; 
&gt; #
1095,1111c772
&lt; CONFIG_FB=y
&lt; CONFIG_FB_CFB_FILLRECT=y
&lt; CONFIG_FB_CFB_COPYAREA=y
&lt; CONFIG_FB_CFB_IMAGEBLIT=y
&lt; CONFIG_FB_SOFT_CURSOR=y
&lt; # CONFIG_FB_MACMODES is not set
&lt; # CONFIG_FB_MODE_HELPERS is not set
&lt; # CONFIG_FB_TILEBLITTING is not set
&lt; # CONFIG_FB_CIRRUS is not set
&lt; # CONFIG_FB_PM2 is not set
&lt; # CONFIG_FB_CYBER2000 is not set
&lt; # CONFIG_FB_ASILIANT is not set
&lt; # CONFIG_FB_IMSTT is not set
&lt; # CONFIG_FB_VGA16 is not set
&lt; CONFIG_FB_VESA=y
&lt; CONFIG_FB_VESA_STD=y
&lt; # CONFIG_FB_VESA_TNG is not set
---
&gt; # CONFIG_FB is not set
1113,1130d773
&lt; # CONFIG_FB_HGA is not set
&lt; # CONFIG_FB_NVIDIA is not set
&lt; # CONFIG_FB_RIVA is not set
&lt; # CONFIG_FB_MATROX is not set
&lt; # CONFIG_FB_RADEON_OLD is not set
&lt; # CONFIG_FB_RADEON is not set
&lt; # CONFIG_FB_ATY128 is not set
&lt; # CONFIG_FB_ATY is not set
&lt; # CONFIG_FB_SAVAGE is not set
&lt; # CONFIG_FB_SIS is not set
&lt; # CONFIG_FB_NEOMAGIC is not set
&lt; # CONFIG_FB_KYRO is not set
&lt; # CONFIG_FB_3DFX is not set
&lt; # CONFIG_FB_VOODOO1 is not set
&lt; # CONFIG_FB_TRIDENT is not set
&lt; # CONFIG_FB_GEODE is not set
&lt; # CONFIG_FB_S1D13XXX is not set
&lt; # CONFIG_FB_VIRTUAL is not set
1137,1147d779
&lt; CONFIG_FRAMEBUFFER_CONSOLE=y
&lt; # CONFIG_FONTS is not set
&lt; CONFIG_FONT_8x8=y
&lt; CONFIG_FONT_8x16=y
&lt; 
&lt; #
&lt; # Logo configuration
&lt; #
&lt; # CONFIG_LOGO is not set
&lt; # CONFIG_BACKLIGHT_LCD_SUPPORT is not set
&lt; CONFIG_FB_SPLASH=y
1152,1170c784
&lt; CONFIG_SPEAKUP=y
&lt; CONFIG_SPEAKUP_ACNTSA=y
&lt; CONFIG_SPEAKUP_ACNTPC=y
&lt; CONFIG_SPEAKUP_APOLLO=y
&lt; CONFIG_SPEAKUP_AUDPTR=y
&lt; CONFIG_SPEAKUP_BNS=y
&lt; CONFIG_SPEAKUP_DECTLK=y
&lt; CONFIG_SPEAKUP_DECEXT=y
&lt; # CONFIG_SPEAKUP_DECPC is not set
&lt; CONFIG_SPEAKUP_DTLK=y
&lt; CONFIG_SPEAKUP_KEYPC=y
&lt; CONFIG_SPEAKUP_LTLK=y
&lt; CONFIG_SPEAKUP_SFTSYN=y
&lt; CONFIG_SPEAKUP_SPKOUT=y
&lt; CONFIG_SPEAKUP_TXPRT=y
&lt; 
&lt; #
&lt; # Enter the 3 to 6 character keyword from the list above, or none for no default synthesizer on boot up.
&lt; #
---
&gt; # CONFIG_SPEAKUP is not set
1176,1186c790
&lt; CONFIG_SOUND=y
&lt; 
&lt; #
&lt; # Advanced Linux Sound Architecture
&lt; #
&lt; # CONFIG_SND is not set
&lt; 
&lt; #
&lt; # Open Sound System
&lt; #
&lt; # CONFIG_SOUND_PRIME is not set
---
&gt; # CONFIG_SOUND is not set
1193c797
&lt; CONFIG_USB=m
---
&gt; CONFIG_USB=y
1208c812
&lt; CONFIG_USB_EHCI_HCD=m
---
&gt; CONFIG_USB_EHCI_HCD=y
1211c815,816
&lt; CONFIG_USB_OHCI_HCD=m
---
&gt; # CONFIG_USB_ISP116X_HCD is not set
&gt; CONFIG_USB_OHCI_HCD=y
1214,1216c819,820
&lt; CONFIG_USB_UHCI_HCD=m
&lt; CONFIG_USB_SL811_HCD=m
&lt; CONFIG_USB_SL811_CS=m
---
&gt; CONFIG_USB_UHCI_HCD=y
&gt; CONFIG_USB_SL811_HCD=y
1221,1228c825,827
&lt; CONFIG_USB_AUDIO=m
&lt; 
&lt; #
&lt; # USB Bluetooth TTY can only be used with disabled Bluetooth subsystem
&lt; #
&lt; # CONFIG_USB_MIDI is not set
&lt; CONFIG_USB_ACM=m
&lt; # CONFIG_USB_PRINTER is not set
---
&gt; # CONFIG_USB_BLUETOOTH_TTY is not set
&gt; # CONFIG_USB_ACM is not set
&gt; CONFIG_USB_PRINTER=y
1233c832
&lt; CONFIG_USB_STORAGE=m
---
&gt; CONFIG_USB_STORAGE=y
1235,1242c834,841
&lt; CONFIG_USB_STORAGE_DATAFAB=y
&lt; CONFIG_USB_STORAGE_FREECOM=y
&lt; CONFIG_USB_STORAGE_ISD200=y
&lt; CONFIG_USB_STORAGE_DPCM=y
&lt; CONFIG_USB_STORAGE_USBAT=y
&lt; CONFIG_USB_STORAGE_SDDR09=y
&lt; CONFIG_USB_STORAGE_SDDR55=y
&lt; CONFIG_USB_STORAGE_JUMPSHOT=y
---
&gt; # CONFIG_USB_STORAGE_DATAFAB is not set
&gt; # CONFIG_USB_STORAGE_FREECOM is not set
&gt; # CONFIG_USB_STORAGE_ISD200 is not set
&gt; # CONFIG_USB_STORAGE_DPCM is not set
&gt; # CONFIG_USB_STORAGE_USBAT is not set
&gt; # CONFIG_USB_STORAGE_SDDR09 is not set
&gt; # CONFIG_USB_STORAGE_SDDR55 is not set
&gt; # CONFIG_USB_STORAGE_JUMPSHOT is not set
1247,1250c846
&lt; CONFIG_USB_HID=m
&lt; CONFIG_USB_HIDINPUT=y
&lt; # CONFIG_HID_FF is not set
&lt; CONFIG_USB_HIDDEV=y
---
&gt; # CONFIG_USB_HID is not set
1257,1259c853,856
&lt; CONFIG_USB_AIPTEK=m
&lt; CONFIG_USB_WACOM=m
&lt; CONFIG_USB_KBTAB=m
---
&gt; # CONFIG_USB_AIPTEK is not set
&gt; # CONFIG_USB_WACOM is not set
&gt; # CONFIG_USB_ACECAD is not set
&gt; # CONFIG_USB_KBTAB is not set
1261,1264c858,863
&lt; CONFIG_USB_MTOUCH=m
&lt; CONFIG_USB_EGALAX=m
&lt; CONFIG_USB_XPAD=m
&lt; CONFIG_USB_ATI_REMOTE=m
---
&gt; # CONFIG_USB_MTOUCH is not set
&gt; # CONFIG_USB_ITMTOUCH is not set
&gt; # CONFIG_USB_EGALAX is not set
&gt; # CONFIG_USB_XPAD is not set
&gt; # CONFIG_USB_ATI_REMOTE is not set
&gt; # CONFIG_USB_KEYSPAN_REMOTE is not set
1284,1314c883,888
&lt; CONFIG_USB_CATC=m
&lt; CONFIG_USB_KAWETH=m
&lt; CONFIG_USB_PEGASUS=m
&lt; CONFIG_USB_RTL8150=m
&lt; CONFIG_USB_USBNET=m
&lt; 
&lt; #
&lt; # USB Host-to-Host Cables
&lt; #
&lt; CONFIG_USB_ALI_M5632=y
&lt; CONFIG_USB_AN2720=y
&lt; CONFIG_USB_BELKIN=y
&lt; CONFIG_USB_GENESYS=y
&lt; CONFIG_USB_NET1080=y
&lt; CONFIG_USB_PL2301=y
&lt; CONFIG_USB_KC2190=y
&lt; 
&lt; #
&lt; # Intelligent USB Devices/Gadgets
&lt; #
&lt; # CONFIG_USB_ARMLINUX is not set
&lt; # CONFIG_USB_EPSON2888 is not set
&lt; # CONFIG_USB_ZAURUS is not set
&lt; CONFIG_USB_CDCETHER=y
&lt; 
&lt; #
&lt; # USB Network Adapters
&lt; #
&lt; CONFIG_USB_AX8817X=y
&lt; CONFIG_USB_ZD1201=m
&lt; # CONFIG_USB_MON is not set
---
&gt; # CONFIG_USB_CATC is not set
&gt; # CONFIG_USB_KAWETH is not set
&gt; # CONFIG_USB_PEGASUS is not set
&gt; # CONFIG_USB_RTL8150 is not set
&gt; # CONFIG_USB_USBNET is not set
&gt; CONFIG_USB_MON=y
1319d892
&lt; CONFIG_USB_USS720=m
1324,1352c897
&lt; CONFIG_USB_SERIAL=m
&lt; CONFIG_USB_SERIAL_GENERIC=y
&lt; CONFIG_USB_SERIAL_AIRPRIME=m
&lt; # CONFIG_USB_SERIAL_BELKIN is not set
&lt; # CONFIG_USB_SERIAL_DIGI_ACCELEPORT is not set
&lt; CONFIG_USB_SERIAL_CP2101=m
&lt; # CONFIG_USB_SERIAL_CYPRESS_M8 is not set
&lt; # CONFIG_USB_SERIAL_EMPEG is not set
&lt; # CONFIG_USB_SERIAL_FTDI_SIO is not set
&lt; # CONFIG_USB_SERIAL_VISOR is not set
&lt; # CONFIG_USB_SERIAL_IPAQ is not set
&lt; # CONFIG_USB_SERIAL_IR is not set
&lt; # CONFIG_USB_SERIAL_EDGEPORT is not set
&lt; # CONFIG_USB_SERIAL_EDGEPORT_TI is not set
&lt; # CONFIG_USB_SERIAL_GARMIN is not set
&lt; CONFIG_USB_SERIAL_IPW=m
&lt; # CONFIG_USB_SERIAL_KEYSPAN_PDA is not set
&lt; # CONFIG_USB_SERIAL_KEYSPAN is not set
&lt; # CONFIG_USB_SERIAL_KLSI is not set
&lt; # CONFIG_USB_SERIAL_KOBIL_SCT is not set
&lt; # CONFIG_USB_SERIAL_MCT_U232 is not set
&lt; # CONFIG_USB_SERIAL_PL2303 is not set
&lt; # CONFIG_USB_SERIAL_HP4X is not set
&lt; # CONFIG_USB_SERIAL_SAFE is not set
&lt; # CONFIG_USB_SERIAL_TI is not set
&lt; # CONFIG_USB_SERIAL_CYBERJACK is not set
&lt; # CONFIG_USB_SERIAL_XIRCOM is not set
&lt; CONFIG_USB_SERIAL_OPTION=m
&lt; CONFIG_USB_SERIAL_OMNINET=m
---
&gt; # CONFIG_USB_SERIAL is not set
1359c904
&lt; CONFIG_USB_AUERSWALD=m
---
&gt; # CONFIG_USB_AUERSWALD is not set
1368c913,914
&lt; CONFIG_USB_SISUSBVGA=m
---
&gt; # CONFIG_USB_SISUSBVGA is not set
&gt; # CONFIG_USB_LD is not set
1372c918
&lt; # USB ATM/DSL drivers
---
&gt; # USB DSL modem support
1374,1375d919
&lt; CONFIG_USB_ATM=m
&lt; CONFIG_USB_SPEEDTOUCH=m
1385,1388c929
&lt; CONFIG_MMC=m
&lt; # CONFIG_MMC_DEBUG is not set
&lt; CONFIG_MMC_BLOCK=m
&lt; CONFIG_MMC_WBSD=m
---
&gt; # CONFIG_MMC is not set
1393,1397c934,938
&lt; CONFIG_INFINIBAND=m
&lt; CONFIG_INFINIBAND_MTHCA=m
&lt; # CONFIG_INFINIBAND_MTHCA_DEBUG is not set
&lt; CONFIG_INFINIBAND_IPOIB=m
&lt; # CONFIG_INFINIBAND_IPOIB_DEBUG is not set
---
&gt; # CONFIG_INFINIBAND is not set
&gt; 
&gt; #
&gt; # SN Devices
&gt; #
1410a952
&gt; # CONFIG_EXT2_FS_XIP is not set
1424,1428c966
&lt; CONFIG_JFS_FS=m
&lt; CONFIG_JFS_POSIX_ACL=y
&lt; # CONFIG_JFS_SECURITY is not set
&lt; # CONFIG_JFS_DEBUG is not set
&lt; # CONFIG_JFS_STATISTICS is not set
---
&gt; # CONFIG_JFS_FS is not set
1434,1439c972
&lt; CONFIG_XFS_FS=y
&lt; CONFIG_XFS_EXPORT=y
&lt; CONFIG_XFS_RT=y
&lt; CONFIG_XFS_QUOTA=y
&lt; CONFIG_XFS_SECURITY=y
&lt; CONFIG_XFS_POSIX_ACL=y
---
&gt; # CONFIG_XFS_FS is not set
1444d976
&lt; CONFIG_QUOTACTL=y
1446c978
&lt; # CONFIG_AUTOFS_FS is not set
---
&gt; CONFIG_AUTOFS_FS=y
1463c995
&lt; CONFIG_MSDOS_FS=m
---
&gt; CONFIG_MSDOS_FS=y
1467,1469c999
&lt; CONFIG_NTFS_FS=m
&lt; # CONFIG_NTFS_DEBUG is not set
&lt; # CONFIG_NTFS_RW is not set
---
&gt; # CONFIG_NTFS_FS is not set
1477d1006
&lt; # CONFIG_DEVFS_FS is not set
1480,1483c1009,1011
&lt; CONFIG_TMPFS_XATTR=y
&lt; CONFIG_TMPFS_SECURITY=y
&lt; # CONFIG_HUGETLBFS is not set
&lt; # CONFIG_HUGETLB_PAGE is not set
---
&gt; # CONFIG_TMPFS_XATTR is not set
&gt; CONFIG_HUGETLBFS=y
&gt; CONFIG_HUGETLB_PAGE=y
1497c1025
&lt; CONFIG_SQUASHFS=y
---
&gt; # CONFIG_SQUASHFS is not set
1507c1035
&lt; CONFIG_NFS_FS=m
---
&gt; CONFIG_NFS_FS=y
1508a1037
&gt; # CONFIG_NFS_V3_ACL is not set
1511c1040
&lt; CONFIG_NFSD=m
---
&gt; CONFIG_NFSD=y
1512a1042
&gt; # CONFIG_NFSD_V3_ACL is not set
1515c1045
&lt; CONFIG_LOCKD=m
---
&gt; CONFIG_LOCKD=y
1518c1048,1049
&lt; CONFIG_SUNRPC=m
---
&gt; CONFIG_NFS_COMMON=y
&gt; CONFIG_SUNRPC=y
1521,1524c1052,1057
&lt; CONFIG_SMB_FS=m
&lt; CONFIG_SMB_NLS_DEFAULT=y
&lt; CONFIG_SMB_NLS_REMOTE="cp437"
&lt; # CONFIG_CIFS is not set
---
&gt; CONFIG_SMB_FS=y
&gt; # CONFIG_SMB_NLS_DEFAULT is not set
&gt; CONFIG_CIFS=y
&gt; # CONFIG_CIFS_STATS is not set
&gt; # CONFIG_CIFS_XATTR is not set
&gt; # CONFIG_CIFS_EXPERIMENTAL is not set
1532,1537c1065
&lt; CONFIG_PARTITION_ADVANCED=y
&lt; # CONFIG_ACORN_PARTITION is not set
&lt; # CONFIG_OSF_PARTITION is not set
&lt; # CONFIG_AMIGA_PARTITION is not set
&lt; # CONFIG_ATARI_PARTITION is not set
&lt; # CONFIG_MAC_PARTITION is not set
---
&gt; # CONFIG_PARTITION_ADVANCED is not set
1539,1548d1066
&lt; # CONFIG_BSD_DISKLABEL is not set
&lt; # CONFIG_MINIX_SUBPARTITION is not set
&lt; # CONFIG_SOLARIS_X86_PARTITION is not set
&lt; # CONFIG_UNIXWARE_DISKLABEL is not set
&lt; CONFIG_LDM_PARTITION=y
&lt; # CONFIG_LDM_DEBUG is not set
&lt; # CONFIG_SGI_PARTITION is not set
&lt; # CONFIG_ULTRIX_PARTITION is not set
&lt; # CONFIG_SUN_PARTITION is not set
&lt; # CONFIG_EFI_PARTITION is not set
1578c1096
&lt; # CONFIG_NLS_ASCII is not set
---
&gt; CONFIG_NLS_ASCII=y
1589c1107
&lt; # CONFIG_NLS_ISO8859_15 is not set
---
&gt; CONFIG_NLS_ISO8859_15=y
1597c1115,1116
&lt; # CONFIG_PROFILING is not set
---
&gt; CONFIG_PROFILING=y
&gt; CONFIG_OPROFILE=y
1605c1124
&lt; CONFIG_LOG_BUF_SHIFT=15
---
&gt; CONFIG_LOG_BUF_SHIFT=18
1608d1126
&lt; CONFIG_DEBUG_PREEMPT=y
1613a1132
&gt; # CONFIG_CHECKING is not set
1614a1134
&gt; # CONFIG_IOMMU_DEBUG is not set
1628,1630c1148,1150
&lt; # CONFIG_CRYPTO_NULL is not set
&lt; # CONFIG_CRYPTO_MD4 is not set
&lt; CONFIG_CRYPTO_MD5=y
---
&gt; CONFIG_CRYPTO_NULL=m
&gt; CONFIG_CRYPTO_MD4=m
&gt; CONFIG_CRYPTO_MD5=m
1634,1636c1154,1156
&lt; # CONFIG_CRYPTO_WP512 is not set
&lt; # CONFIG_CRYPTO_TGR192 is not set
&lt; CONFIG_CRYPTO_DES=y
---
&gt; CONFIG_CRYPTO_WP512=m
&gt; CONFIG_CRYPTO_TGR192=m
&gt; CONFIG_CRYPTO_DES=m
1640c1160
&lt; CONFIG_CRYPTO_AES=m
---
&gt; CONFIG_CRYPTO_AES_X86_64=m
1645,1646c1165,1166
&lt; # CONFIG_CRYPTO_KHAZAD is not set
&lt; # CONFIG_CRYPTO_ANUBIS is not set
---
&gt; CONFIG_CRYPTO_KHAZAD=m
&gt; CONFIG_CRYPTO_ANUBIS=m
1650c1170
&lt; # CONFIG_CRYPTO_TEST is not set
---
&gt; CONFIG_CRYPTO_TEST=m
1661c1181
&lt; CONFIG_LIBCRC32C=m
---
&gt; CONFIG_LIBCRC32C=y
