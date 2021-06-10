---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: home
title: Image Shuffle
heading: Image Shuffle
---

<html>
<head>
<style>
* {
  box-sizing: border-box;
}

.column {
  float: left;
  width: 50%;
  padding: 5px;
}

/* Clearfix (clear floats) */
.row::after {
  content: "";
  clear: both;
  display: table;
}
</style>
</head>
<body>

<h2>Images Side by Side</h2>
<p>How to create side-by-side images with the CSS float property:</p>

<div class="row">
  <div class="column">
    <img src="assets/Montauk.jpg" alt="Snow" style="width:100%">
  </div>
  <div class="column">
    <img src="assets/Montauk.jpg" alt="Forest" style="width:100%">
  </div>
</div>

</body>
</html>
