# -*- coding: utf-8 -*-
# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo.http import request, route
from odoo.addons.website.controllers.main import Website


class WebsiteMultiTheme(Website):

    def _xml_id2key(self, xml_id):
        view = request.env.ref(xml_id, raise_if_not_found=False)
        if view:
            return view.key
        return None

    @route()
    def theme_customize_get(self, xml_ids):
        """Extend in order to replace xml_id to key, because
        view.xml_id is 'website_multi_theme.auto_view_ID_WEBSITE',
        while client works with original IDs.

        """
        res = super(WebsiteMultiTheme, self).theme_customize_get(xml_ids)
        res = [[
            self._xml_id2key(xml_id) or xml_id
            for xml_id in group
        ] for group in res]
        return res
