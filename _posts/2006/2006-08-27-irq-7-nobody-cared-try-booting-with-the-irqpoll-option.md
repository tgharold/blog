---
layout: post
title: 'irq 7: nobody cared (try booting with the "irqpoll" option)'
date: '2006-08-27T20:23:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Not sure what I'm going to do about this error on the AMD64 Asus M2N32-SLI Deluxe motherboard.

```
Aug 27 20:16:42 san1-azure irq 7: nobody cared (try booting with the "irqpoll" option)
Aug 27 20:16:42 san1-azure 
Aug 27 20:16:42 san1-azure Call Trace: <irq> <ffffffff8024e594>{__report_bad_irq+48}
Aug 27 20:16:42 san1-azure <ffffffff8024e7b9>{note_interrupt+472} <ffffffff8024e078>{__do_IRQ+183}
Aug 27 20:16:42 san1-azure <ffffffff8020ba20>{do_IRQ+57} <ffffffff80207c47>{default_idle+0}
Aug 27 20:16:42 san1-azure <ffffffff80209b94>{ret_from_intr+0} <eoi> <ffffffff80207c72>{default_idle+43}
Aug 27 20:16:42 san1-azure <ffffffff80207e40>{cpu_idle+151} <ffffffff80216a38>{start_secondary+1141}
Aug 27 20:16:42 san1-azure handlers:
Aug 27 20:16:42 san1-azure [<ffffffff8045e684>] (usb_hcd_irq+0x0/0x54)
Aug 27 20:16:42 san1-azure Disabling IRQ #7</ffffffff8045e684></ffffffff80216a38></ffffffff80207e40></ffffffff80207c72></eoi></ffffffff80209b94></ffffffff80207c47></ffffffff8020ba20></ffffffff8024e078></ffffffff8024e7b9></ffffffff8024e594></irq>
```

Putting "irqpoll" on the end of the kernel line in grub.conf causes the system to panic during boot (has to do with the 2nd core in the X2 chip).
