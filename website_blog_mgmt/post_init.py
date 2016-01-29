# -*- coding: utf-8 -*-
# Copyright 2015 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


def post_init(cr, registry):
    """Install hook
    fill website_publication_date field with create_date value for published
    blog.post
    """
    cr.execute("""
        UPDATE
            blog_post
        SET
            website_publication_date = create_date
        WHERE
            website_published = true
    """)
