# -*- coding: utf-8 -*-#
# © 2016 Nicolas Petit <nicolas.petit@vivre-d-internet.fr>
# © 2016, TODAY Odoo S.A
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from lxml import etree
from openerp import tools, fields, models, api


class View(models.Model):

    _inherit = "ir.ui.view"

    version_id = fields.Many2one(
        'website_version_ce.version', ondelete='cascade', string="Version")

    @api.multi
    def write(self, vals):
        if self.env.context is None:
            self.env.context = {}

        version_id = self.env.context.get('version_id')
        if version_id and \
                not self.env.context.get('write_on_view') and \
                'active' not in vals:
            self.env.context = dict(self.env.context, write_on_view=True)
            version = self.env['website_version_ce.version'].browse(version_id)
            website_id = version.website_id.id
            version_view_ids = self.env['ir.ui.view']
            for current in self:
                # check if current is in version
                if current.version_id.id == version_id:
                    version_view_ids += current
                else:
                    new_v = self.search([
                        ('website_id', '=', website_id),
                        ('version_id', '=', version_id),
                        ('key', '=', current.key)
                    ])
                    if new_v:
                        version_view_ids += new_v
                    else:
                        copy_v = current.copy({'version_id': version_id,
                                               'website_id': website_id})
                        version_view_ids += copy_v
            super(View, version_view_ids).write(vals)
        else:
            self.env.context = dict(self.env.context, write_on_view=True)
            super(View, self).write(vals)

    @api.multi
    def publish(self):
        """To delete and replace views which are in the website
        (in fact with website_id)
        """
        self.ensure_one()
        master_record = self.search([
            ('key', '=', self.key),
            ('version_id', '=', False),
            ('website_id', '=', self.website_id.id)
        ])
        if master_record:
            master_record.unlink()
        self.copy({'version_id': None})

    @api.multi
    def action_publish(self):
        """To publish a view in backend"""
        self.publish()

    @api.model
    def get_view_id(self, xml_id):
        if self.env.context and 'website_id' in self.env.context and \
                not isinstance(xml_id, (int, long)):
            domain = [
                ('key', '=', xml_id),
                '|',
                ('website_id', '=', self.env.context['website_id']),
                ('website_id', '=', False)
            ]
            if 'version_id' in self.env.context:
                domain += \
                    ['|', ('version_id', '=', self.env.context['version_id']),
                     ('version_id', '=', False)]
            xml_id = self.search(
                domain, order='website_id,version_id', limit=1).id
        else:
            xml_id = super(View, self).get_view_id(xml_id)
        return xml_id

    @tools.ormcache_context(
        'uid',
        'view_id',
        keys=('lang', 'inherit_branding', 'editable', 'translatable',
              'edit_translations', 'website_id', 'version_id')
    )
    def _read_template(self, cr, uid, view_id, context=None):
        arch = self.read_combined(cr, uid, view_id, fields=['arch'],
                                  context=context)['arch']
        arch_tree = etree.fromstring(arch)

        if 'lang' in context:
            arch_tree = self.translate_qweb(cr, uid, view_id, arch_tree,
                                            context['lang'], context)

        self.distribute_branding(arch_tree)
        root = etree.Element('templates')
        root.append(arch_tree)
        arch = etree.tostring(root, encoding='utf-8', xml_declaration=True)
        return arch

    # To take the right inheriting views
    @api.model
    def get_inheriting_views_arch(self, view_id, model):
        arch = super(View, self).get_inheriting_views_arch(view_id, model)
        vw = self.browse(view_id)
        if not (self.env.context and self.env.context.get('website_id') and
                vw.type == 'qweb'):
            return arch

        right_ids = {}
        priority = {}

        view_arch = dict([(v, a) for a, v in arch])
        keys = self.browse(view_arch.keys())
        # The view to take depends of the context
        context_version_id = self.env.context.get('version_id')
        context_website_id = self.env.context.get('website_id')
        for k in keys:
            if context_version_id:
                # priority:1 take the view which is in the same version
                if k.version_id.id and k.version_id.id == context_version_id:
                    right_ids[k.key] = k.id
                    priority[k.key] = 3
                # priority:2 take the view which is just in the same website
                elif k.version_id.id is False and k.website_id.id and \
                        k.website_id.id == context_website_id:
                    if not priority.get(k.key) or priority.get(k.key) < 3:
                        right_ids[k.key] = k.id
                        priority[k.key] = 2
                # priority:3 take the original view
                elif k.version_id.id is False and k.website_id.id is False:
                    if not priority.get(k.key) or priority.get(k.key) < 2:
                        right_ids[k.key] = k.id
                        priority[k.key] = 1
            else:
                # priority:1 take the view which is just in the same website
                if k.version_id.id is False and \
                        k.website_id.id and \
                        k.website_id.id == context_website_id:
                    right_ids[k.key] = k.id
                    priority[k.key] = 2
                # priority:2 take the original view
                elif k.version_id.id is False and k.website_id.id is False:
                    if not priority.get(k.key) or priority.get(k.key) < 2:
                        right_ids[k.key] = k.id
                        priority[k.key] = 1
        return [x for x in arch if x[1] in right_ids.values()]

    # To active or desactive the right views according to the key
    def toggle(self, cr, uid, ids, context=None):
        """ Switches between enabled and disabled statuses
        """
        for view in self.browse(
                cr, uid, ids, context=dict(context or {}, active_test=False)):
            all_id = self.search(
                cr, uid, [('key', '=', view.key)],
                context=dict(context or {}, active_test=False))
            for v in self.browse(
                    cr, uid, all_id,
                    context=dict(context or {}, active_test=False)):
                v.write({'active': not v.active})

    @api.model
    def customize_template_get(self, key, full=False, bundles=False, **kw):
        result = super(View, self).customize_template_get(
            key, full=full, bundles=bundles, **kw)
        check = []
        res = []
        for data in result:
            if data['name'] not in check:
                check.append(data['name'])
                res.append(data)
        return res
