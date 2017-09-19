# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from datetime import timedelta, date
from odoo import fields
from odoo.tests.common import SavepointCase


class TestHrJob(SavepointCase):

    @classmethod
    def setUpClass(cls):
        super(TestHrJob, cls).setUpClass()
        cls.hr_job = cls.env['hr.job']

    def test_process_unpublish_hr_job(self):
        vals = {
            'name': 'Junior Python/Odoo Developper'
        }
        hr_job = self.hr_job.create(vals)
        # check job is not published
        self.assertFalse(
            hr_job.website_published, 'Should not be published')
        # check there is not date to unpublish
        self.assertFalse(
            hr_job.unpublish_date, 'Should not have a unpublication date')
        # publish job
        hr_job.write({'website_published': True})
        # check job is published
        self.assertTrue(
            hr_job.website_published, 'Should be published')

        # set date to unpublish as tomorrow
        # this must not be unpublished by cron
        tomorrow = date.today()+timedelta(1)
        tomorrow = fields.Date.to_string(tomorrow)
        hr_job.unpublish_date = tomorrow

        self.hr_job.process_unpublish_hr_job()
        self.assertTrue(
            hr_job.website_published,
            'Should not be unpublished as the unpublication date is '
            'for tomorrow')

        # set date to unpublish as yesterday
        # this must be unpublished by cron
        yesterday = date.today() - timedelta(1)
        yesterday = fields.Date.to_string(yesterday)
        hr_job.unpublish_date = yesterday

        self.hr_job.process_unpublish_hr_job()
        self.assertFalse(hr_job.website_published)
