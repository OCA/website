# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields


class CrmHeading(models.Model):
    _name = 'crm.heading'
    _description = "Heading"

    name = fields.Char(required=True, translate=True)
