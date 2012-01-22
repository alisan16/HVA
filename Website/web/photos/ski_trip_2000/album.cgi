#!/usr/local/bin/perl

## Programmer's Notes
# file : filename.jpg
# thumbnail : filename_tn.jpg

# Defaults
$imgdir = ".";
$caption_file = "./captions";


opendir (CURRDIR, $imgdir) or &error ("Could not find image directory.");
@allfiles = readdir CURRDIR;
closedir CURRDIR;

@alltnjpgs = grep /\_tn.jpg$/, @allfiles;
@alltngifs = grep /\_tn.gif$/, @allfiles;

@alltns = (@alltnjpgs, @alltngifs);


open (CAPTION, "$caption_file") or &error ("Could not find caption file.");

# Get captions, put in hash
# Caption file is of the form:
# (name of image) (whitespace) (caption)
while ($line = <CAPTION>) {
	($img_name, $caption) = split (/\s+/, $line);
	$cap_hash{"$img_name"} = $caption;
}
close CAPTION;


print <<EOF;
Content-type: text/html

<html>
<head>
<title>Photo Album</title>

<script>
<!--
var i=0;
function openwindow(url) {
	window.open(url, "new" + i);
	i++;
}
//-->
</script>


</head>
<body bgcolor="#000000" text="#FFFFFF">
<center>
<h1>Ski Trip, Intersession, 2000</h1>

Click on a thumbnail for a bigger picture.

<p>
<table cellspacing=0 cellpadding=10 border=0>
EOF

$i = 0;
foreach $tn (@alltns) {
	($full_img = $tn) =~ s/_tn.jpg/.JPG/;
	if (!($i % 4)) {
		print "\n<tr>\n";
	}
#		print qq(<td><a href="Javascript:window.open\('$imgdir/$full_img',);
	print qq(<td><a href="$full_img" width=100>);
#		print qq('_new','height=200,width=200'\)">);
	print qq(<img src="$tn" border=0></a><br>$cap_hash{"$full_img"}\n);

#		print qq("Javascript:open\('$imgdir/$full_img', '', ''\)">);
#		print qq(<td> <img src="$imgdir/$tn");
#		print qq(onClick="Javascript:open\('$imgdir/$full_img','',);
#		print qq('height=200,width=200'\)">);
#		print qq(<br>$cap_hash{"$full_img"}\n);
	$i++;
}

print <<EOF;
</center>
</table>
</body>
</html>
EOF

exit 0;


sub error {
	print <<EOF;
Content-type: text/html

<html>
<head>
<title>Error</title>
</head>
<body>
<h3>Error</h3>
<p>$_[0]</p>
</body></html>
EOF

exit 1;
}

