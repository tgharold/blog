---
layout: post
title: 'Benchmarking - bonnie'
date: '2006-08-19T15:06:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


The first test is done on /dev/md3 (composed of partitions on /dev/hda and /dev/sda).

<pre>nogitsune tmp # bonnie -s 16384 -m nogitsune-vgmirror
File './Bonnie.9315', size: 17179869184
Writing with putc()...done
Rewriting...done
Writing intelligently...done
Reading with getc()...done
Reading intelligently...done
Seeker 1...Seeker 2...Seeker 3...start 'em...done...done...done...
              -------Sequential Output-------- ---Sequential Input-- --Random--
              -Per Char- --Block--- -Rewrite-- -Per Char- --Block--- --Seeks---
Machine    MB K/sec %CPU K/sec %CPU K/sec %CPU K/sec %CPU K/sec %CPU  /sec %CPU
nogitsun 16384 16714 39.6 21765  8.4 12889  4.3 42827 80.7 55645  5.0 155.6  0.4</pre>

Test results for a 3-disk RAID5 volume on Nogitsune:

<pre>nogitsune backup # bonnie -s 16384 -m raid5-{3}
File './Bonnie.9472', size: 17179869184
Writing with putc()...done
Rewriting...done
Writing intelligently...done
Reading with getc()...done
Reading intelligently...done
Seeker 1...Seeker 2...Seeker 3...start 'em...done...done...done...
              -------Sequential Output-------- ---Sequential Input-- --Random--
              -Per Char- --Block--- -Rewrite-- -Per Char- --Block--- --Seeks---
Machine    MB K/sec %CPU K/sec %CPU K/sec %CPU K/sec %CPU K/sec %CPU  /sec %CPU
raid5-{3 16384 12250 30.9 15062  8.3 10926  6.3 34752 65.0 84890 15.4 134.5  0.7
nogitsune backup # </pre>

These are test results for the RAID1 set on the VIA C3 unit.

<pre>nezumi / # bonnie -s 2047 -m nezumi-raid1
File './Bonnie.22025', size: 2146435072
Writing with putc()...done
Rewriting...done
Writing intelligently...done
Reading with getc()...done
Reading intelligently...done
Seeker 1...Seeker 2...Seeker 3...start 'em...done...done...done...
              -------Sequential Output-------- ---Sequential Input-- --Random--
              -Per Char- --Block--- -Rewrite-- -Per Char- --Block--- --Seeks---
Machine    MB K/sec %CPU K/sec %CPU K/sec %CPU K/sec %CPU K/sec %CPU  /sec %CPU
nezumi-r 2047  2637 94.2 27421 57.8 12256 18.9  2665 93.7 29279 25.7 231.7  5.9
nezumi / # </pre>

Here's is the Celeron 566MHz unit showing performance for the RAID1 array:

<pre>coppermine svn # bonnie -s 2047 -m coppermine-raid1
File './Bonnie.8564', size: 2146435072
Writing with putc()...done
Rewriting...done
Writing intelligently...done
Reading with getc()...done
Reading intelligently...done
Seeker 1...Seeker 2...Seeker 3...start 'em...done...done...done...
              -------Sequential Output-------- ---Sequential Input-- --Random--
              -Per Char- --Block--- -Rewrite-- -Per Char- --Block--- --Seeks---
Machine    MB K/sec %CPU K/sec %CPU K/sec %CPU K/sec %CPU K/sec %CPU  /sec %CPU
coppermi 2047  1087 19.7  1272  6.6  1020 19.5  3505 95.4  6763 78.9 143.8  5.5
coppermine svn #</pre>

The following is the Celeron 566MHz talking to a single 120GB 5400rpm drive:

<pre>coppermine backup # bonnie -s 2047 -m direct          
File './Bonnie.8837', size: 2146435072
Writing with putc()...done
Rewriting...done
Writing intelligently...done
Reading with getc()...done
Reading intelligently...done
Seeker 1...Seeker 2...Seeker 3...start 'em...done...done...done...
              -------Sequential Output-------- ---Sequential Input-- --Random--
              -Per Char- --Block--- -Rewrite-- -Per Char- --Block--- --Seeks---
Machine    MB K/sec %CPU K/sec %CPU K/sec %CPU K/sec %CPU K/sec %CPU  /sec %CPU
direct   2047  4517 83.2 11374 58.1  9073 54.7  6932 98.6 36154 52.7  99.8  3.2
coppermine backup #</pre>
