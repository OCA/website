To use this module:
-------------------

* Drag the widget in any website container
* Save page
* search for any term

Or just create a link to /search , you will find the search interface available there.


To extend this module:
----------------------
The module structure is easily extendible by extending the website.search model
with a method named _do_search_{OBJECTNAME}  The general method _do_search will 
call it and include in search results.
Search results also have a type, that can be used in result rendering or for a 
future javascript search type selection.

