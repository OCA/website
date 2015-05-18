# -*- encoding: utf-8 -*-
# Python source code encoding : https://www.python.org/dev/peps/pep-0263/
##############################################################################
#
#    OpenERP, Odoo Source Management Solution
#    Copyright (c) 2015 Antiun Ingeniería S.L. (http://www.antiun.com)
#                 Endika Iglesias <endikaig@antiun.com>
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
from openerp import models, fields, api
from datetime import datetime

import logging
from pprint import pformat
_logger = logging.getLogger(__name__)


class HrAnalyticTimesheet(models.Model):
    _inherit = 'hr.analytic.timesheet'

    date = fields.Datetime(
        string='Date', required=True, default=datetime.now())

    @api.multi
    def button_end_work(self):
        end_date = datetime.now()
        _logger.info("button_end_work::"+pformat(self))
        for work in self:
            date = fields.Datetime.from_string(work.date)
            work.unit_amount = (end_date - date).total_seconds() / 3600
        return True
