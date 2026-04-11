---
layout: post
title: 'Troubleshooting (comparison of kernel configs)'
date: '2005-11-21T22:05:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


I now have a few sample kernel configs from kind folks in alt.os.linux.gentoo.  There are two that I've focused in on (mostly because they posted first and they gave background on the config files).

[2005_1-LiveCDConfig.txt](/techblog/Gentoo/AMD64/2005_1-LiveCDConfig.txt) - This is the .config file from the AMD64 2005.1 LiveCD.  Since I know this kernel works, it's a prime starting point for researching why I'm having the issues that I'm having.

[Anton-AsusK8VSE-Sep2005-config.txt](/techblog/Gentoo/AMD64/Anton-AsusK8VSE-Sep2005-config.txt) - This kernel config is for an Asus K8VSE, which isn't exactly the board that I'm using (an Asus A8V).  However, it is at least a VIA chipset so is pretty relevant.  Comparing against this helps to narrow what is different between my kernel, Anton's kernel and the kernel config on the LiveCD.

[Scharf-AsusA8V-Aug2005-config.txt](/techblog/Gentoo/AMD64/Scharf-AsusA8V-Aug2005-config.txt) - This is a kernel config for an Asus A8V (same motherboard as me).  So it will help me verify my particular configuration.

Now for the comparison files.  These were created by GNU's diff3 tool on my WinXP laptop, but the output should be pretty standard diff3 output.  File #1 is always the LiveCD, file #2 is my current kernel config and file #3 is whatever .config file that I'm comparing against.

[LiveCD-vs-Kernel11141600-vs-Anton.txt](/techblog/Gentoo/AMD64/LiveCD-vs-Kernel11141600-vs-Anton.txt)

[LiveCD-vs-Kernel11141600-vs-Scharf.txt](/techblog/Gentoo/AMD64/LiveCD-vs-Kernel11141600-vs-Scharf.txt)

Lines that are the same between the LiveCD and the sample config, but *different* on my config would show up as:

```
1:35c
3:35c
  CONFIG_HOTPLUG=y
2:36c
  # CONFIG_HOTPLUG is not set
```

CONFIG_HOTPLUG is set as "y" in both the LiveCD kernel config and Anton's kernel config, but not defined in my kernel config.  Naturally, my first pass through the comparison is looking for instances like this and then researching the option to understand whether it should be uniquely set on my system.

Now for the details, I've identified a few troublespots in my kernel config that could be causing issues (these are comparisons against the Scharf config).  What I'm finding is that there are very few places in my config where I'm doing something different then the Scharf config (but the LiveCD is the same as the Scharf config).:

```
1:35c
3:35c
  CONFIG_HOTPLUG=y
2:36c
  # CONFIG_HOTPLUG is not set
```

Both Anton/Scharf configs set this the same way as the LiveCD.

```
1:61c
3:60c
  # CONFIG_MODULE_FORCE_UNLOAD is not set
2:62c
  CONFIG_MODULE_FORCE_UNLOAD=y
```

Both Anton/Scharf configs set this the same way as the LiveCD.

```
1:110c
3:102c
  # CONFIG_SOFTWARE_SUSPEND is not set
2:120,121c
  CONFIG_SOFTWARE_SUSPEND=y
  CONFIG_PM_STD_PARTITION=""
```

The software suspend option is probably not the cause of my troubles.  Anton's config uses software suspend to a dedicated partition.  However, I should still plan on turning this off since I'm not going to use software suspend.

```
1:211c
3:189c
  # CONFIG_IA32_AOUT is not set
2:211c
  CONFIG_IA32_AOUT=y
```

Anton configuration has this set to "Y", the Scharf has it not set.

```
1:895c
3:613c
  # CONFIG_NETCONSOLE is not set
2:591,595c
  CONFIG_NETCONSOLE=y
  CONFIG_NETPOLL=y
  # CONFIG_NETPOLL_RX is not set
  # CONFIG_NETPOLL_TRAP is not set
  CONFIG_NET_POLL_CONTROLLER=y
```

Mine is the only config to set this to "Y".

```
1:1597c
3:1334c
  # CONFIG_PROFILING is not set
2:1089,1090c
  CONFIG_PROFILING=y
  CONFIG_OPROFILE=y
```

Probably not an issue.  The Anton config sets this to "Y"/"M" instead of "Y"/"Y".

Updates:

None of the above settings seem to have made any difference.
