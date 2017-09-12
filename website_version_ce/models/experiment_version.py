# -*- coding: utf-8 -*-#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo import models, fields


class ExperimentVersion(models.Model):
    """ Allow to define the versions contained in an experiment.
    The frequency is a ponderation to determine the probability to visit
    a version in an experiment.
    The googe_index is the index of a version in an experiment, used to send
    data to Google Analytics.
    """

    _name = "website_version_ce.experiment.version"
    _rec_name = "version_id"

    version_id = fields.Many2one(
        'website_version_ce.version',
        string="Version", required=True,
        ondelete='cascade'
    )
    experiment_id = fields.Many2one(
        'website_version_ce.experiment',
        string="Experiment",
        required=True,
        ondelete='cascade'
    )
    frequency = fields.Selection(
        [('10', 'Less'), ('50', 'Medium'), ('80', 'More')],
        string='Frequency', default='50')
    google_index = fields.Integer(string='Google index')
