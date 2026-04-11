---
layout: post
title: 'Gentoo Samba with ADS'
date: '2004-05-01T01:06:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


Trying to setup my Samba box ("emerge samba") so that I can access the shares from Win2000 and WinXP machines in a Win2000 domain (Active Directory Services).  One of the links indicates that I need MIT Kerberos 1.3.1, which can be installed with "emerge mit-krb5" (AFAICT).  So I'll start with installing that...  I also have the <i>The Official Samba-3 HOWTO and Reference Guide</i> book handy, although it's a bit sparse on exactly how to setup Samba to be a file server in an ADS environment.

(Note: you should emerge the mit-krb5 package prior to emerge the samba package... otherwise you'll have to recompile samba after the mit-krb5 package is installed if you want ADS support... per the official samba howto / reference guide book in the Bruce Peren's series, p 78, section 6.4.3.1.)

Things that I'll probably definitely configure in smb.conf (reading through the smb.conf.example file while mit-krb5 finishes compiling):

    [global]

    # section 1
    netbios name = nezumi
    server string = Samba Server %v

    # section 7 (name resolution)
    local master = no <i>(don't be a master browser)</i>
    domain master = no <i>(don't be a domain master browser)</i>
    wins support = no <i>(don't be a wins server)</i>
    wins server = <i>(my local wins server... not sure if I can list multiple, actually I lie - I don't have a WINS server on my home network, not going to put this line in)</i>

Well, mit-krb5 is finished emerging in, time to test it out.

    # kinit administrator@intra.tgharold.org
    Password for administrator@intra.tgharold.org: ******
    kinit(v5): KDC has no support for encryption type while getting initial credentials

Hmmm, got an error, should be easy to [google]() for that.  Looks like I need to edit the /etc/krb5.conf file, focusing on anywhere that it says "example".  Basically, if your ADS domain is "intra.tgharold.org", then replace every occurence of "example.com" with "intra.tgharold.org".  Which then gives me the next error:

    kinit(v5): Clock skew too great while getting initial credentials

Okay, fixed time... next error!  (Again, trying the kinit command.)

    kinit(v5): KDC reply did not match expectations while getting initial credentials

That error indicates (according to [trouble with fedora and active directory](http://www.netadmintools.com/art172.html)) that there is a case-issue with the principal name.  Also, looking at my krb5.conf file again, I see that I forgot to replace the first "example.com =" occurence in the [realms] section.  I also edited the /etc/krb5kdc/kdc.conf file, again changing any "EXAMPLE.COM" to "INTRA.TGHAROLD.ORG".  Bingo! (and here's the trick... I was testing with the wrong kinit line, [everything after the '@' needs to be uppercase](http://diswww.mit.edu:8008/menelaus.mit.edu/kerberos/21152))

    # kinit administrator@INTRA.TGHAROLD.ORG
    Password for administrator@INTRA.TGHAROLD.ORG: ******

That tested out perfectly.  Back to [Using Samba to Authenticate GNU/Linux Against Active Directory](http://www.netadmintools.com/art172.html), next step is to configure the /etc/samba/smb.conf file for real.  Here's my first attempt:

    [global]
    netbios name = nazumi
    server string = Samba Server %v

    local master = no
    domain master = no
    wins support = no

    workgroup = INTRA
    realm = INTRA.TGHAROLD.ORG
    ads server = DC1.INTRA.TGHAROLD.ORG
    security = ADS
    encrypt passwords = yes

Save, exit, run the following command to join up with the ADS domain:

    # net ads join

Whoops! "net" command not found... um... what did I forget?  Er, forgot to install the samba-client package (which is named what?).  Well, one note that I read indicates that after Kerberos is installed, you have to reinstall samba to have ADS support compiled in.  To uninstall samba, it looks like the command is "emege unmerge samba" (to check before you jump, use "emerge --pretend unmerge samba").  Then "emerge samba" to recompile and re-install samba (probably have to redo the smb.conf file?).  Another reason that I'm uninstalling/reinstalling samba is that the keywords "realm" and "ads server" caused complaints when I ran "testparm /etc/samba/smb.conf" to check my syntax.

Well, samba has finished... yet testparm still complains about the "realm" and "ads server" keywords in the smb.conf file.  My next guess is that I need to recompile the kernel and make sure I have samba support installed.

Helpful links:
[Authenticating to Samba share using "Active Directory Server"](http://linuxquestions.org/questions/history/161506)
[[Samba] force user not working](http://www.mail-archive.com/samba@lists.samba.org/msg36617.html)
