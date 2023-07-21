import re
import werkzeug

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class WebsiteRewrite(models.Model):
    _inherit = 'website.rewrite'
    
    absolute_url = fields.Boolean("Is absolute url")

    @api.constrains('url_to', 'url_from', 'redirect_type')
    def _check_url_to(self):
        for rewrite in self:
            if rewrite.redirect_type in ['301', '302', '308']:
                if not rewrite.url_to:
                    raise ValidationError(_('"URL to" can not be empty.'))
                elif not rewrite.absolute_url and not rewrite.url_to.startswith('/'):
                    raise ValidationError(_('"URL to" must start with a leading slash.'))
                for param in re.findall('/<.*?>', rewrite.url_from):
                    if param not in rewrite.url_to:
                        raise ValidationError(_('"URL to" must contain parameter %s used in "URL from".') % param)
                for param in re.findall('/<.*?>', rewrite.url_to):
                    if param not in rewrite.url_from:
                        raise ValidationError(_('"URL to" cannot contain parameter %s which is not used in "URL from".') % param)
                try:
                    converters = self.env['ir.http']._get_converters()
                    routing_map = werkzeug.routing.Map(strict_slashes=False, converters=converters)
                    if not rewrite.absolute_url:
                        rule = werkzeug.routing.Rule(rewrite.url_to)
                        routing_map.add(rule)
                    else:
                        routing_map.bind(rewrite.url_to)
                except ValueError as e:
                    raise ValidationError(_('"URL to" is invalid: %s') % e)