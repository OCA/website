# -*- coding: utf-8 -*-
# Copyright (C) 2015 Agile Business Group sagl (<http://www.agilebg.com>)
# Copyright (C) 2015 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import models, fields
from openerp.tools.translate import _


class Company(models.Model):
    _inherit = "res.company"
    cookieAnalytics = fields.Boolean(
        string="cookieAnalytics",
        help="just using a simple analytics package? change this to true")
    cookieMessage = fields.Char(
        string="cookieMessage",
        default=_('We use cookies on this website, you can '
                  '<a href="{{cookiePolicyLink}}" title="read about our '
                  'cookies">read about them here</a>. To use the website as '
                  'intended please...'),
        translate=True)
    cookiePolicyLink = fields.Char(
        string="cookiePolicyLink",
        help="if applicable, enter the link to your privacy policy here...",
        default='/page/privacy')
    cookieOverlayEnabled = fields.Boolean(
        string="cookieOverlayEnabled",
        help="don't want a discreet toolbar? Fine, set this to true")
    cookieAnalyticsMessage = fields.Char(
        string="cookieAnalyticsMessage",
        default=_('We use cookies, just to track visits to our website, we '
                  'store no personal details.'),
        translate=True)
    cookieErrorMessage = fields.Char(
        string="cookieErrorMessage",
        default=_("We\'re sorry, this feature places cookies in your browser "
                  "and has been disabled. <br>To continue using this "
                  "functionality, please"),
        translate=True)
    cookieDeclineButton = fields.Boolean(
        string="cookieDeclineButton")
    cookieAcceptButton = fields.Boolean(
        string="cookieAcceptButton",
        default=True)
    cookieResetButton = fields.Boolean(
        string="cookieResetButton")
    cookieWhatAreTheyLink = fields.Char(
        string="cookieWhatAreTheyLink",
        default="//wikipedia.org/wiki/HTTP_cookie")
    cookieAcceptButtonText = fields.Char(
        string="cookieAcceptButtonText", default=_("ACCEPT COOKIES"),
        translate=True)
    cookieDeclineButtonText = fields.Char(
        string="cookieDeclineButtonText", default=_("DECLINE COOKIES"),
        translate=True)
    cookieResetButtonText = fields.Char(
        string="cookieResetButtonText",
        default=_("RESET COOKIES FOR THIS WEBSITE"),
        translate=True)
