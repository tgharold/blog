---
layout: post
title: 'How Much Is That Terabyte in Windows?'
date: '2003-05-15T12:00:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Windows
- Storage
- Technology
---

I remember back in 2003, when hard drives were measured in gigabytes and the idea of a terabyte seemed like science fiction. Now, with drives in the 1TB+ range, it's important to understand how Windows actually reports storage capacity.

When you look at your Windows computer's disk management, you'll notice that the capacity reported is different from what the manufacturer claims. This happens because hard drive manufacturers use decimal (base 10) calculations while Windows uses binary (base 2) calculations.

For example, a 1TB drive is actually:
- 1,000,000,000,000 bytes (decimal)
- 1,099,511,627,776 bytes (binary)

This difference is why a 1TB drive shows up as approximately 931GB in Windows - which seems like a significant loss, but it's actually how things work.

What's your experience with hard drive sizes and capacity calculations? Have you noticed any differences with newer drives?