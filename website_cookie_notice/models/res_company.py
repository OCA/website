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

from openerp import _, models, fields


class Company(models.Model):
    _inherit = "res.company"
    cookieAnalytics = fields.Boolean(
        string="Analytics",
        help="Just using a simple analytics package? change this to true")
    cookieMessage = fields.Char(
        string="Message",
        default=lambda self: _(
            'We use cookies on this website, you can '
            '<a href="{{cookiePolicyLink}}" title="read about our '
            'cookies">read about them here</a>. To use the website as '
            'intended please...'),
        translate=True)
    cookiePolicyLink = fields.Char(
        string="Policy link",
        help="If applicable, enter the link to your privacy policy here...",
        default='/page/privacy')
    cookieOverlayEnabled = fields.Boolean(
        string="Overlay enabled",
        help="Don't want a discreet toolbar? Fine, set this to true")
    cookieAnalyticsMessage = fields.Char(
        string="Analytics message",
        default=lambda self: _(
            'We use cookies, just to track visits to our website, we '
            'store no personal details.'),
        translate=True)
    cookieErrorMessage = fields.Char(
        string="Error message",
        default=lambda self: _(
            "We are sorry, this feature places cookies in your browser "
            "and has been disabled. <br/>To continue using this "
            "functionality, please"),
        translate=True)
    cookieDeclineButton = fields.Boolean(
        string="Decline button")
    cookieAcceptButton = fields.Boolean(
        string="Accept button",
        default=True)
    cookieResetButton = fields.Boolean(
        string="Reset button")
    cookieWhatAreTheyLink = fields.Char(
        string="What are they link",
        default="http://www.allaboutcookies.org/")
    cookieAcceptButtonText = fields.Char(
        string="Accept button text",
        default="Accept cookies",
        translate=True)
    cookieDeclineButtonText = fields.Char(
        string="Decline button text",
        default=lambda self: _("Decline cookies"),
        translate=True)
    cookieResetButtonText = fields.Char(
        string="Reset button text",
        default=lambda self: _("Reset cookies for this website"),
        translate=True)
