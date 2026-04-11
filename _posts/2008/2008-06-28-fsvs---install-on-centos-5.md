---
layout: post
title: 'FSVS - Install on CentOS 5'
date: '2008-06-28T22:52:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>(Note: This has been mostly superseded by my newer post [FSVS: Install on CentOS 5.4](/techblog/2009/11/fsvs-install-on-centos-54.shtml))

The following should be enough (and is probably overkill) to install all of the dependencies that FSVS 1.1.16 needs on CentOS 5 (and CentOS 5.1)

# yum install subversion subversion-devel ctags apr apr-devel gcc gdbm gdbm-devel pcre pcre-devel apr-util-devel

# ./configure
configure: ***  Now configuring FSVS   ***
checking for gcc... gcc
checking for C compiler default output file name... a.out
checking whether the C compiler works... yes
checking whether we are cross compiling... no
checking for suffix of executables... 
checking for suffix of object files... o
checking whether we are using the GNU C compiler... yes
checking whether gcc accepts -g... yes
checking for gcc option to accept ISO C89... none needed
checking how to run the C preprocessor... gcc -E
configure: "CFLAGS=-g -O2 -D_GNU_SOURCE=1 -D_FILE_OFFSET_BITS=64 -idirafter /usr/local/include -idirafter /usr/include -idirafter /openpkg/include -idirafter /usr/include/apr-1"
configure: "LDFLAGS= -L/usr/local/lib -L/openpkg/lib"
checking for pcre_compile in -lpcre... yes
checking for apr_md5_init in -laprutil-1... no
configure: error: Sorry, can't find APR.
See `config.log' for more details.

Note the addition of "apr-util-devel" at the end of the "yum install" line.  This fixes the error when you run ./configure for FSVS and get the "can't find APR" error.

In older versions of CentOS 5, we did not need to also specify the apr-util-devel package.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2008.shtml">2008</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/FSVS.shtml">FSVS</a>
		<div class="Byline">
			posted by Thomas at 
			[22:52](http://www.tgharold.com/techblog/2008/06/fsvs-install-on-centos-5.shtml)

		</div>