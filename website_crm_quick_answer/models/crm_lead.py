# -*- coding: utf-8 -*-
# Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    # TODO Remove in v11
    def website_form_input_filter(self, request, values):
        """Set the logical default ``team_id``."""
        values.setdefault(
            "team_id",
            self.env["ir.model.data"].xmlid_to_res_id(
                "website.salesteam_website_sales", False))
        return super(CrmLead, self).website_form_input_filter(request, values)
