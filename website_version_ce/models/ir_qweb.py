# -*- coding: utf-8 -*-#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

"""
Website-context rendering needs to add some metadata to rendered fields,
as well as render a few fields differently.

Also, adds methods to convert values back to odoo models.
"""

from odoo import api, models


class IrQweb(models.AbstractModel):
    """ QWeb object for rendering stuff in the website context
    """
    _inherit = 'ir.qweb'

    @api.model
    def render(self, id_or_xml_id, qwebcontext=None, loader=None):
        website_id = self.env.context.get('website_id')
        orm_exp_ver = self.env["website_version_ce.experiment.version"]
        if website_id:
            if 'experiment_id' in self._context:
                # Search for a corresponding version
                exp_ver_id = orm_exp_ver.search([
                    ('version_id.view_ids.key', '=', id_or_xml_id),
                    ('experiment_id.state', '=', 'running'),
                    ('experiment_id.website_id.id', '=', website_id)
                ])

                if exp_ver_id:
                    # Found version, check overlap
                    exp_version = orm_exp_ver.browse([exp_ver_id[0]])
                    exp = exp_version.experiment_id
                    # Avoid "google_id is unique" error at db reinitialization
                    version_id = self._context.get('website_version_ce_experiment'
                                             ).get(str(exp.google_id))
                    if version_id:
                        context['version_id'] = int(version_id)

            if isinstance(id_or_xml_id, (int, long)):
                id_or_xml_id = self.pool["ir.ui.view"].browse(
                    id_or_xml_id).key

            domain = [('key', '=', id_or_xml_id), '|',
                      ('website_id', '=', website_id),
                      ('website_id', '=', False)]
            version_id = self._context.get('version_id')
            domain += version_id \
                and ['|', ('version_id', '=', False),
                     ('version_id', '=', version_id)] or \
                    [('version_id', '=', False)]

            id_or_xml_id = self.pool["ir.ui.view"].search(
                domain, order='website_id, version_id',
                limit=1)[0]

        return super(IrQweb, self).render(
            id_or_xml_id, qwebcontext, loader=loader,
        )
