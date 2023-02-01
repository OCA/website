On website configuration, Odoo allows to setup a URL for some of the biggest
social media platforms (e.g.: Facebook, Twitter, Youtube). Those URLs are used
to provide a target for the respective social media platforms' icons on the
website. This behaviour causes two kind of issues:

1. The social media icons are displayed wether a URL for that website is provided or not, resulting in some empty link.
2. The functionality is limited to a predefined set of social media platforms.

This module introduces a new model "website.dynamic.link" which is meant
to provide the user a method to define all the external links (social media,
web pages, mail shortcuts, etc.) its websites are connected to, and, for each
of them, what's the URL that should be open.

Finally, this module introduces a "Dynamic Lynk" snippet to the Website
building blocks. This block will automatically be filled with all the links
defined for the website it is in.
