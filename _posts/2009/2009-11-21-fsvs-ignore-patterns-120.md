---
layout: post
title: 'FSVS ignore patterns (1.2.0)'
date: '2009-11-21T17:29:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Here's an example of a more complex FSVS ignore/take pattern.

On our mail server, we store all mail in MailDir folders under the structure of:

/var/vmail/domainname/username/

We keep our user-specific Sieve scripts in a "Home" folder under that location.

/var/vmail/domainname/username/Home/

So obviously, we want to version the Home folder under each user.  But we don't want to version the other MailDir folders at all.  The trick to this is that because our folder structure is predictable, we can do it in a handful of FSVS ignore patterns.

```
# cd /
# fsvs ignore dump >> /root/fsvs-ignore-yyyymmdd.txt
```

That makes a backup of your current rules, just in case you decide that you don't like your changes (they can be reloaded with "fsvs ignore load < filename").

```
# cd /
# fsvs ignore group:ignore,./var/vmail/lost+found
# fsvs ignore group:take,./var/vmail/*
# fsvs ignore group:take,./var/vmail/*/*
# fsvs ignore group:take,./var/vmail/*/*/Home
# fsvs ignore group:take,./var/vmail/*/*/Home/**
# fsvs ignore group:ignore,./var/vmail/**
```

Line 1 "group:ignore,./var/vmail/lost+found": In our setup /var/vmail is a separate mount point, so we'll want to ignore the lost+found folder.

Line 2 "group:take,./var/vmail/*": This tells FSVS to version anything at or below /var/vmail.

Line 3 "ignore group:take,./var/vmail/*/*": Grabs the next directory level and files below /var/vmail.

Line 4 "group:take,./var/vmail/*/*/Home": Now we grab just the "Home" folder inside of the user's MailDir directory.  This lets us ignore the new|cur|tmp folders as well as the other hidden MailDir folders (such as .Junk).

Line 5 "group:take,./var/vmail/*/*/Home/**": Grab everything inside of Home and below that point.  This will grab all of the Sieve scripts or other files that are located there.  If you wanted to exclude certain files in Home, you would insert that ignore rule above this line.

Line 6 "group:ignore,./var/vmail/**": This is the clean-up rule.  Anything not explicitly mentioned above here will now be ignored.  This keeps us from versioning the messages inside the user's MailDir folders.
