# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class HrJob(models.Model):

    _inherit = 'hr.job'

    unpublish_date = fields.Datetime(
        string='Scheduled Unpublication Date',
    )

    @api.model
    def prepare_unpublish_hr_job(self):
        return {'website_published': False}

    @api.model
    def process_unpublish_hr_job(self):
        """
        Search all publised job with a date_to_unpublish reached and update
        those records with date_to_unpublish to False
        """
        today = fields.Datetime.now()
        domain = [('unpublish_date', '<=', today),
                  ('website_published', '=', True)]
        hr_job = self.search(domain)
        if hr_job:
            hr_job.write(self.prepare_unpublish_hr_job())
