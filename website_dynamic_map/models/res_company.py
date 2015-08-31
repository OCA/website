# -*- coding: utf-8 -*-
# See README.rst file on addon root folder for license details

from openerp import models, fields


class ResCompany(models.Model):
    _inherit = 'res.company'

    google_map_marker = fields.Boolean(
        string='Show marker on Google map',
        related="partner_id.google_map_marker")
    google_map_type = fields.Selection(
        [('static', 'Static map'),
         ('dynamic', 'Dynamic map')],
        string="Google map type",
        related="partner_id.google_map_type")
    google_map_zoom = fields.Integer(
        string="Google map zoom",
        related="partner_id.google_map_zoom")
    google_map_lat = fields.Float(
        string="Google map latitude",
        related="partner_id.google_map_lat")
    google_map_lon = fields.Float(
        string="Google map longitude",
        related="partner_id.google_map_lon")
