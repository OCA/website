from odoo import api, fields, models


class Target(models.Model):
    _name = "ab.testing.target"
    _description = "Target"

    def _default_website(self):
        return self.env["website"].search(
            [("company_id", "=", self.env.company.id)], limit=1
        )

    website_id = fields.Many2one(
        comodel_name="website",
        string="Website",
        default=_default_website,
        ondelete="cascade",
    )
    name = fields.Char(required=True)
    active = fields.Boolean(default=True)

    trigger_ids = fields.One2many(
        name="Triggers",
        comodel_name="ab.testing.target.trigger",
        inverse_name="target_id",
    )

    conversion_ids = fields.One2many(
        name="Conversions",
        comodel_name="ab.testing.target.conversion",
        inverse_name="target_id",
    )

    conversion_count = fields.Integer(compute="_compute_conversion_count")

    @api.depends("conversion_ids")
    def _compute_conversion_count(self):
        for target in self:
            target.conversion_count = len(target.conversion_ids)

    def open_conversion_view(self):
        self.ensure_one()
        action = self.env.ref("website_ab_testing.ab_testing_target_conversion_action")
        action = action.read()[0]
        action["domain"] = [("target_id", "=", self.id)]
        action["context"] = "{}"
        return action

    def open_conversion_graph(self):
        self.ensure_one()
        action = self.env.ref("website_ab_testing.ab_testing_target_conversion_action")
        action = action.read()[0]
        action["domain"] = [("target_id", "=", self.id)]
        action["views"] = [(False, "graph")]
        return action
