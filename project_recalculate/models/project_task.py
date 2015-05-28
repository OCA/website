# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright :
#        (c) 2014 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
#                 Endika Iglesias <endikaig@antiun.com>
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

from openerp import models, fields, api
from datetime import timedelta


class ProjectTask(models.Model):
    _inherit = 'project.task'

    from_days = fields.Integer(
        string='From days',
        help='Anticipation days from date begin or date end', default=0)
    estimated_days = fields.Integer(
        string='Estimated days', help='Estimated days to end', default=1)

    def count_days_without_weekend(self, date_start, date_end):
        all_days = (date_start + timedelta(x + 1)
                    for x in xrange((date_end - date_start).days))
        return sum(1 for day in all_days if day.weekday() < 5)

    def correct_days_to_workable(self, date, increment=True):
        while date.weekday() >= 5:
            if increment:
                date += timedelta(days=1)
            else:
                date -= timedelta(days=1)
        return date

    def calculate_date_without_weekend(self, date_start, days, increment=True):
        count_days = 0
        date = 0
        if increment:
            count_days = self.count_days_without_weekend(
                date_start, date_start + timedelta(days=days))
            date = date_start + timedelta(days=(days + (days - count_days)))
        else:
            count_days = self.count_days_without_weekend(
                date_start - timedelta(days=days), date_start)
            date = date_start - timedelta(days=(days + (days - count_days)))
        date = self.correct_days_to_workable(date, increment)
        return date

    @api.one
    @api.onchange('date_start')
    def on_change_date_start(self):
        if self.date_start is not False and self.date_end is not False:
            date_start = fields.Datetime.from_string(self.date_start)
            date_end = fields.Datetime.from_string(self.date_end)
            self.estimated_days = self.count_days_without_weekend(
                date_start, date_end)
            if self.project_id.calculation_type == 'date_begin':
                date_start = fields.Datetime.from_string(
                    self.project_id.date_start)
                date_end = fields.Datetime.from_string(self.date_start)
            self.from_days = self.count_days_without_weekend(
                date_start, date_end)

    @api.one
    @api.onchange('date_end')
    def on_change_date_end(self):
        if self.date_start is not False and self.date_end is not False:
            self.estimated_days = self.count_days_without_weekend(
                fields.Datetime.from_string(self.date_start),
                fields.Datetime.from_string(self.date_end))
            if self.project_id.calculation_type == 'date_end':
                date_end = fields.Datetime.from_string(
                    self.project_id.date)
                date_start = fields.Datetime.from_string(self.date_end)
            self.from_days = self.count_days_without_weekend(
                date_start, date_end)

    def task_recalculate(self):
        increment = (True if self.project_id.calculation_type == 'date_begin'
                     else False)
        project_date = (fields.Datetime.from_string(self.project_id.date_start)
                        if self.project_id.calculation_type == 'date_begin'
                        else fields.Datetime.from_string(self.project_id.date))
        if increment:
            task_date_start = fields.Datetime.to_string(
                self.calculate_date_without_weekend(
                    project_date, self.from_days, increment=increment))
            date_start = fields.Datetime.from_string(task_date_start)
            task_date_end = fields.Datetime.to_string(
                self.calculate_date_without_weekend(
                    date_start, self.estimated_days))
        else:
            task_date_end = fields.Datetime.to_string(
                self.calculate_date_without_weekend(
                    project_date, self.from_days, increment=increment))
            date_end = fields.Datetime.from_string(task_date_end)
            task_date_start = fields.Datetime.to_string(
                self.calculate_date_without_weekend(
                    date_end, self.estimated_days, increment=increment))
        self.write({'date_start': task_date_start, 'date_end': task_date_end})
