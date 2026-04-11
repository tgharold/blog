---
layout: post
title: 'ngg.js and fgg.js site infections'
date: '2008-08-01T14:51:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


<div style="clear:both;"></div>One of our users visited a website that was infected with the ngg.js and fgg.js codes (they get injected into the HTML files on the server towards the end of the page).

We've blocked it in our squid configuration by:

# squid.conf

acl blocked_urls dstdomain "/etc/squid/blocked_urls.squid"
acl blocked_regex urlpath_regex "/etc/squid/blocked_regex.squid"

# Block some URLs
http_access deny blocked_urls
http_access deny blocked_regex

# blocked_urls.squid
.bjxt.ru
.njep.ru
.uhwc.ru

# blocked_regexp.squid
/fgg\.js
/ngg\.js

I won't explain this too much except to say that the blocked_urls file is designed to block top-level domains, while the regexp file is for blocking URLs using a regular expression.<div style="clear:both; padding-bottom:0.25em"></div>
Labels: <a rel="tag" href="http://www.tgharold.com/techblog/labels/2008.shtml">2008</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Security.shtml">Security</a>, <a rel="tag" href="http://www.tgharold.com/techblog/labels/Squid.shtml">Squid</a>
		<div class="Byline">
			posted by Thomas at 
			[14:51](http://www.tgharold.com/techblog/2008/08/nggjs-and-fggjs-site-infections.shtml)

		</div>