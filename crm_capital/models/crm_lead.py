# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    capital_country = fields.Many2one(
        'res.country', string="Capital country",
        help="Country of origin of the capital of this company")
    capital_registered = fields.Integer(string="Capital registered")
    turnover_range = fields.Many2one(comodel_name='crm.turnover_range')
    turnover_number = fields.Integer()

    def _lead_create_contact(self, cr, uid, lead, name, is_company,
                             parent_id=False, context=None):
        """Propagate capital_country and capital_registered to created partner.
        """
        partner_id = super(CrmLead, self)._lead_create_contact(
            cr, uid, lead, name, is_company, parent_id=parent_id,
            context=context)
        self.pool['res.partner'].write(
            cr, uid, partner_id, {
                'capital_country': lead.capital_country.id,
                'capital_registered': lead.capital_registered,
                'turnover_range': lead.turnover_range.id,
                'turnover_number': lead.turnover_number,
            }, context=context)
        return partner_id
