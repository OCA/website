# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


def migrate(cr, version):
    """Now you can have multiple origins for a destination."""
    cr.execute("""ALTER TABLE website_seo_redirection
                  DROP CONSTRAINT IF EXISTS
                  website_seo_redirection_destination_unique""")
