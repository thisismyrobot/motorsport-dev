Description
-----------

This is just a sandbox for testing communication between Python and a small serial GPS unit.

The GPS unit: http://www.sparkfun.com/commerce/product_info.php?products_id=8936

Currently, uses python as a server to host 2 pages. The first is a google-maps drive map display. The second page returns values from the gps unit (as json) to ajax calls from the first page.

Future ideas
------------

Would like a mapping source that is not javascript-driven - so can use pyglet opengl for visualisations from web-sourced static images. 