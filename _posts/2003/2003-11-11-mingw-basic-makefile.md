---
layout: post
title: 'MinGW Basic Makefile'
date: '2003-11-11T14:16:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Programming
- Windows
- Technology
---

<h4>Basic Makefile for MinGW</h4>
I've been working with the MinGW compiler and needed a basic makefile to understand how to build my C programs. Here's a simple makefile that demonstrates how to compile and link a basic C project:

```makefile
CC = gcc
CFLAGS = -Wall -g
TARGET = myprogram
SOURCES = main.c util.c

$(TARGET): $(SOURCES)
	$(CC) $(CFLAGS) -o $(TARGET) $(SOURCES)

clean:
	rm -f $(TARGET)
```

This makefile uses the GCC compiler (which is part of MinGW) to compile C source files and create an executable. The `-Wall` flag enables all warnings, and `-g` includes debugging information.

In practice, it's better to have separate object files and use a more complex makefile, but this is sufficient to get started with basic projects.