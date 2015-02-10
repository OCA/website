# -*- encoding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################
from openerp import models, fields, api


class EventEvent(models.Model):
    _inherit = 'event.event'

    tasks = fields.One2many(
        comodel_name='project.task', inverse_name='event', string="Tasks")
    count_tasks = fields.Integer(string='Task number', compute='_count_tasks')

    @api.one
    @api.depends('tasks')
    def _count_tasks(self):
        self.count_tasks = len(self.tasks)
