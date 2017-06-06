Website SEO Blog
================

Provide an improved SEO handling for the blog module
----------------------------------------------------

This module adds a SEO handling for blog and blog posts. It means that blogs and blog posts use now the seo_url field provided by the
website_seo module. One goal of these changes is the reducing of the blog url level, means we reduce the url level from 2 to 1 for blogs and from 4 to 2 for
blog posts. Another goal is the separation between the blog and blog post names and the urls, means you can change the blog and blog post names later
without changing the urls.

The blog url changes from "/blog/slugged_blog_name_ID" to "/blog-seo_url". Example: if the blog seo_url is "our-news" the blog url
http://www.yourdomain.de/blog/our-news-1 is also available by http://www.yourdomain.de/blog-our-news. The fix part "blog-" is important because we need a
unique url part for the odoo routers. Without this fix part there are problems with different languages and translations. Maybe we address this issue at a
later time. You don't need to add "blog-" to the seo_url field but you need to add "blog-" to all links which refers to the blog.

The blog post url changes from "/blog/slugged_blog_name_ID/post/slugged_blog_post_name_ID" to "/blog-seo_url/seo_url". Example: if the
blog post seo_url is "my-first-blogpost" the blog post url http://www.yourdomain.de/blog/our-news-1/post/my-first-blogpost is also available by
http://www.yourdomain.de/blog-our-news/my-first-blogpost.

The original routers for blogs and blog posts are still available which means that the urls are also available by the old url
structure. The reasons are that it is not that easy to delete or deactivate routers in another module and some functions like the blog post creation in the
frontend won't work well.

Important
---------

If you install this module and you haven't installed the module website_seo and update the module website before you have to update
all modules with models which inherits website.seo.metadata after the installation. In general it is enough to update the website module. It is needed to
populate the seo_url field in all related models of the installed website modules.

If you install this module in an existing database it will add the SEO urls of existing blogs and blog posts based on the names
automatically.

After the module installation you have to update the website menu entry with the correct link manually.

Regards Bloopark

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