# -*- coding: utf-8 -*-
##############################################################################
#
# Authors: Odoo S.A., Nicolas Petit (Clouder)
# Copyright 2016, TODAY Odoo S.A. Clouder SASU
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

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

    def render(self, cr, uid, id_or_xml_id, qwebcontext=None, loader=None, context=None):
        if context is None:
            context = {}
        website_id = context.get('website_id')
        if website_id:
            if 'experiment_id' in context:
                # Is there a version which have the view.key == id_or_xml_id and which is in a running experiment?
                exp_ver_id = self.pool["website_version.experiment.version"].search(cr, uid, [
                    ('version_id.view_ids.key', '=', id_or_xml_id),
                    ('experiment_id.state', '=', 'running'),
                    ('experiment_id.website_id.id', '=', website_id)
                ], context=context)

                if exp_ver_id:
                    # If yes take the first because there is no overlap between running experiments.
                    exp_version = self.pool["website_version.experiment.version"].browse(cr, uid, [exp_ver_id[0]],
                                                                                         context=context)
                    exp = exp_version.experiment_id
                    # Setting google_id as key in the dict to avoid "google_id is unique" error at db reinitialization
                    version_id = context.get('website_version_experiment').get(str(exp.google_id))
                    if version_id:
                        context['version_id'] = int(version_id)

            if isinstance(id_or_xml_id, (int, long)):
                id_or_xml_id = self.pool["ir.ui.view"].browse(cr, uid, id_or_xml_id, context=context).key

            domain = [('key', '=', id_or_xml_id), '|', ('website_id', '=', website_id), ('website_id', '=', False)]
            version_id = context.get('version_id')
            domain += version_id \
                and ['|', ('version_id', '=', False), ('version_id', '=', version_id)] \
                or [('version_id', '=', False)]

            id_or_xml_id = self.pool["ir.ui.view"].search(cr, uid, domain, order='website_id, version_id', limit=1,
                                                          context=context)[0]

        return super(QWeb, self).render(cr, uid, id_or_xml_id, qwebcontext, loader=loader, context=context)
