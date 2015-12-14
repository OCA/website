# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sector = fields.Many2one(comodel_name='crm.sector')
    secondary_sector_ids = fields.Many2many(comodel_name='crm.sector',
                                            string="Other sectors")
