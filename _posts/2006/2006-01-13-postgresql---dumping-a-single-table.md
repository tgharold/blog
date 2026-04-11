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


$ pg_dump -Fp -U postgres --table=TABLENAME DATABASENAME &gt; TABLENAME.sql

$ pg_dump -Fp -U postgres --table=TABLENAME DATABASENAME | gzip -c &gt; TABLENAME.sql.gz

Useful for dumping out individual tables from a particular database in plain-text (SQL) format.
