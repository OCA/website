# -*- coding: utf-8 -*-
import unicodedata
import re

from odoo import api, fields, models
from odoo.http import request
from odoo.tools import html_escape as escape, ustr, image_resize_and_sharpen, image_save_for_web

from odoo.addons.http_routing.models.ir_http import slug

class WebsiteSupportHelpGroup(models.Model):

    _name = "website.support.help.group"
    _order = "sequence asc"

    name = fields.Char(string="Name", translate=True)
    image = fields.Binary(string="Image")
    sequence = fields.Integer(string="Sequence")
    website_published = fields.Boolean(string="Published", default="True")
    page_ids = fields.One2many('website.support.help.page','group_id',string="Pages")
    page_count = fields.Integer(string="Number of Pages", compute='_page_count')
    group_ids = fields.Many2many('res.groups', string="Privilege Groups")

    @api.one
    @api.depends('page_ids')
    def _page_count(self):
        """Amount of help pages in a help group"""
        self.page_count = self.env['website.support.help.page'].search_count([('group_id','=',self.id)])

    @api.model
    def create(self, values):
        sequence=self.env['ir.sequence'].next_by_code('website.support.help.group')
        values['sequence']=sequence
        return super(WebsiteSupportHelpGroup, self).create(values)

class WebsiteSupportHelpPage(models.Model):

    _name = "website.support.help.page"
    _order = "sequence asc"

    name = fields.Char(string='Page Name', translate=True)
    sequence = fields.Integer(string="Sequence")
    website_published = fields.Boolean(string="Published", default="True")
    url = fields.Char(string="Page URL")
    group_id = fields.Many2one('website.support.help.group', string="Group")
    content = fields.Html(sanatize=False, string='Content', translate=True)
    feedback_ids = fields.One2many('website.support.help.page.feedback', 'hp_id', string="Feedback")
    feedback_average = fields.Float(string="Feedback Average Rating", compute="_compute_feedback_average")
    feedback_count = fields.Integer(string="Feedback Count", compute="_compute_feedback_count")

    @api.one
    @api.depends('feedback_ids')
    def _compute_feedback_count(self):
        self.feedback_count = len(self.feedback_ids)

    @api.one
    @api.depends('feedback_ids')
    def _compute_feedback_average(self):
        average = 0

        for fb in self.feedback_ids:
            average += fb.feedback_rating

        if len(self.feedback_ids) > 0:
            self.feedback_average = average / len(self.feedback_ids)
        else:
           self.feedback_average = 0

    @api.model
    def create(self, values):
        sequence=self.env['ir.sequence'].next_by_code('website.support.help.page')
        values['sequence']=sequence
        return super(WebsiteSupportHelpPage, self).create(values)


class WebsiteSupportHelpPageFeedback(models.Model):

    _name = "website.support.help.page.feedback"

    hp_id = fields.Many2one('website.support.help.page', string="Help Page")
    feedback_rating = fields.Integer(string="Feedback Rating")
    feedback_text = fields.Text(string="Feedback Text")

def slugify(s, max_length=None):
    """ Transform a string to a slug that can be used in a url path.

    This method will first try to do the job with python-slugify if present.
    Otherwise it will process string by stripping leading and ending spaces,
    converting unicode chars to ascii, lowering all chars and replacing spaces
    and underscore with hyphen "-".

    :param s: str
    :param max_length: int
    :rtype: str
    """
    s = ustr(s)
    uni = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode('ascii')
    slug = re.sub('[\W_]', ' ', uni).strip().lower()
    slug = re.sub('[-\s]+', '-', slug)

    return slug[:max_length]