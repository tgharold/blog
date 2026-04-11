---
layout: post
title: 'CSS 4-panel layout using DIVs'
date: '2004-06-12T17:44:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


You'd think it would be simple, right?  Oh, young grasshopper, you have much to learn!  Actually, it's not all <em>that</em> bad, just tedious to get a layout up and running.  Took me about 2 hours of trial-n-error, and looking at some of the sites over at the [CSS Zen Garden](http://www.mezzoblue.com/zengarden/).  Finally, [Michael Pick's blog entry about the CSS Zen Garden](http://www.mikepick.com/news/archives/000086.html) proved to be the most useful as I teased apart his DIVs and his CSS file.  Mike's page was already close to the layout that I wanted and his CSS file was pretty simple.

My goal for this blog's design is a navigation bar across the top of the page, a footer at the bottom of the page, a side-bar containing links to the various archive pages, and a main body that is 80-85% of the page width.  This is somewhat similar to the diagram under [section 9.6.1 (Fixed positioning)](http://www.w3.org/TR/REC-CSS2/visuren.html#fixed-positioning) of the [W3C.org CSS2 Specification](), except that I don't want to use fixed positioning.

First, start with the following HTML file ([see what it looks like](/techblog/css_4panel_layout_example_Jun2004.shtml)):
```

&lt;!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd"&gt;
&lt;html&gt;
&lt;head&gt;
&lt;title&gt;CSS 4-panel layout example (June 2004)&lt;/title&gt;
&lt;style media="screen" type="text/css"&gt;
body {
background-color: White;
color: Black;
font-family: verdana, arial, helvetica, sans-serif;
margin: 0px;
padding: 0px;
}
#Main {
background-color: Blue;
}
#TopNav {
background-color: Fuchsia;
margin: 0;
padding: 2px;
}
#SideBar {
background-color: Gray;
clear: none;
float: left;
margin-top: 0px;
padding: 2px;
width: 14%;
}
#BlogBody {
background-color: Orange;
height: 200px; /* must be larger then height of SideBar to fix IE6 glitch */
margin-bottom: 10px;
margin-left: 15%;
margin-top: 10px;
padding: 2px;
}
#Footer {
background-color: Purple;
clear: both;
padding: 2px;
}
&lt;/style&gt;
&lt;/head&gt;
&lt;body&gt;
&lt;div id="Main"&gt;
&lt;div id="TopNav"&gt;foo foo foo foo foo foo&lt;/div&gt;
&lt;div id="SideBar"&gt;sidebar&lt;br&gt;sidebar&lt;br&gt;&lt;br&gt;sidebar&lt;br&gt;sidebar&lt;br&gt;sidebar&lt;br&gt;sidebar&lt;/div&gt;
&lt;div id="BlogBody"&gt;
blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body blog body
&lt;/div&gt;
&lt;div id="Footer"&gt;footer-copyright&lt;/div&gt;
&lt;/div&gt;
&lt;/body&gt;
&lt;/html&gt;

```
Yes, those are <b>very ugly</b> colors.  But it does make it very easy to see where the various panels have ended up on the page.

Bugs:<ol>
<li>
<b>[IE6]</b> If the content of the "BlogBody" DIV does not contain enough text to make the height of the DIV more then that of the "SideBar" DIV then the body panel will not display properly.  The work-around is to specify a CSS height value that is larger then the height of the "SideBar" DIV.  I'm going to play around with the design some more and see if I can get rid of that issue (and get the side-bar to be the full height of the page).

</li>
</ol>
