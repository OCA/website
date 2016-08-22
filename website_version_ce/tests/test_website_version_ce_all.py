# -*- coding: utf-8 -*-
##############################################################################
#
# Authors: Odoo S.A., Nicolas Petit (Clouder)
# Copyright 2016, TODAY Odoo S.A. Clouder SASU
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from . import test_website_version_base


class TestWebsiteVersionAll(test_website_version_base.TestWebsiteVersionBase):

    def test_copy_version(self):
        """ Testing version_copy"""
        view_0_0_0_0_id, version_id, website_id = self.view_0_0_0_0.id, self.version.id, self.website.id

        copy_version = self.website_version_version.create({'name': 'copy_version_0_0_0_0', 'website_id': website_id})
        self.version.copy_version(copy_version.id)
        view_copy_version = copy_version.view_ids[0]
        self.env.context = {'version_id': version_id}
        view_0_0_0_0 = self.ir_ui_view.browse(view_0_0_0_0_id)
        test_error_str = 'website_version: copy_version: website_version must have ' + \
            'in snpashot_copy the same views then in version_0_0_0_0'
        self.assertEqual(view_copy_version.arch, view_0_0_0_0.arch, test_error_str)
