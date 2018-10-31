from odoo import fields, models
# Copyright 2015 Agile Business Group - Lorenzo Battistini
# Copyright 2016 Tecnativa - Antonio Espinosa
# Copyright 2017 Tecnativa - David Vidal
# Copyright 2018 eslaAmer - Eslam Amer
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


class Config(models.TransientModel):
    _inherit = 'res.config.settings'

    logo = fields.Binary(
        related='website_id.logo',
        readonly=False)
