# -*- coding: utf-8 -*-
# Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.http import request
from odoo.addons.website.controllers import main


class Website(main.Website):
    # TODO Remove when merged upstream
    # HACK https://github.com/odoo/odoo/pull/17970
    def get_view_ids(self, xml_ids):
        if not request.website_enabled:
            return super(Website, self).get_view_ids(xml_ids)
        View = request.env["ir.ui.view"].with_context(active_test=False)
        result = []
        for xmlid in xml_ids:
            found = View.search([
                ("website_id", "=", request.website.id),
                ("key", "=", xmlid),
            ]).ids
            if not found:
                found = super(Website, self).get_view_ids([xmlid])
            result += found
        return result
