---
layout: post
title: 'System Burnin Testing'
date: '2006-07-26T22:24:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>One of the key things I try to do when setting up a new system is to really hammer it for a few days prior to delivering it to the main office and installing it.  That means exercising the disks, keeping an eye on temps, making the CPU run at 100% utilization and running data to/from the memory.  To do this, there are (4) programs that I use under Windows:

1) [SpeedFan](http://www.almico.com/speedfan.php) - Which does an excellent job at allowing you to see what your CPU and hard drive temperatures are.  You can also display graphs of historical temperatures so that you can see the rise/fall as the component is put under a load.  Configuration is fairly easy, the hard part is identifying which temperature sensor is which.

2) [COSBI OpenSourceMark](http://sourceforge.net/projects/opensourcemark) - I mostly use this tool for it's ability to run continuous copies from drive to drive (or on the same drive) using the "File Copy" test.  You could also rig up something with a batch file if you wanted.

3) [Prime95](http://www.mersenne.org/) - This is pretty much the only tool out there that will find flaky RAM/CPUs because it really puts the RAM, CPU core and CPU cache under a heavy load.  If your system is even the slightest bit unstable, Prime95 will probably detect that instability.  OTOH, if you can pass 24-48 hours of Prime95's torture test, then your system is likely to be rock solid.

Running Prime95 on dual-CPU or dual-core machines is a bit tricky.  You'll need to install as normal, then create a copy of the Prime95 shortcut in the Programs menu.  Simply append " -A1" or " -A2" or " -A3" to the end of the shortcut so that the additional copies know to start up with a different config file rather then using the same one as the first Prime95 copy.  Once you do that, it's easy to configure the two or four Prime95 windows to use a set amount of RAM during the torture / self-test.

4) Task Manager - A builtin component of windows which allows you to see whether your CPU is being fully utilized or not.

...

When running both Prime95 and the disk test at the same time, you should see significant activity of the disk lights along with full CPU utilization in Task Manager.  Some things to watch for:

1) Disk drive lights should be pretty steadily lit, perhaps with a lot of flickering.  You may even hear the heads moving back and forth as the disk does its seeking to read/write data.

2) Hard drive temperatures should be (ideally) no more then 5C to 10C above ambient temperature.  So if it's 28C in the room, drive temps should be around 33C to 38C.  Lower is better.  If the difference between idle and active temperature is large (i.e. 25C at idle but 45C when active) you should take that as an indicator of poor cooling.  A properly cooled drive will only heat up a few degrees when active.

For example:  The WD Raptor 10k SATA that I installed today shows a minimum temp of 32C when idle with a max temp of 34-35C.  That indicates that airflow over the drive is just about perfect and will result in a very long lifespan.  Or at least it won't be heat that kills the drive.  The other SATA drive (400GB Seagate) is 30C at idle and 32-33C when active.

3) Task Manager should be showing 100% utilization along with the majority of RAM in-use (look at the "Total" field under "Commit Charge").  If not, then you're not fully exercising the system's potential.

4) Watch your fan speeds.  Make sure that all of the fans are spinning as they should be.

5) Check the other temperature sensors inside the case.  Different CPUs run at different temperatures, so it is hard to make ballpark recommendations.  The Athlon64 X2 4200+ in a system that I'm burning in right now runs at 60-61C under full load.

6) Watch the Prime95 windows and look for error indicators.  An error in Prime95 indicates that there is a problem with either your RAM or your CPU.  It could be as simple as incorrect timings or maybe the "fast" RAM that you bought isn't as fast as it says it is (and backing off on memory timings will make the system stable).  In general, Prime95 is extremely sensitive to marginal hardware, where MemTest86 might give it a "pass" Prime95 will throw a warning.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2006.shtml">2006</a>
		<div class="Byline">
			posted by Thomas at 
			[22:24](http://www.tgharold.com/techblog/2006/07/system-burnin-testing.shtml)

		</div>