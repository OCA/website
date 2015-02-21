# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    function = fields.Char(string="Detailed job position")
    job_position = fields.Many2one(comodel_name='crm.job_position',
                                   string="Job position")
