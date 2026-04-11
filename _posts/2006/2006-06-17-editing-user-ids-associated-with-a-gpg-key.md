---
layout: post
title: 'Editing user IDs associated with a GPG key'
date: '2006-06-17T18:29:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Back when one of my users created their GPG keys, they put some bogus text in the Comment field because they didn't realize the public nature of the field.  So their name looks like:

Joe Smith (bogus text) jsmith@example.com

Which isn't really what we wanted it to look like.  So the question is how to adjust the key on the fly using WinPT and publish the changes.  We could just revoke the key and create a new one, but that would require re-signing and re-doing trust information for the new key.

According to various sources, the proper way to do this is with the "REVUID" command (not the "DELUID" command).  While you can never remove a UID associated with your keys from the public key servers, a revocation tells people that the old identity (UID) is no longer used.

Performing the key edit in WinPT:
<ol>

<li>Open up the WinPT key manager, find your key, right-click and choose "Key Edit"

</li>
<li>The "Key Edit" window will display showing the keys associated with this key set (top pane) and the User IDs (UIDs) associated with the key set (lower pane).

</li>
<li>Highlight the incorrect UID, pick "REVUID" from the <i>Command</i> list and click "Ok"

</li>
<li>You will be prompted for your passphrase. Enter it.

</li>
<li>You will be asked to confirm this operation.

</li>
<li>The <i>Validity</i> column for this UID will now say "Revoked".

</li>
<li>In the <i>Command</i> list, choose "ADDUID" and click "OK".

</li>
<li>Enter the correct information for your new ID.  Remember that all 3 fields are public information.  Comment is typically either the name of your company or a website URL.

</li>
<li>Backup your keys (especially the secret key).

</li>
<li>Distribute your updated public key.

</li>
</ol>

For information on backing up a key, see [my previous post on GPG4Win](/techblog/2006/06/getting-started-with-gpg4win.shtml).

Note #1: If you have multiple UIDs associated with a key, you can use the "PRIMARY" command to flag one of the UIDs as the default UID to display in the key list.  Simply select "PRIMARY" from the Command list, highlight the UID you want as the primary and click "OK".  However, this only works in WinPT... in most other implementations, the default UID is the last one added to the key.

Note #2: Prior to exporting the key or giving it to anyone else, you can use the DELUID to remove UIDs from the key. But once you have published a UID for a particular key, only the REVUID command will do what you want.
