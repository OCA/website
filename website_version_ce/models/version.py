# -*- coding: utf-8 -*-#
# © 2016 Nicolas Petit <nicolas.petit@vivre-d-internet.fr>
# © 2016, TODAY Odoo S.A
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import fields, models, api
from openerp.exceptions import Warning
from openerp.http import request
from openerp.tools.translate import _


class Version(models.Model):
    """ A version is a set of qweb views which differs from the qweb views in
    production for the website.
    """

    _name = "website_version_ce.version"

    name = fields.Char(string="Title", required=True)
    view_ids = fields.One2many('ir.ui.view', 'version_id', string="View",
                               copy=True)
    website_id = fields.Many2one('website', ondelete='cascade',
                                 string="Website")
    create_date = fields.Datetime('Create Date')

    _sql_constraints = [
        ('name_uniq', 'unique(name, website_id)',
         _('You cannot have multiple versions with the same name ' +
           'in the same domain!')),
    ]

    @api.multi
    def unlink(self):
        for version_id in self.ids:
            result = self.env['website_version_ce.experiment'].search([
                '|',
                ('state', '=', 'running'),
                ('state', '=', 'paused'),
                ('experiment_version_ids.version_id', '=', version_id)
            ])
            if result:
                raise Warning(_("You cannot delete a version which is " +
                                "in a running or paused experiment."))
        # To avoid problem when we delete versions in Backend
        if request:
            request.session['version_id'] = 0
        return super(Version, self).unlink()

    @api.multi
    def action_publish(self):
        for version in self:
            version.view_ids.publish()

    @api.one
    def publish_version(self, save_master, copy_master_name):
        del_l = self.env['ir.ui.view']
        copy_l = self.env['ir.ui.view']
        ir_ui_view = self.env['ir.ui.view']
        for view in self.view_ids:
            master_id = ir_ui_view .search([
                ('key', '=', view.key),
                ('version_id', '=', False),
                ('website_id', '=', view.website_id.id)
            ])
            if master_id:
                del_l += master_id
                copy_l += master_id
            else:
                # Copy view that could be shared
                master_id = ir_ui_view.search([
                    ('key', '=', view.key),
                    ('version_id', '=', False),
                    ('website_id', '=', False)
                ])
                copy_l += master_id
        if copy_l:
            if save_master:
                check_id = self.search([
                    ('name', '=', copy_master_name),
                    ('website_id', '=', self.website_id.id)])
                if check_id:
                    check_id.unlink()
                copy_version_id = self.create(
                    {'name': copy_master_name,
                     'website_id': self.website_id.id})
                copy_l.copy({'version_id': copy_version_id.id,
                             'website_id': self.website_id.id})
            del_l.unlink()
        # All the views in the version published are copied without version_id
        for view in self.view_ids:
            view.copy({'version_id': None})
        return self.name

    # To make a version of a version
    @api.one
    def copy_version(self, new_version_id):
        for view in self.view_ids:
            view.copy({'version_id': new_version_id})
