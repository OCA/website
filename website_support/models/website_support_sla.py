# -*- coding: utf-8 -*-
import datetime
import logging
_logger = logging.getLogger(__name__)

from odoo.exceptions import UserError
from odoo import api, fields, models

class WebsiteSupportSLA(models.Model):

    _name = "website.support.sla"

    name = fields.Char(string="Name", translate=True)
    description = fields.Text(string="Description", translate=True)
    rule_ids = fields.One2many('website.support.sla.rule', 'vsa_id', string="Rules", help="If a ticket matches mutiple rules then the one with the lowest response time is used")
    alert_ids = fields.One2many('website.support.sla.alert', 'vsa_id', string="Email Alerts")

class WebsiteSupportSLARule(models.Model):

    _name = "website.support.sla.rule"
    _order = "response_time asc"

    vsa_id = fields.Many2one('website.support.sla', string="SLA")
    name = fields.Char(string="Name", required="True")
    condition_ids = fields.One2many('website.support.sla.rule.condition', 'wssr_id', string="Conditions", help="All conditions have to be fulfilled for the rule to apply, e.g. priority='High' AND category='Tech Support'", required="True")
    response_time = fields.Float(string="Response Time", required="True", help="If the support ticket matches the conditions then it has to be completed within this amount of time, e.g. high priority tech support ticket within 1 hour")
    countdown_condition = fields.Selection([('business_only','Business Only'), ('24_hour','24 Hours')], default="24_hour", required="True", help="During what time do we start counting down the SLA timer")

class WebsiteSupportSLARuleCondition(models.Model):

    _name = "website.support.sla.rule.condition"

    wssr_id = fields.Many2one('website.support.sla.rule', string="SLA Rule")
    type = fields.Selection([('category','Category'), ('subcategory','Sub Category'), ('priority','Priority')], string="Type", required="True")
    display_value = fields.Char(string="Display Value", compute="_compute_display_value")
    category_id = fields.Many2one('website.support.ticket.category', string="Category")
    subcategory_id = fields.Many2one('website.support.ticket.subcategory', string="Sub Category")
    priority_id = fields.Many2one('website.support.ticket.priority', string="Priority")

    @api.one
    @api.depends('type','category_id','subcategory_id','priority_id')
    def _compute_display_value(self):
        if self.type == "category":
            self.display_value = self.category_id.name
        elif self.type == "subcategory":
            self.display_value = self.subcategory_id.name
        elif self.type == "priority":
            self.display_value = self.priority_id.name
        
class WebsiteSupportSLAAlert(models.Model):

    _name = "website.support.sla.alert"
    _order = "alert_time desc"

    vsa_id = fields.Many2one('website.support.sla', string="SLA")
    alert_time = fields.Float(string="Alert Time", help="Number of hours before or after SLA expiry to send alert")
    type = fields.Selection([('email','Email')], default="email", string="Type")