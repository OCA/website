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

from openerp import models, fields
from openerp.exceptions import Warning  # , RedirectWarning
from openerp.tools.translate import _

import logging
from pprint import pformat
_logger = logging.getLogger(__name__)


class ProjectProject(models.Model):
    _inherit = 'project.project'

    calculation_type = fields.Selection(
        [('date_begin', 'Date begin'), ('date_end', 'Date end')],
        default='date_begin', string='Calculation type',
        help='how to calculate tasks with date start or date end references')

    def calcule_date_start_date_end(self):
        project_task_obj = self.env['project.task']
        project_task_ids = project_task_obj.search(
            [('project_id', '=', self.id)])
        if not project_task_ids:
            raise Warning(_('Cannot recalculate project because your project '
                            'don\'t have tasks.'))
        min_date_start = fields.Datetime.from_string(
            project_task_ids[0].date_start)
        date_start_from_days = project_task_ids[0].from_days
        max_date_end = fields.Datetime.from_string(
            project_task_ids[0].date_end)
        date_start = fields.Datetime.from_string(
            project_task_ids[0].date_start)
        for project_task in project_task_ids:
            date_end = fields.Datetime.from_string(project_task.date_end)
            if min_date_start > date_start:
                min_date_start = date_start
                date_start_from_days = project_task.from_days
            if max_date_end < date_end:
                max_date_end = date_end
        if self.calculation_type == 'date_begin':
            date_start = project_task_obj.calculate_date_without_weekend(
                date_start, date_start_from_days, increment=False)
            date_end = max_date_end
        else:
            date_end = project_task_obj.calculate_date_without_weekend(
                date_end, date_start_from_days, increment=True)
        return (fields.Datetime.to_string(date_start),
                fields.Datetime.to_string(date_end))

    def project_recalculate(self):
        if not self.calculation_type:
            raise Warning(_('Cannot recalculate project because your project '
                            'don\'t have calculation type.'))
        if self.calculation_type == 'date_begin' and not self.date_start:
            raise Warning(_('Cannot recalculate project because your project '
                            'don\'t have date start.'))
        if self.calculation_type == 'date_end' and not self.date:
            raise Warning(_('Cannot recalculate project because your project '
                            'don\'t have date end.'))
        project_task_obj = self.env['project.task']
        project_task_type_obj = self.env['project.task.type']
        project_task_type = project_task_type_obj.search([('fold', '=', True)])
        project_task_type_ids = [x.id for x in project_task_type]
        project_task_ids = project_task_obj.search(
            [('project_id', '=', self.id),
             ('stage_id', 'not in', project_task_type_ids)
             ])
        for project_task in project_task_ids:
            project_task.task_recalculate()
        date_start, date_end = self.calcule_date_start_date_end()
        self.write({'date_start': date_start, 'date': date_end})
