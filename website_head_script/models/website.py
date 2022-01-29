# -*- coding: utf-8 -*-
import logging
from odoo import models, fields

_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = "website"

    head_script_ids = fields.One2many(
        "website.head.script", "website_id", string="Head scripts")

    def apply_head_scripts(self, main_object):
        res = "\n"
        if not main_object:
            _logger.error("main_object not set, aborting")
            return res
        for script in self.head_script_ids:
            if (
                script.excluded_page_ids and
                main_object.id in script.excluded_page_ids.ids
            ):
                continue
            if (
                script.involved_page_ids and
                main_object.id not in script.involved_page_ids.ids
            ):
                continue
            if script.skip_for_publishers and self.is_publisher():
                continue
            res += script.content
            res += "\n"
        return res


class WebsiteHeadScript(models.Model):
    _name = "website.head.script"
    _order = "sequence, id"

    name = fields.Char("Name", required=True)
    sequence = fields.Integer(default=10)
    website_id = fields.Many2one("website", ondelete="cascade")
    content = fields.Text("Script content", required=True)
    excluded_page_ids = fields.Many2many(
        "ir.ui.view", relation="website_head_script_excluded_page_rel",
        string="Excluded pages",
        help="If set, the script will not be applied to these pages")
    involved_page_ids = fields.Many2many(
        "ir.ui.view", relation="website_head_script_involved_page_rel",
        string="Involved pages",
        help="If set, the script will be applied only to these pages")
    skip_for_publishers = fields.Boolean(
        help="Do not render this script for publisher users")
