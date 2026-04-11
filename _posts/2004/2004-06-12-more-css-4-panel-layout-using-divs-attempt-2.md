---
layout: post
title: 'More CSS 4-panel layout using DIVs (attempt #2)'
date: '2004-06-12T18:38:00.000-05:00'
author: Thomas Harold
category:
- Tech
tags:
- Technology
---


1) Removed the "Main" DIV tag from the previous attempt.  (Go look at [BlueRobot.com's 2-panel layout](http://bluerobot.com/web/layouts/layout1.html).)

2) Decided that I liked the look of [CSS Layout Techniques: for Fun and Profit](http://glish.com/css/) where the side-bar menu is on the right, which allows text to fill the width of the window once you scroll down past the end.  That looks more natural then a left side menu with a fixed left margin.  Internet Explorer 6 also seems to like that layout a bit better.  ([BlueRobot.com's 2-panel right menu layout](http://bluerobot.com/web/layouts/layout2.html))

HTML and CSS ([see what it looks like](/techblog/css_4panel_layout_example2_Jun2004.shtml), [short-body version](/techblog/css_4panel_layout_example2short_Jun2004.shtml)):
```

<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<title>CSS 4-panel layout example #2 (June 2004)</title>
<style media="screen" type="text/css">
body {
background-color: White;
color: Black;
font-family: verdana, arial, helvetica, sans-serif;
}
#TopNav {
background-color: Fuchsia;
padding: 2px;
}
#SideBar {
background-color: Gray;
float: right;
width: 15%;
}
#BlogBody {
background-color: Orange;
padding: 2px;
}
#Footer {
background-color: Purple;
clear: right;
padding: 2px;
}
</style>
</head>
<body>
<div id="TopNav">foo foo foo foo foo foo</div>
<div id="SideBar">sidebar<br>sidebar<br><br>sidebar<br>sidebar<br>sidebar<br>sidebar</div>
<div id="BlogBody">
blog body blog body blog
</div>
<div id="Footer">footer-copyright</div>
</body>
</html>

```
Bugs:<ol>
<li>
<b>[IE5/Windows]</b>: It's possible that this layout will not work properly on Internet Explorer 5 for MS-Windows.  I suspect that IE5's quirks won't really matter in this particular layout, but I have yet to test it.

</li>
</ol>
