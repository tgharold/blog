---
layout: post
title: 'Visual Basic Rnd() function tricks and traps'
date: '2005-08-30T11:12:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Found this while examining some code results this week.  

One of our bits of code attempts to generate a negative 32bit integer to be used for a random ID.  The code is pretty standard for Visual Basic, and is used just about everywhere:

```
'Int((upperbound - lowerbound + 1) * Rnd + lowerbound)
tmpUserID = Int((-1 - -2147483647 + 1) * Rnd + -2147483647)
```

The problem with this code is that the end result is <i>always</i> divisible by 4.  So instead of getting ~2,147,483,647 unique values, we're only getting around 536,870,911.  Needless to say, that tends to raise a bit of concern about the RNG in Visual Basic.

But, if you do some digging, it becomes pretty apparent why this happens.  The Rnd() function returns a value of type "single", which is a 32-bit IEEE floating point value.  (One bit is used for the sign, 8 bits for the exponent, and 23 bits for the mantissa.) The value returned is always >=0 and <1, which is only about 30bits worth of randomness.

So, when you try to eek out a full 31 or 32 bits worth of randomness, you simply don't have the bits to do it.  There are ways to combine two calls to the Rnd() function to get more bits, but I need to do some research rather then posting a broken method of doing this.
