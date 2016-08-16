# -*- coding: utf-8 -*-#
# © 2016 Nicolas Petit <nicolas.petit@vivre-d-internet.fr>
# © 2016, TODAY Odoo S.A
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

"""
Website-context rendering needs to add some metadata to rendered fields,
as well as render a few fields differently.

Also, adds methods to convert values back to openerp models.
"""

from openerp import models


class QWeb(models.AbstractModel):
    """ QWeb object for rendering stuff in the website context
    """
    _inherit = 'ir.qweb'

    def render(self, cr, uid, id_or_xml_id, qwebcontext=None, loader=None,
               context=None):
        if context is None:
            context = {}
        website_id = context.get('website_id')
        orm_exp_ver = self.pool.get["website_version_ce.experiment.version"]
        if website_id:
            if 'experiment_id' in context:
                # Search for a corresponding version
                exp_ver_id = orm_exp_ver.search(cr, uid, [
                    ('version_id.view_ids.key', '=', id_or_xml_id),
                    ('experiment_id.state', '=', 'running'),
                    ('experiment_id.website_id.id', '=', website_id)
                ], context=context)

                if exp_ver_id:
                    # Found version, check overlap
                    exp_version = orm_exp_ver.browse(cr, uid, [exp_ver_id[0]],
                                                     context=context)
                    exp = exp_version.experiment_id
                    # Avoid "google_id is unique" error at db reinitialization
                    version_id = context.get('website_version_ce_experiment'
                                             ).get(str(exp.google_id))
                    if version_id:
                        context['version_id'] = int(version_id)

            if isinstance(id_or_xml_id, (int, long)):
                id_or_xml_id = self.pool["ir.ui.view"].browse(
                    cr, uid, id_or_xml_id, context=context).key

            domain = [('key', '=', id_or_xml_id), '|',
                      ('website_id', '=', website_id),
                      ('website_id', '=', False)]
            version_id = context.get('version_id')
            domain += version_id \
                and ['|', ('version_id', '=', False),
                     ('version_id', '=', version_id)] or \
                    [('version_id', '=', False)]

            id_or_xml_id = self.pool["ir.ui.view"].search(
                cr, uid, domain, order='website_id, version_id',
                limit=1, context=context)[0]

        return super(QWeb, self).render(
            cr, uid, id_or_xml_id, qwebcontext, loader=loader, context=context)
