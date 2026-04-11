---
layout: post
title: 'SVN: Care and feeding of a sparse working copy'
date: '2009-06-12T15:40:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


One of the wonderful (and long awaited for us) features in SVN 1.5 was the addition of "sparse" working copies.  This allows you to create a working copy that checks out from the root of the repository, but without having to bring down the entire repository into your working copy.  Which is a great boon for situations where a large monolithic repository is preferred over having lots of smaller repositories.

This was a feature that Visual SourceSafe (VSS) and SourceOffSite (SOS) had for many years prior to SVN 1.5's sparse working copy feature.   We were an SOS shop for a long time prior to switching to SVN back in 2006 and our entire VSS repository was basically monolithic and we'd only bring down what we needed to our local working copies.

(The primary advantage for monolithic working copies is mostly ease of use and ease of administration.  Rather then pester the SVN administrator to create a new repository for every new client or project, users can simply work within the existing project repository and create folders as needed.  Plus, the end-user can more easily do a global update of their working copy overnight without having to write a lengthy batch file to update individual working copies.)

Support for sparse working copies got even better in 1.6 because now you can trim folders back out of your working copy once you no longer need them.  In SVN 1.5, once you told SVN to bring a folder tree down, you were stuck with it and your working copy would slowly bloat.

<b>Creating a sparse working copy:</b>
<ol>

<li>Create the folder on your hard drive (i.e. C:\TGH\Projects).

</li>
<li>Right-click in the folder and use, TortoiseSVN's "SVN Checkout..." option.

</li>
<li>Enter the repository URL (i.e. svn+ssh://svn.tgharold.com/tgh-projects)

</li>
<li>Change the "Checkout Depth" to anything other then "Fully recursive".  (I usually use "Only this item".)

</li>
<li>Click the "OK" button and TortoiseSVN will do a sparse checkout.

</li>
</ol>

<b>Populating your working copy:</b>
<ol>

<li>Right-click anywhere inside your working copy and bring up the TortoiseSVN Repository Browser (TSVN -&gt; Repo-Browser).

</li>
<li>In the Repo-Browser, navigate to the project tree that you want to bring to your working copy.  

</li>
<li>Right-click on the project folder and choose "Update item to revision".  I usually set the "Update Depth" to "Working Copy" as this will bring down the folder and all of the children files and folders below it.

</li>
</ol>

Note: Sometimes the Repo-Browser will lose track of what has / hasn't been brought down to the working copy.  You won't see the "Update item to revision" choice in the right-click menu when this happens.  The solution is to close the Repo-Browser window and open up a new one from a location in your working copy (i.e. go back to step 1).

<b>Trimming your working copy:</b>
<ol>

<li>Right-click on the folder that you want to remove from your working copy and do an "SVN Update".

</li>
<li>Right-click on the folder that you want to remove from your working copy and do an "SVN Commit".  This is to make sure that there's nothing in the working copy that you have forgotten to commit.

</li>
<li>Right-click on the folder that you want to remove from your working copy and use the TortoiseSVN -&gt; Update to revision option.

</li>
<li>Change the "Update Depth" to "Exclude" and click the "OK" button.

</li>
</ol>

Note: If TortoiseSVN does not remove the folder, then there was something in it that was not committed or that it felt you wanted to keep around.  Which is why I recommend doing an Update and then using the Commit dialog to verify that the working copy folder is clean.
