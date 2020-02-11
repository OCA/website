# -*- coding: utf-8 -*-
# Copyright 2019 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class IrUiView(models.Model):
    _inherit = 'ir.ui.view'

    page_permission_ids = fields.Many2many('res.groups')

    # The website publisher must always be in the permissions group.
    # Otherwise she might create/clone a page see can not see/edit herself.
    @api.model
    def create(self, vals):
        result = super(IrUiView, self).create(vals)
        result.suspend_security()._ensure_web_editor()
        return result

    @api.multi
    def write(self, vals):
        result = super(IrUiView, self).write(vals)
        self.suspend_security()._ensure_web_editor()
        return result

    @api.multi
    def _ensure_web_editor(self):
        editor = self.env.ref('website.group_website_designer')
        for this in self:
            if (
                    this.page_permission_ids and
                    editor not in this.page_permission_ids
            ):
                super(IrUiView, this).write({
                    'page_permission_ids': [(4, editor.id, False)],
                })
