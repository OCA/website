# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).


def migrate(cr, version):
    # rename column to update data in "post-..." script
    cr.execute("ALTER TABLE ir_ui_view "
               "RENAME COLUMN multi_theme_generated "
               "TO multi_theme_generated_tmp")
