from odoo import api, fields, models


class TargetConversion(models.Model):
    _name = "ab.testing.target.conversion"
    _description = "Conversion"

    date = fields.Datetime()
    target_id = fields.Many2one(
        name="Target",
        comodel_name="ab.testing.target",
        compute="_compute_target_id",
        store=True,
    )

    trigger_id = fields.Many2one(
        name="Trigger", comodel_name="ab.testing.target.trigger", ondelete="cascade"
    )

    view_ids = fields.Many2many(name="Active Variants", comodel_name="ir.ui.view")

    view_names = fields.Char(
        name="Active Variant Names", compute="_compute_view_names", store=True
    )

    @api.depends("trigger_id", "trigger_id.target_id")
    def _compute_target_id(self):
        for conversion in self:
            conversion.target_id = (
                conversion.trigger_id and conversion.trigger_id.target_id
            )

    @api.depends("view_ids", "view_ids.name")
    def _compute_view_names(self):
        for conversion in self:
            conversion.view_names = ", ".join(
                conversion.view_ids.sorted(key=lambda l: l.id).mapped("name")
            )
