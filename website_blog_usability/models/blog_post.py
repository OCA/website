# Copyright 2026 - TODAY, Marcel Savegnago <marcel.savegnago@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class BlogPost(models.Model):
    _inherit = "blog.post"

    def action_open_backend_form(self):
        """Open the blog post form view in backend."""
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "blog.post",
            "res_id": self.id,
            "view_mode": "form",
            "target": "current",
        }
