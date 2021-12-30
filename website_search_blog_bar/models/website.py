# Copyright 2021 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class Website(models.Model):
    _inherit = "website"

    blog_search_title = fields.Boolean(string="Search by Title")
    blog_search_content = fields.Boolean(string="Search by Content")
    blog_search_manual_teaser = fields.Boolean(string="Search by Manual Teaser")
    show_search_bar = fields.Boolean(
        string="Show Search Bar", compute="_compute_show_search_bar", store=True
    )

    @api.depends(
        "blog_search_title", "blog_search_content", "blog_search_manual_teaser"
    )
    def _compute_show_search_bar(self):
        for sel in self:
            sel.show_search_bar = (
                sel.blog_search_title
                or sel.blog_search_content
                or sel.blog_search_manual_teaser
            )
