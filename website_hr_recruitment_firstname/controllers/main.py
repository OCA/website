# -*- coding: utf-8 -*-
#
##############################################################################
#
#    Authors: Adrien Peiffer
#    Copyright (c) 2015 Acsone SA/NV (http://www.acsone.eu)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
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

from openerp.addons.website_hr_recruitment.controllers.main import\
    website_hr_recruitment


class WebsiteHrRecruitment(website_hr_recruitment):

    def _get_applicant_char_fields(self):
        res = super(WebsiteHrRecruitment, self)._get_applicant_char_fields()
        fields_list = set(['partner_firstname'])
        res = set(res)
        res |= fields_list
        return list(res)
