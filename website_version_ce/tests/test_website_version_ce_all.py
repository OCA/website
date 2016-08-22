# -*- coding: utf-8 -*-#
# © 2016 Nicolas Petit <nicolas.petit@vivre-d-internet.fr>
# © 2016, TODAY Odoo S.A
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from . import test_website_version_ce_base


class TestWebsiteVersionAll(test_website_version_ce_base.TestWebsiteVersionBase):

    def test_copy_version(self):
        """ Testing version_copy"""
        view_0_0_0_0_id, version_id, website_id = self.view_0_0_0_0.id, self.version.id, self.website.id

        copy_version = self.website_version_ce_version.create({'name': 'copy_version_0_0_0_0', 'website_id': website_id})
        self.version.copy_version(copy_version.id)
        view_copy_version = copy_version.view_ids[0]
        self.env.context = {'version_id': version_id}
        view_0_0_0_0 = self.ir_ui_view.browse(view_0_0_0_0_id)
        test_error_str = 'website_version_ce: copy_version: website_version_ce must have ' + \
            'in snpashot_copy the same views then in version_0_0_0_0'
        self.assertEqual(view_copy_version.arch, view_0_0_0_0.arch, test_error_str)
