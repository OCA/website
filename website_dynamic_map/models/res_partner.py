# -*- coding: utf-8 -*-
# See README.rst file on addon root folder for license details

from openerp import models, fields
from openerp.addons.website.models.website import urlplus
from openerp.tools.float_utils import float_is_zero


class ResPartner(models.Model):
    _inherit = 'res.partner'

    google_map_marker = fields.Boolean(
        string='Show marker on Google Maps map', default=True)
    google_map_type = fields.Selection(
        [('static', 'Static map'),
         ('dynamic', 'Dynamic map')],
        string="", default='static')
    google_map_zoom = fields.Integer(string="Google Maps map zoom", default=8)
    google_map_lat = fields.Float(
        string="Google Maps map latitude", digits=(3, 8))
    google_map_lon = fields.Float(
        string="Google Maps map longitude", digits=(3, 8))

    def google_map_img(self, cr, uid, ids, zoom=8, width=298, height=298,
                       context=None):
        super(ResPartner, self).google_map_img(
            cr, uid, ids, zoom=zoom, width=width, height=height,
            context=context)
        partner = self.browse(cr, uid, ids[0], context=context)
        if (not float_is_zero(partner.google_map_lat, precision_digits=8) and
                not float_is_zero(partner.google_map_lon, precision_digits=8)):
            position = '%3.8f, %3.8f' % (
                partner.google_map_lat,
                partner.google_map_lon)
        else:
            position = '%s, %s %s, %s' % (
                partner.street or '',
                partner.city or '',
                partner.zip or '',
                partner.country_id and
                partner.country_id.name_get()[0][1] or ''),

        if partner.google_map_type == 'static':
            params = {
                'center': position,
                'size': "%sx%s" % (height, width),
                'zoom': zoom,
                'sensor': 'false',
            }
            if partner.google_map_marker:
                params['markers'] = params['center']
            url_base = '//maps.googleapis.com/maps/api/staticmap'
        else:
            params = {
                'q': '%s %s' % (partner.name, position),
                'ie': 'UTF8',
                'output': 'embed',
                'z': zoom,
            }
            url_base = '//maps.google.com/maps'
        return urlplus(url_base, params)
