from odoo import models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    def set_values(self):
        res = super(ResConfigSettings, self).set_values()
        IrDefault = self.env["ir.default"].sudo()
        if self.show_availability:
            value = self.available_threshold
        else:
            value = None

        IrDefault.set("product.template", "available_threshold", value)
        return res
