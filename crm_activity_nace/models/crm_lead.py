# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import models, fields


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    main_nace = fields.Many2one(comodel_name='res.partner.nace',
                                string="Main activity")
    secondary_naces = fields.Many2many(comodel_name='res.partner.nace',
                                       string="Other activities")

    def _lead_create_contact(self, cr, uid, lead, name, is_company,
                             parent_id=False, context=None):
        """Propagate NACE activity to created partner.
        """
        partner_id = super(CrmLead, self)._lead_create_contact(
            cr, uid, lead, name, is_company, parent_id=parent_id,
            context=context)
        data = {
            'main_nace': lead.main_nace.id,
            'secondary_naces': [(4, x.id) for x in lead.secondary_naces]}
        self.pool['res.partner'].write(cr, uid, partner_id, data,
                                       context=context)
        return partner_id
