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

<div class="row">
  <div class="column">
    <img src="assets/Montauk.jpg" style="width:75%">
  </div>
  <div class="column">
    <img src="assets/Montauk%20-%20shuffled.png" style="width:75%">
  </div>
</div>

</body>
</html>
