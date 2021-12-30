# Copyright 2021 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Website Blog Search Bar",
    "summary": "Search blog posts",
    "version": "13.0.1.0.0",
    "category": "Blog",
    "website": "https://github.com/oca/website",
    "author": "Sygel, " "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": ["base", "website", "website_blog"],
    "data": ["views/search_blog.xml", "views/website_views.xml"],
}
