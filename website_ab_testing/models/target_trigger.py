from odoo import _, api, fields, models


class TargetTrigger(models.Model):
    _name = "ab.testing.target.trigger"
    _description = "Goal Trigger"

    name = fields.Char(compute="_compute_name",)

    target_id = fields.Many2one(
        string="Target",
        comodel_name="ab.testing.target",
        required=True,
        ondelete="cascade",
    )

    on = fields.Selection(string="On", selection=[("url_visit", "Url Visit")])

    url = fields.Char(default="/")

    @api.depends("on", "url")
    def _compute_name(self):
        for trigger in self:
            name = ""
            if trigger.on == "url_visit":
                name = _("When visitors visit '%s'") % trigger.url
            trigger.name = name

    def create_conversion(self, date=None, variants=None):
        if variants is None:
            variants = self.env["ir.ui.view"].get_active_variants()
        if not date:
            date = fields.Datetime.now()
        for trigger in self:
            self.env["ab.testing.target.conversion"].create(
                {
                    "date": date,
                    "view_ids": [(4, v.id) for v in variants],
                    "trigger_id": trigger.id,
                }
            )
