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

    def project_template_duplicate(self):
        if self.project_template and not self.project:
            assert len(self) >= 0 and len(self) <= 1, "Expected singleton"
            result = self.project_template.duplicate_template()
            self.project = result['res_id']
            name = self.name
            self.project.write({'name': name,
                                'date_start': self.date_begin,
                                'date': self.date_begin,
                                'calculation_type': 'date_end'})
            self.project.project_recalculate()
            return True
        return False

    def project_data_update(self, vals):
        map_vals = {}
        recalculate = False
        if self.project:
            if vals.get('name'):
                map_vals['name'] = self.name
            if vals.get('date_begin'):
                map_vals['date_start'] = self.date_begin
                map_vals['date'] = self.date_begin
                recalculate = True
            if map_vals:
                self.project.write(map_vals)
                if recalculate:
                    self.project.project_recalculate()
        return True

    @api.model
    def create(self, vals):
        event = super(EventEvent, self).create(vals)
        event.project_template_duplicate()
        return event

    @api.multi
    def write(self, vals):
        super(EventEvent, self).write(vals)
        if not self.project_template_duplicate():
            self.project_data_update(vals)
        return True
