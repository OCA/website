Website SEO
===========

Provide the base for an improved SEO handling
---------------------------------------------

This module adds a new seo_url field to the website.seo.metadata model. It means all models which inherit website.seo.metadata will
have the new seo_url field. In general it affects website modules like website_blog, website_forum, website_hr_recruitment etc. The module itself adds no
SEO handling. It is done in additional modules like website_seo_blog.

Provide the base for Robots Meta Information
--------------------------------------------

This module adds a new 'Robots Content' field to the promote panel where the user have full control on the robots meta information.
The selected value is stored in the website_meta_robots field in the website.seo.metadata model. It means all models which inherit website.seo.metadata
will have access to this functionality except of the ir.ui.view model. We add the website_meta_robots field to this model separately because ir.ui.view
doesn't inherit website.seo.metadata.

*The description of the meta robots information is as follow*:

- **index**: pages may be indexed
- **noindex**: pages may not be indexed
- **follow**: pages must be followed
- **nofollow**: pages should not be followed

Important
---------

If you install this module you have to update all modules with models which inherits website.seo.metadata after the installation. In
general it is enough to update the website module. It is needed to populate the seo_url and website_meta_robots fields in all related models of the
installed website modules.

If you uninstall this module or a related SEO module like website_seo_blog you have to clean up the related seo_url and website_meta_robots
entries in the database table ir_model_fields manually. You also have to delete the seo_url and website_meta_robots column in the related database tables
manually.

Regards Bloopark

Known issues / Roadmap
======================

 * make seo_url field editable in the frontend via the promote panel
 * add translation handling for SEO urls

Credits
=======

Contributors
------------

* Robert Rübner (rruebner@bloopark.de)

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose mission is to support the collaborative development of Odoo features and promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.