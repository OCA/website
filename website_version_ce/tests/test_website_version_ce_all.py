# -*- coding: utf-8 -*-#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from . import test_website_version_ce_base as test_wvb


class TestWebsiteVersionAll(test_wvb.TestWebsiteVersionBase):

    def test_copy_version(self):
        """ Testing version_copy"""
        view_0_0_0_0_id = self.view_0_0_0_0.id
        version_id = self.version.id
        website_id = self.website.id

        copy_version = self.orm_version.create(
            {'name': 'copy_version_0_0_0_0', 'website_id': website_id})
        self.version.copy_version(copy_version.id)
        view_copy_version = copy_version.view_ids[0]
        self.env.context = {'version_id': version_id}
        view_0_0_0_0 = self.orm_view.browse(view_0_0_0_0_id)
        test_error_str = 'website_version_ce: copy_version: ' + \
                         'website_version_ce must have in ' + \
                         'snpashot_copy the same views then in version_0_0_0_0'
        self.assertEqual(view_copy_version.arch, view_0_0_0_0.arch,
                         test_error_str)
