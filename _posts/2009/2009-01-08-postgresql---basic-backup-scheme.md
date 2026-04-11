---
layout: post
title: 'PostgreSQL - Basic backup scheme'
date: '2009-01-08T08:24:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Here's a basic backup scheme.  We're using pg_dump in plain-text mode, compressing the output with bzip2, and writing the results out to files named after the database, schema and table name.  It's not the most efficient method, but allows us to go back to:

- any of the past 7 days
- any Sunday within the past month
- the last week of each month in the past quarter
- the last week of each quarter within the past year
- the last week of each year

Which is about 24-25 copies of the data, stored on the hard drive.  So you'll need to make sure that you have enough space on the drive to handle all of these copies.

Most of the grunt work is handled by the include script, the daily / weekly / monthly backup scripts simply setup a few variables and then call the main include script.

<b>backup_daily.sh</b>
```
#!/bin/bash
# DAILY BACKUPS (writes to a daily folder each day)
DAYNR=`date +%w`
echo $DAYNR
DIR=/backup/pgsql/daily/$DAYNR/
echo $DIR

source ~/bin/include_backup_compressed.sh
```

<b>backup_weekly.sh</b>
```
#!/bin/bash
# WEEKLY BACKUPS
# Backups go to a five directories based on the day of the month
# converted into 1-5 based on modulus arithmetic.  The fifth week
# will sometimes be left over for a few months depending on how
# many weeks there are in the year.
WEEKNR=`date +%d`
echo $WEEKNR
let "WEEKNR = (WEEKNR+6) / 7"
echo $WEEKNR
DIR=/backup/pgsql/weekly/$WEEKNR/
echo $DIR

source ~/bin/include_backup_compressed.sh
```

<b>backup_monthly.sh</b>
```
#!/bin/bash
# MONTHLY BACKUPS
# Backups go to three directories based on the month of year
# converted into 1-3 based on modulus arithmetic.
MONTHNR=`date +%m`
echo $MONTHNR
let "MONTHNR = ((MONTHNR -1) % 3) + 1"
echo $MONTHNR
DIR=/backup/pgsql/monthly/$MONTHNR/
echo $DIR

source ~/bin/include_backup_compressed.sh
```

<b>backup_quarterly.sh</b>
```
#!/bin/bash
# QUARTERLY BACKUPS
# Backups go to a four directories based on the quarter of the year
# converted into 1-4 based on modulus arithmetic.
QTRNR=`date +%m`
echo $QTRNR
let "QTRNR = (QTRNR+2) / 3"
echo $QTRNR
DIR=/backup/pgsql/quarterly/$QTRNR/
echo $DIR

source ~/bin/include_backup_compressed.sh
```

<b>backup_yearly.sh</b>
```
#!/bin/bash
# ANNUAL BACKUPS
YEARNR=`date +%Y`
echo $YEARNR
DIR=/backup/pgsql/yearly/$YEARNR/
echo $DIR

source ~/bin/include_backup_compressed.sh
```

<b>include_backup_compressed.sh</b>
```
#!/bin/bash
# Compressed backups to $DIR
echo $DIR
DBS=$(psql -l | grep '|' | awk '{ print $1}' | grep -vE '^-|^Name|template[0|1]')
for d in $DBS
do
    echo $d
    DBDIR=$DIR/$d
    if ! test -d $DBDIR
    then
        mkdir -p $DBDIR
    fi
    SCHEMAS=$(psql -d $d -c '\dn' | grep '|' | awk '{ print $1}' \
        | grep -vE '^-|^Name|^pg_|^information_schema')
    for s in $SCHEMAS
    do
        echo $d.$s
        TABLES=$(psql -d $d -c "SELECT schemaname, tablename FROM pg_catalog.pg_tables WHERE schemaname = '$s';" \
            | grep '|' | awk '{ print $3}' | grep -vE '^-|^tablename')
        for t in $TABLES
        do
            echo $d.$s.$t
            if [ $s = 'public' ]
            then
                pg_dump -a -b -O -t $t -x $d | bzip2 -c2 &gt; $DIR/$d/$s.$t.sql.bz2
            else
                pg_dump -a -b -O -t $s.$t -x $d | bzip2 -c2 &gt; $DIR/$d/$s.$t.sql.bz2
            fi
        done
    done
done
```

We tried using gzip instead of bzip2, but found that bzip2 worked a little better even though it uses up more CPU.  We use a block size of only 200k for bzip2 in order to be more friendly to an rsync push to an external server.
