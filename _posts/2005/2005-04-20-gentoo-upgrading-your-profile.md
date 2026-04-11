---
layout: post
title: 'Gentoo Upgrading your Profile'
date: '2005-04-20T23:59:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


At some point, I need to upgrade my Gentoo profile from 2004.3 to 2005.0.  Here's the error message that you see on screen when you need to do this.

<code>livecd linux # emerge (something)

!!! Your current profile is deprecated and not supported anymore.
!!! Please upgrade to the following profile if possible:
        default-linux/x86/2005.0

To upgrade do the following steps:
# emerge -n '&gt;=sys-apps/portage-2.0.51'
# cd /etc/
# rm make.profile
# ln -s ../usr/portage/profiles/default-linux/x86/2005.0 make.profile

# Gentoo has switched to 2.6 as the defaults for headers/kernels.  If you wish
# to use 2.4 headers/kernels, then you should do the following to upgrade:
# emerge -n '&gt;=sys-apps/portage-2.0.51'
# cd /etc/
# rm make.profile
# ln -s ../usr/portage/profiles/default-linux/x86/2005.0/2.4 make.profile

# More information can be found at the following URLs:
# http://www.gentoo.org/doc/en/gentoo-upgrading.xml
# http://www.gentoo.org/doc/en/migration-to-2.6.xml</code>
