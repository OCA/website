# -*- coding: utf-8 -*-
from openerp import fields, models


class WebsiteConfigSettings(models.TransientModel):

    _inherit = "website.config.settings"

    website_slide_google_app_key = fields.Char(string='Google Doc Key')

    def get_default_website_slide_google_app_key(
            self, cr, uid, fields, context=None):
        icp = self.pool.get('ir.config_parameter')
        return {
            'website_slide_google_app_key': icp.get_param(
                cr, uid, 'website_slides.google_app_key', '')
        }

    def set_website_slide_google_app_key(self, cr, uid, ids, context=None):
        config = self.browse(cr, uid, ids[0], context=context)
        icp = self.pool.get('ir.config_parameter')
        icp.set_param(cr, uid, 'website_slides.google_app_key',
                      config.website_slide_google_app_key or '')
