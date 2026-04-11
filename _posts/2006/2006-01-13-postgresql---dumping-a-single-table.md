---
layout: post
title: 'PostgreSQL - dumping a single table'
date: '2006-01-13T11:46:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>$ pg_dump -Fp -U postgres --table=TABLENAME DATABASENAME &gt; TABLENAME.sql

$ pg_dump -Fp -U postgres --table=TABLENAME DATABASENAME | gzip -c &gt; TABLENAME.sql.gz

Useful for dumping out individual tables from a particular database in plain-text (SQL) format.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2006.shtml">2006</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/PostgreSQL.shtml">PostgreSQL</a>
		<div class="Byline">
			posted by Thomas at 
			[11:46](http://www.tgharold.com/techblog/2006/01/postgresql-dumping-single-table.shtml)

		</div>