.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
    :alt: License: AGPL-3
Openstreetmap
=====================
This module creates a widget, available on your website that allows you to
place the openstreetmap of your companies website wherever you want. It also
replaces the google map in the contacts with an openstreetmap, therefore
severing all connections of your website to google maps.
The area shown on the map is centered in the GPS coordinates specified on the
Company form.

The module adds to the company form a new tab called
"OpenStreetMap GPS coordinates" where you can manually insert the
coordinates you want to show on the map. Coordinates can be also retrieved
automatically using a search feature that uses your company's
Street, city, country and ZIP.


Usage
=====
To use the widget select "EDIT" from the website topbar.
Then select "Insert Blocks".
In the list of available Blocks, in the section "Content" you will find the
openStreetMap widget, just select it and drag it to the desired position
on page. The map will automatically show the GPS position specified in the
Company Options Form.

 SETTING GPS POSITION:

 Go to Settings>Companies>MyCompany>OpenStreetMap GPS coordinates tab
 insert your GPS coordinates manually or press
 "Get my gps coordinates from openstreetmap" , it will do an automatic
 search based on the address registered in your company profile.
 (see Known issues to have best search results).


Known Issues
======================
-GPS search does not return results if info is incomplete:
    street,zipcode,country,city must all be filled.
-GPS search does not return results if the street has a number too
    (only the street name is needed)
-GPS does not return results if ZIPCODE has letters at the end,
    the zipcode numbers should be enough.


Roadmap
=====================
-The current search just gives back the first result Allow to choose the
closest searchresult by selecting from a list of results.
-Automatically try to improve search parameters
    (remove numbers from street name, letters from zipcode, automatically
    fill in country if missing.)
-floating widget
-View options on the widget, to customize map view.


Contributors
------------
* Giovanni Francesco Capalbo  <giovanni@therp.nl>
* Holger Brunn <hbrunn@therp.nl>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

   This module is maintained by the OCA.

   OCA, or the Odoo Community Association, is a nonprofit organization whose mission is to support the collaborative development of Odoo features and promote its widespread use.

   To contribute to this module, please visit http://odoo-community.org.
