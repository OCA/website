# -*- coding: utf-8 -*-
# © 2016 Antiun Ingenieria S.L. - Antonio Espinosa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, api, _
from openerp.exceptions import ValidationError


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.multi
    @api.constrains('ref', 'is_company', 'company_id')
    def _check_ref(self):
        for partner in self:
            mode = partner.company_id.partner_ref_unique
            if (partner.ref and (
                    mode == 'all' or
                    (mode == 'companies' and partner.is_company))):
                domain = [
                    ('id', '!=', partner.id),
                    ('ref', '=', partner.ref),
                    ('customer', '=', True),
                ]
                if mode == 'companies':
                    domain.append(('is_company', '=', True))
                other = self.search(domain)
                if other:
                    raise ValidationError(
                        _("This reference is equal to partner '%s'") %
                        other[0].display_name)
