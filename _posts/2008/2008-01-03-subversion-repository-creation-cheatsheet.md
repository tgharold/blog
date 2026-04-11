---
layout: post
title: 'Subversion repository creation cheatsheet'
date: '2008-01-03T07:39:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Whenever I setup new SVN repositories, I always create a unix group for people who need read/write access to the repository.  If the repository is named "tgh-public", then I choose to name the group as "svn-tgh-public".

I also generally designate a single user as the initial owner of the SVN repository folder under /var/svn.  Alternately, you could just leave the repository owned by root.

    # cd /var/svn
    (your repositories may be stored elsewhere)
    # /usr/sbin/groupadd svn-repositoryname
    # svnadmin create /var/svn/repositoryname
    # chmod -R 770 repositoryname
    # chmod -R g+s repositoryname/db
    # chown -R username:svn-repositoryname repositoryname
    # /usr/sbin/usermod -a -G svn-repositoryname username

Notes:
<ul>

<li>You'll want to repeat the "usermod" command for each person who will have access to the new repository.

</li>
<li>The chmod value of 770 means that anyone who is either the "username" or who belongs to the "svn-repositoryname" group will be able to access this repository via SVN+SSH and make changes.

</li>
<li>If you want to allow public reads, then you should use a chmod value of 774 which allows everyone read access to the folders.

</li>
<li>Forgetting to set the sticky bit for the group will result in a repository that breaks as different users edit the contents. If you dig through the contents of the FSFS directories, you'll see that files were created with ownership username:username instead of belonging to the group who is responsible for that repository.

</li>
</ul>
