---
layout: post
title: 'Visual Basic RND issues, take 2'
date: '2005-11-25T14:39:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


I talked about this a few months ago in [Visual Basic Rnd() function tricks and traps](/techblog/2005/08/visual-basic-rnd-function-tricks-and.shtml), where I discovered that I wasn't getting a full 32bits of randomness out of VB's Rnd() function in my VBScript/Visual Basic pages.  At the time, I thought it was simply due to Rnd() returning a 32bit IEEE floating point value which really only has 30bits of data.

In reality, the situation is even worse:

[PRNG (Pseudo Random Number Generator) By Michael Meelis](http://www.codeproject.com/tools/prngmit.asp)
[ Microsoft Visual Basic: Pseudo Random Number Generator](http://www.noesis.net.au/prng.php)
[Using and Creating Cryptographic-Quality Random Numbers By Jon Callas](http://www.merrymeet.com/jon/usingrandom.html)
[True random number generators](http://www.robertnz.net/true_rng.html)

VB's Rnd() function only provides 24bits of randomness.  After the 2^24th sample, it starts repeating.  (See [INFO: How Visual Basic Generates Pseudo-Random Numbers for the RND Function](http://support.microsoft.com/support/kb/articles/Q231/8/47.asp).)

Randomize() just contributes to the problem.  See [An Examination of Visual Basic's Random Number Generation By Mark Hutchinson](http://www.15seconds.com/issue/051110.htm) and notice that calling Randomize() is based on the time of the day and only provides around 2^16 different starting points within the 2^24 stream.  So if you're calling Randomize() before every Rnd(), you're only getting 16bits of randomness.  (It's actually worse, because you'll get identical starting points at the same time of day.)
