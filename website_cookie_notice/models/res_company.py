# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Agile Business Group sagl (<http://www.agilebg.com>)
#    Copyright (C) 2015 Lorenzo Battistini <lorenzo.battistini@agilebg.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields


class Company(models.Model):
    _inherit = "res.company"
    cookieAnalytics = fields.Boolean(
        string="cookieAnalytics",
        help="just using a simple analytics package? change this to true")
    cookieMessage = fields.Char(
        string="cookieMessage",
        default='We use cookies on this website, you can '
                '<a href="{{cookiePolicyLink}}" title="read about our '
                'cookies">read about them here</a>. To use the website as '
                'intended please...',
        translate=True)
    cookiePolicyLink = fields.Char(
        string="cookiePolicyLink",
        help="if applicable, enter the link to your privacy policy here...",
        default='/privacy-policy')
    cookieOverlayEnabled = fields.Boolean(
        string="cookieOverlayEnabled",
        help="don't want a discreet toolbar? Fine, set this to true")
    cookieAnalyticsMessage = fields.Char(
        string="cookieAnalyticsMessage",
        default='We use cookies, just to track visits to our website, we store'
                ' no personal details.',
        translate=True)
    cookieErrorMessage = fields.Char(
        string="cookieErrorMessage",
        default="We\'re sorry, this feature places cookies in your browser and"
                " has been disabled. <br>To continue using this functionality,"
                " please",
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
        default="http://www.allaboutcookies.org/")
