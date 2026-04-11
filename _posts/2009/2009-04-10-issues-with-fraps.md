---
layout: post
title: 'Issues with FRAPS'
date: '2009-04-10T09:15:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


I tend to do a lot of FRAPS capture of games that I play for a variety of reasons (the ability to look back, review gameplay, hobby).  However, ever since I upgraded my NVIDIA display drivers a month or two ago, I've started running into the following issue in VirtualDub:

<code>The decompression codec cannot decompress to an RGB format. This is very unusual. Check that any "Force YUY2" options are not enabled in the codec's properties.</code>

Now for the fun symptoms:

- It does not always occur when attempting to do video encoding (usually in the job queue).  

- When it does occur, it breaks the encoding job early on right at the start.

- A task that failed to encode the first time, will often work the second time.  So there's a random element of chance here.

- When things are screwy, sometimes the VirtualDub menu will disappear while using the "File -&gt; Append AVI segment" menu option.  This symptom may or not actually be related to the issue.  By vanish, I mean that the preview window will bleed through from the background and wipe out the dropped down File menu.  But you can still select menu options by moving the mouse up/down.

All of this points to problems in the video codec rendering path.  It's made mass conversion of FRAPS video a real PITA in VirtualDub, because I'm doing 2-pass XVid encoding so a failure in the 1st pass means that the 2nd pass also needs to be tossed.
