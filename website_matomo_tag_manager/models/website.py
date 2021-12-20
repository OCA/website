# Copyright 2020 Onestein (<https://www.onestein.nl>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Website(models.Model):
    _inherit = 'website'

    matomo_tag_manager = fields.Boolean(string='Matomo Tag Manager')
    matomo_host_name = fields.Char("Matomo Host")
    matomo_container_ref = fields.Char("Matomo Container ID")

    def _matomo_tag_manager_script(self):
        self.ensure_one()
        res = '''
            var _mtm = window._mtm = window._mtm || [];
            _mtm.push({'mtm.startTime': (new Date().getTime()), 'event': 'mtm.Start'});
            var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')
            [0];
            g.type='text/javascript'; g.async=true;
            g.src='https://%s/js/container_%s.js';
            s.parentNode.insertBefore(g,s);
        ''' % (self.matomo_host_name, self.matomo_container_ref)
        return res
