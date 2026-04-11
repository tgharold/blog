---
layout: post
title: 'Getting started with GPG4Win'
date: '2009-11-20T18:04:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---



[GNU Privacy Guard for Windows Home Page (GPG4Win)](http://www.gpg4win.org/) - The GPG4Win project recently released version 2.0.1 of their product, so I figured it was a good time to reexamine GPG4Win.  There have been a few changes since version 1, most notable for me is that WinPT is no longer part of the GPG4Win distribution.

<b>Installation</b>

For getting started, I strongly recommend using the [gpg4win-light package](http://www.gpg4win.org/download.html) at first as you probably won't need Kleopatra or the german-only manuals).  As for the optional modules, I'd recommend installing GPA and GPGEx at a minimum.  Note that GPGOL is still only compatible with Outlook 2003 and Outlook 2007, so you may wish to not install that module if you use other versions of Microsoft Outlook.  In addition, you probably won't need Claws Mail at first.

By default, GPG4Win puts your key files under (or wherever your HOMEPATH environment variable points to?):

C:\Documents and Settings\USERNAME\Application Data\gnupg

Make sure you include this location in any backup programs that you are using.  Your public and secret keyrings are stored in this folder and need to be backed up regularly.

<b>Public Key Pairs</b>

Now we get into the theoretical realm, GPG now supports RSA signing and encryption keys (in addition to the older DSA for signing and Elgamal for encryption methods).  DSA signing keys are limited to 1024 bit lengths, while RSA signing keys can be much longer (512 to 4096 bits are commonly used).  The only restriction that you should keep in mind for RSA keys is that you should never sign with the same key that you use for encryption (and vice-versa).  In GnuPG v2, the default is now to create (2) RSA keys for the account, one for encryption and one for signing.

Typically, you'll want signing keys to have a very long lifespan (at least 5 years, maybe as long as 20 or more).  This allows you to build a much larger web of trust before your key can no longer be used to sign other keys.  However, you should really expire your encryption key after a few years.  Then, a bit before your encryption key expires, you should add a new encryption subkey to your key with a new expiration date.

Unfortunately, the default creation options in GnuPG will assign the same expiration to both the signing key and the encryption keys.  But this can be fixed using the "gpg --edit-key" command.

<b>Creating a GPG key</b>

```
gpg --gen-key
gpg (GnuPG) 2.0.12; Copyright (C) 2009 Free Software Foundation, Inc.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Please select what kind of key you want:
   (1) RSA and RSA (default)
   (2) DSA and Elgamal
   (3) DSA (sign only)
   (4) RSA (sign only)
Your selection?
```

Unless you have a strong reason to use DSA/Elgamal, you may as well use the defaults in GPG v2 and pick "RSA and RSA".

```
RSA keys may be between 1024 and 4096 bits long.
What keysize do you want? (2048)
```

If you're creating a key that will expire in the next 5 years, I recommend 2048 bits.  For longer durations, you may wish to use 3172 or 4096 bits.

```
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0)</n></n></n></n>
```

For an initial key where you're not protecting anything super critical, I suggest starting with a 25 year (entered as "25y") expiration date.  You will be asked to confirm the expiration date (enter "y" to continue).

```
GnuPG needs to construct a user ID to identify your key.

Real name:
```

For personal use, I suggest just entering your name (i.e. "Thomas Harold").  But if you're creating a key for corporate/business use, I suggest adding a bit more information in this field to make things easier for others if they have more then one key with similar names.  I recommend against using parenthesis in this field as it can be confusing later on.  Square brackets "[]", curly braces "{}", or angle brackets "&lt;&gt;" are all good choices to set elements off from each other.  Some examples:

Thomas Harold, Acme Inc.
Thomas Harold [Acme]
Thomas Harold <acme inc.>
Thomas Harold {Example LTD}

Remember, that this and the next two fields are all public information that will be visible to everyone who uses your public key to send you things, or who uses your signing key to verify a signature.

```
EMail address:
```

This is very simple, you should enter the primary email address that you want associated with this key (i.e. "tgh@tgharold.com").  If you need to add additional email addresses, you can do that later using the "gpg --edit-key" command.

```
Comment:
```

The comment field is a <b>public</b> field and will be seen by others.  I recommend putting website information here, or the full company name, or a combination of the two.  Keep in mind that the contents of this field are typically displayed as enclosed in parenthesis, so avoid using parenthesis or brackets/braces here.  Some examples:

www.tgharold.com
Acme Corporation - www.acme.corp
Example LTD, www.example.com

```
You selected this USER-ID:
    "Thomas Harold [Acme] (Acme Corporate Sales - www.acme.corp) <tgh>"

Change (N)ame, (C)omment, (E)mail or (O)kay/(Q)uit?</tgh>
```

After entering those three values, you will be presented with how it might look to another user.  As you can see, the comment gets wrapped in parenthesis while the email address gets presented inside of angled brackets.  Once you are satisfied with how it looks, enter "O" for "Okay" to continue.

GnuPG will then pop-up a window that prompts you for a passphrase.  <b>This is extremely important.</b>  The passphrase that protects your key from unauthorized use is the weakest link of the entire GnuPG encryption chain.  Pick something lengthy, yet easy to type, that is extremely difficult for someone to guess or attack.  Write it down if you want, but keep that slip of paper secure in a safe or safety deposit box.

You will eventually be presented with something that looks like:

```
gpg: checking the trustdb
gpg: 3 marginal(s) needed, 1 complete(s) needed, PGP trust model
gpg: depth: 0  valid:   2  signed:   0  trust: 0-, 0q, 0n, 0m, 0f, 2u
gpg: next trustdb check due at 2009-12-16
pub   3200R/AAFA2876 2009-11-21 [expires: 2009-12-16]
      Key fingerprint = 0324 917E C27D 2FB0 DDEF  ABFA 4DEE 71F0 AAFA 2876
uid                  Thomas Harold [Acme] (Acme Corporate Sales - www.acme.corp) <tgh>
sub   3200R/1972B360 2009-11-21 [expires: 2009-12-16]</tgh>
```

This means that GnuPG has finished generating your key and has saved it to your keyring.  This sample key (both the encryption key and the signing key) will expire Dec 16, 2009.

The key fingerprint is an important piece of information that should be given to your contacts over a secure channel.  It will allow them to verify that they have the correct key and that they are not subject to a man-in-the-middle (MitM) attack when they use the key.  You can find out the fingerprints of keys in your keyring using the "gpg --fingerprint" command.  Typically, you would send them your public encryption key via email or some other digital method while telling them the key's fingerprint over an entirely different medium such as a telephone call or a physical piece of paper (letter / package).

<b>Editing your key</b>

In order to edit your key using GnuPG, you must know the 8-digit key ID.  In the above example it is listed on the line that starts with "pub".  For example, the key that I just created has a key ID of "AAFA2876":

```
pub   3200R/AAFA2876 2009-11-21 [expires: 2009-12-16]
```

In order to edit the key, you will use the following command:

```
gpg --edit-key aaFa2876
```

As you can see, the key ID is not case sensitive as it is merely an 8-digit hexadecimal string.

```
gpg (GnuPG) 2.0.12; Copyright (C) 2009 Free Software Foundation, Inc.
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Secret key is available.

pub  3200R/AAFA2876  created: 2009-11-21  expires: 2009-12-16  usage: SC
                     trust: ultimate      validity: ultimate
sub  3200R/1972B360  created: 2009-11-21  expires: 2009-12-16  usage: E
[ultimate] (1). Thomas Harold [Acme] (Acme Corporate Sales - www.acme.corp) <tgh>

Command&gt;</tgh>
```

This shows us a bunch of information.  The line that starts with "pub" gives us the following information:

pub - indicates that this is the primary key (you will also see "sub"
3200R - this is a 3200 bit RSA key (R=RSA, D=DSA, g=Elgamal)
AAFA2876 - the key ID (or subkey ID)
created: / expire(d|s): - the creation and expiration dates
usage: - indicates how the key can be used (S=sign, E=encrypt)

Useful commands at this point are:

fpr - show key fingerprint
list - list key and user IDs
quit - exit without making changes

<b>Changing the expiration date</b>

By default, all operations will occur to the primary key (the "pub" line) in this keyset.  So before you edit a subkey, you need to tell GnuPG to work with that key.  These keys are simply numbered 1-N as they are shown in the list.  

```
Command&gt; key 1

pub  3200R/AAFA2876  created: 2009-11-21  expires: 2009-12-16  usage: SC
                     trust: ultimate      validity: ultimate
sub* 3200R/1972B360  created: 2009-11-21  expires: 2009-12-16  usage: E
```

This puts an asterisk by the "sub*" line telling us that we're going to work on the subkey with ID "1972B360".

```
Command&gt; expire
Changing expiration time for a subkey.
Please specify how long the key should be valid.
         0 = key does not expire
      <n>  = key expires in n days
      <n>w = key expires in n weeks
      <n>m = key expires in n months
      <n>y = key expires in n years
Key is valid for? (0) 6m
Key expires at 05/19/10 20:28:31 Eastern Daylight Time
Is this correct? (y/N) y

You need a passphrase to unlock the secret key for
user: "Thomas Harold [Acme] (Acme Corporate Sales - www.acme.corp) <tgh>"
3200-bit RSA key, ID AAFA2876, created 2009-11-21

pub  3200R/AAFA2876  created: 2009-11-21  expires: 2009-12-16  usage: SC
                     trust: ultimate      validity: ultimate
sub* 3200R/1972B360  created: 2009-11-21  expires: 2010-05-20  usage: E</tgh></n></n></n></n>
```

As you can see, the subkey's expiration date changed from "2009-12-16" to "2010-05-20".  If we had wanted to change the primary key's expiration date, we would've entered "key 0" then "expire" at the "Command&gt;" prompt.

Once you are happy with the new expiration dates, enter "save" to save and quit the key editor.

<b>Adding another User ID to the key</b>

Let's say that you want to add a second email address to your key pairs.  As before, you're going to use the "gpg --edit-key" command to do this.

```
gpg --edit-key AaFa2876
```

Then you'll issue the "adduid" command.

```
Command&gt; adduid
Real name: Thomas Harold [Example]
Email address: tgh@example.com
Comment: www.example.com
You selected this USER-ID:
    "Thomas Harold [Example] (www.example.com) <tgh>"

Change (N)ame, (C)omment, (E)mail or (O)kay/(Q)uit? O</tgh>
```

Your key will now look like:

```
pub  3200R/AAFA2876  created: 2009-11-21  expires: 2012-11-20  usage: SC
                     trust: ultimate      validity: ultimate
sub  3200R/1972B360  created: 2009-11-21  expires: 2010-05-20  usage: E
[ultimate] (1)  Thomas Harold [Acme] (Acme Corporate Sales - www.acme.corp) <tgh>
[ unknown] (2). Thomas Harold [Example] (www.example.com) <tgh></tgh></tgh>
```

Now that we have two User IDs associated with this key, we should flag one of them as the primary.

```
Command&gt; uid 2
Command&gt; primary
Command&gt; uid 0

pub  3200R/AAFA2876  created: 2009-11-21  expires: 2012-11-20  usage: SC
                     trust: ultimate      validity: ultimate
sub  3200R/1972B360  created: 2009-11-21  expires: 2010-05-20  usage: E
[ultimate] (1)  Thomas Harold [Example] (www.example.com) <tgh>
[ultimate] (2). Thomas Harold [Acme] (Acme Corporate Sales - www.acme.corp) <tgh></tgh></tgh>
```

The asterisk by the number in parenthesis is the currently selected user ID.  If you see a dot/period after the number in parenthesis, that indicates which user ID is the primary.  

<b>Backing up your key</b>

The following command allows you to export your secret key to an ASCII armored text file.  

```
gpg -a --export-secret-keys aafa2876 &gt;&gt; my-secret-key.asc
```

You should also export your currently usable public encryption key.

```
gpg -a --export aafa2876 &gt;&gt; my-public-key.asc
```

You should print these files out as well as keeping an electronic copy in a secure location such as a safe or safe-deposit box.  Don't leave the secret key ASCII file laying around.  A sealed security envelope with a phrase and the current date written across the sealed flap and then covered with transparent tape is a good countermeasure to detect tampering.
