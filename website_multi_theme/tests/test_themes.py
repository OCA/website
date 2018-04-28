# -*- coding: utf-8 -*-
# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.tests.common import TransactionCase


THEME_MODULE = 'theme_module'


class TestThemes(TransactionCase):

    def _create_view(self, parent, xml_id, arch):
        module, _ = xml_id.split('.')
        view = self.env['ir.ui.view'].create({
            'inherit_id': parent.id,
            'arch': arch,
            'key': xml_id,
        })
        self.env['ir.model.data'].create({
            'name': xml_id,
            'model': 'ir.ui.view',
            'module': module,
            'res_id': view.id,
        })
        return view

    def test_dependency(self):
        """Test that dependency's views are copied too"""
        theme = self.env.ref('website_multi_theme.demo_multi')
        website = self.env.ref("website.default_website")
        dep_view = self.env.ref('website.footer_custom')

        theme._convert_assets()
        # setting multi_theme_id calls _multi_theme_activate
        website.multi_theme_id = theme

        self.assertTrue(
            website._find_duplicated_view_for_website(dep_view),
            "Dependency's view was not copied")

        theme.write({'dependency_ids': [(5, 0, 0)]})

        theme._convert_assets()
        website._multi_theme_activate()

        self.assertFalse(
            website._find_duplicated_view_for_website(dep_view),
            "The dependency is removed, but its view still has duplicate")

    def test_copied_parent(self):
        """Test a case, when copied view has to reference
        to copied parent instead of original one"""

        assets_frontend = self.env.ref('website.assets_frontend')

        # data below is simplified version of theme_clean module.

        # similar to theme_clean.less
        middle_view = self._create_view(
            assets_frontend,
            '%s.middle_view' % THEME_MODULE,
            """<?xml version="1.0"?>
<data name="middle view" inherit_id="website.assets_frontend">
        <xpath expr="//link[last()]" position="after">
            <!-- middle_view -->
        </xpath>
</data>
            """
        )

        # similar to one of the options,
        # e.g. theme_clean.option_bg_shade_light2
        self._create_view(
            middle_view,
            '%s.option_view' % THEME_MODULE,
            """<?xml version="1.0"?>
<data name="option view" inherit_id="%s.middle_view">
        <xpath expr="." position="inside">
            <!-- option_view -->
        </xpath>
</data>
            """ % THEME_MODULE
        )

        theme = self.env['website.theme'].create({
            'name': THEME_MODULE,
            'converted_theme_addon': THEME_MODULE,
        })
        theme._convert_assets()

        website = self.env.ref("website.default_website")

        website.multi_theme_id = theme

        website._multi_theme_activate()

        # TODO: instead of just making coverage, we could add checking
        # that option_view data are presented in corresponding "auto assets"
