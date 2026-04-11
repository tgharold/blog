---
layout: post
title: 'hde: dma_intr: bad DMA status (dma_stat=35)'
date: '2006-06-20T02:14:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Getting the following messages in my system log:

<code>nogitsune etc # grep 'Jun 16 07' /var/log/messages
Jun 16 07:38:51 nogitsune ntpd[6095]: peer 205.166.121.66 now invalid
Jun 16 07:52:27 nogitsune ntpd[6095]: peer 205.166.121.66 now valid
Jun 16 07:07:52 nogitsune hde: dma_intr: bad DMA status (dma_stat=35)
Jun 16 07:07:52 nogitsune hde: dma_intr: status=0x50 { DriveReady SeekComplete }
Jun 16 07:07:52 nogitsune ide: failed opcode was: unknown
Jun 16 07:16:09 nogitsune hde: dma_intr: bad DMA status (dma_stat=35)
Jun 16 07:16:09 nogitsune hde: dma_intr: status=0x50 { DriveReady SeekComplete }
Jun 16 07:16:09 nogitsune ide: failed opcode was: unknown
Jun 16 07:17:10 nogitsune hde: dma_intr: bad DMA status (dma_stat=35)
Jun 16 07:17:10 nogitsune hde: dma_intr: status=0x50 { DriveReady SeekComplete }
Jun 16 07:17:10 nogitsune ide: failed opcode was: unknown
Jun 16 07:18:13 nogitsune hde: dma_intr: bad DMA status (dma_stat=35)
Jun 16 07:18:13 nogitsune hde: dma_intr: status=0x50 { DriveReady SeekComplete }
Jun 16 07:18:13 nogitsune ide: failed opcode was: unknown
Jun 16 07:23:35 nogitsune hdg: dma_intr: bad DMA status (dma_stat=35)
Jun 16 07:23:35 nogitsune hdg: dma_intr: status=0x50 { DriveReady SeekComplete }
Jun 16 07:23:35 nogitsune ide: failed opcode was: unknown
Jun 16 07:25:52 nogitsune hdg: dma_intr: bad DMA status (dma_stat=35)
Jun 16 07:25:52 nogitsune hdg: dma_intr: status=0x50 { DriveReady SeekComplete }
Jun 16 07:25:52 nogitsune ide: failed opcode was: unknown
Jun 16 07:39:52 nogitsune hde: dma_intr: bad DMA status (dma_stat=35)
Jun 16 07:39:52 nogitsune hde: dma_intr: status=0x50 { DriveReady SeekComplete }
Jun 16 07:39:52 nogitsune ide: failed opcode was: unknown
Jun 16 07:42:35 nogitsune hdg: dma_intr: bad DMA status (dma_stat=35)
Jun 16 07:42:35 nogitsune hdg: dma_intr: status=0x50 { DriveReady SeekComplete }
Jun 16 07:42:35 nogitsune ide: failed opcode was: unknown
Jun 16 07:43:11 nogitsune hdg: dma_intr: bad DMA status (dma_stat=35)
Jun 16 07:43:11 nogitsune hdg: dma_intr: status=0x50 { DriveReady SeekComplete }
Jun 16 07:43:11 nogitsune ide: failed opcode was: unknown
Jun 16 07:45:15 nogitsune hdg: dma_intr: bad DMA status (dma_stat=35)
Jun 16 07:45:15 nogitsune hdg: dma_intr: status=0x50 { DriveReady SeekComplete }
Jun 16 07:45:15 nogitsune ide: failed opcode was: unknown
Jun 16 07:48:05 nogitsune hde: dma_intr: bad DMA status (dma_stat=35)
Jun 16 07:48:05 nogitsune hde: dma_intr: status=0x50 { DriveReady SeekComplete }
Jun 16 07:48:05 nogitsune ide: failed opcode was: unknown
Jun 16 07:48:59 nogitsune hdg: dma_intr: bad DMA status (dma_stat=35)
Jun 16 07:48:59 nogitsune hdg: dma_intr: status=0x50 { DriveReady SeekComplete }
Jun 16 07:48:59 nogitsune ide: failed opcode was: unknown
Jun 16 07:52:03 nogitsune hdg: dma_intr: bad DMA status (dma_stat=35)
Jun 16 07:52:03 nogitsune hdg: dma_intr: status=0x50 { DriveReady SeekComplete }
Jun 16 07:52:03 nogitsune ide: failed opcode was: unknown
Jun 16 07:56:23 nogitsune hde: dma_intr: bad DMA status (dma_stat=35)
Jun 16 07:56:23 nogitsune hde: dma_intr: status=0x50 { DriveReady SeekComplete }
Jun 16 07:56:23 nogitsune ide: failed opcode was: unknown
nogitsune etc #</code>

Basically, they happen anytime that I put a sustained load onto the 2 drives attached to that PCI card.  At the moment, I'm not sure (might be in the archives) which IDE host adapter I'm using for hde and hdg.

From my limited digging, it appears that it may have something to do with lost interrupts, except that I'm not seeing any other messages in the logs regarding that.
