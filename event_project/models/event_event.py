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


class EventEvent(models.Model):
    _inherit = 'event.event'

    project_template = fields.Many2one(
        comodel_name='project.project', string='Template project',
        domain="[('state', '=', 'template')]")
    project = fields.Many2one(
        comodel_name='project.project', string='Related project',
        readonly=True)

    tasks = fields.One2many(
        comodel_name='project.task', related='project.task_ids',
        string="Tasks")
    count_tasks = fields.Integer(string='Task number', compute='_count_tasks')

    @api.one
    @api.depends('tasks')
    def _count_tasks(self):
        self.count_tasks = len(self.tasks)

    def get_project_with_duplicate_template(self, template):
        return self.env['project.project'].browse(
            int(template.duplicate_template()['res_id']))

    @api.onchange('project_template')
    def on_change_project_template(self):
        if self.project_template and not self.project:
            self.project = self.get_project_with_duplicate_template(
                self.project_template)

    @api.onchange('date_begin')
    def on_change_date_begin(self):
        if (self.date_begin and self.project
                and self.project.calculation_type is not False
                and self.project.calculation_type == 'date_begin'):
            self.project.write({'date_start': self.date_begin})
            self.project.project_recalculate()

    @api.onchange('date_end')
    def on_change_date_end(self):
        if (self.date_begin and self.project
                and self.project.calculation_type is not False
                and self.project.calculation_type == 'date_end'):
            self.project.write({'date': self.date_end})
            self.project.project_recalculate()

    @api.onchange('name')
    def on_change_name(self):
        if self.name and self.project:
            self.project.write({'name': self.name})
