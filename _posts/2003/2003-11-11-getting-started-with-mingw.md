---
layout: post
title: 'Getting Started with MinGW'
date: '2003-11-11T14:16:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Programming
- Windows
- Technology
---

<h4>Getting started with MinGW</h4>
So I'm trying to dust off my very rusty (and crusty) C and C++ skills and I've downloaded the [MinGW](http://www.mingw.org/) compiler and the [MSYS](http://www.mingw.org/msys.shtml) package.  On the plus side, compiling with MinGW means that you don't need the Cygwin stuff in order to distribute windows-only binaries - but on the down side, MinGW has very little documentation (I have yet to find a central site).  I guess you could try the GCC home pages since MinGW is a port of the GCC compiler collection.

Anyway, it took me a bit to figure out how to compile and link a C application where I have (1) module (usage.c and usage.h) and (1) program (main.c).  To compile this into a working .exe file requires the following steps if you're doing it by hand:

gcc -c -o usage.o usage.c
gcc -c -o main.o main.c
gcc -o main.exe main.o usage.o

Now that I know those basics, I need to remember how to use makefiles...