# -*- coding: utf-8 -*-#
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from odoo.exceptions import UserError
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.translate import _

TOO_MUCH_EXPERIMENTS = 2
OVERLAP_EXPERIMENT = 1
CREATE_EXPERIMENT = 0


class Goals(models.Model):
    """ Allow to define the goal of an experiment.
    The goals are defined in the Google Analytics account and can be
    synchronised in backend.
    """
    _name = "website_version_ce.goals"

    name = fields.Char(string="Name", required=True)
    google_ref = fields.Char(string="Google Reference", required=True)


class Experiment(models.Model):
    """ An experiment pointed to some experiment_versions and dispatch
    each website visitor to a version.
    """

    _name = "website_version_ce.experiment"
    _inherit = ['mail.thread']
    _order = 'sequence'

    name = fields.Char(string="Title", required=True)
    experiment_version_ids = fields.One2many(
        'website_version_ce.experiment.version',
        'experiment_id',
        string="Experiment Version"
    )
    website_id = fields.Many2one('website', string="Website", required=True)
    state = fields.Selection(
        [
            ('running', 'Running'),
            ('paused', 'Paused'),
            ('ended', 'Ended')
        ],
        'Status', required=True, copy=False, track_visibility='onchange',
        default='running')
    goal_id = fields.Many2one('website_version_ce.goals', string="Objective",
                              required=True)
    color = fields.Integer('Color Index')
    version_number = fields.Integer(compute='_compute_version_number',
                                    string='Version Number')
    sequence = fields.Integer(required=True, default=1)
    google_id = fields.Char(string="Google id")

    @api.multi
    @api.constrains('state')
    def _check_view(self):
        # No overlap for running experiments
        for exp in self:
            if exp.state == 'running':
                for exp_ver in exp.experiment_version_ids:
                    if exp_ver.search([
                        ('version_id.view_ids.key', 'in',
                         [v.key for v in exp_ver.version_id.view_ids]),
                        ('experiment_id', '!=', exp_ver.experiment_id.id),
                        ('experiment_id.website_id', '=',
                         exp_ver.experiment_id.website_id.id),
                        ('experiment_id.state', '=', 'running')
                    ]):
                        raise ValidationError(_(
                            'This experiment contains a view which '
                            'is already used in another running experience'))
        return True

    @api.multi
    @api.constrains('website_id', 'experiment_version_ids')
    def _check_website(self):
        for exp in self:
            for exp_ver in exp.experiment_version_ids:
                if not exp_ver.version_id.website_id.id == exp.website_id.id:
                    raise ValidationError(_(
                        'This experiment must have versions which '
                        'are in the same website'))

    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None,
                   orderby=False, lazy=True):
        """ Override read_group to always display all states. """
        if groupby and groupby[0] == "state":
            # Default result structure
            states = [('running', 'Running'), ('paused', 'Paused'),
                      ('ended', 'Ended')]
            read_group_all_states = [{
                '__context': {'group_by': groupby[1:]},
                '__domain': domain + [('state', '=', state_value)],
                'state': state_value,
                'state_count': 0,
            } for state_value, state_name in states]
            # Get standard results
            read_group_res = super(Experiment, self).read_group(
                domain, fields, groupby, offset=offset, limit=limit,
                orderby=orderby, lazy=lazy)
            # Update standard results with default results
            result = []
            for state_value, state_name in states:
                res = filter(lambda x: x['state'] == state_value,
                             read_group_res)
                if not res:
                    res = filter(lambda x: x['state'] == state_value,
                                 read_group_all_states)
                res[0]['state'] = [state_value, state_name]
                result.append(res[0])
            return result
        else:
            return super(Experiment, self).read_group(
                domain, fields, groupby, offset=offset, limit=limit,
                orderby=orderby, lazy=lazy)

    @api.multi
    def _compute_version_number(self):
        for exp in self:
            exp.version_number = len(exp.experiment_version_ids) + 1

    @api.model
    def create(self, vals):
        exp = {
            'name': vals['name'],
            'objectiveMetric': self.env['website_version_ce.goals'].browse(
                vals['goal_id']).google_ref,
            'status': vals['state'],
            'variations': [
                {'name': 'master', 'url': 'http://localhost/master'}]
        }
        version_list = vals.get('experiment_version_ids', [])
        for version in version_list:
            if version[0] == 0:
                name = self.env['website_version_ce.version'].browse(
                    version[2]['version_id']).name
                # We must give a URL for each version in the experiment
                exp['variations'].append(
                    {'name': name, 'url': 'http://localhost/' + name})
            else:
                raise UserError(_("The experiment you try to create has " +
                                "a bad format."))
        if not version_list:
            raise UserError(_("You must select at least one version in " +
                            "your experiment."))
        vals['google_id'] = self.env['google.management'].create_an_experiment(
            exp, vals['website_id'])
        return super(Experiment, self).create(vals)

    @api.multi
    def write(self, vals):
        state = vals.get('state')
        for exp in self:
            if state and exp.state == 'ended':
                raise UserError(_("You cannot modify an ended experiment."))
            elif state == 'ended':
                # google_data is the data to send to Googe
                google_data = {
                    'name': exp.name,
                    'status': state,
                    'variations': [
                        {'name': 'master', 'url': 'http://localhost/master'}],
                }
                for exp_v in exp.experiment_version_ids:
                    google_data['variations'].append({
                        'name': exp_v.version_id.name,
                        'url': 'http://localhost/'+exp_v.version_id.name
                    })
                # Check the constraints before writing on google analytics
                self.env['google.management'].update_an_experiment(
                    google_data, exp.google_id, exp.website_id.id)
        return super(Experiment, self).write(vals)

    @api.multi
    def unlink(self):
        for exp in self:
            self.env['google.management'].delete_an_experiment(
                exp.google_id, exp.website_id.id)
        return super(Experiment, self).unlink()

    @api.multi
    def update_goals(self):
        gm_obj = self.env['google.management']
        goals_obj = self.env['website_version_ce.goals']
        website_id = self.env.context.get('website_id')
        if not website_id:
            raise UserError(_("You must specify the website."))
        for goal in gm_obj.get_goal_info(website_id)[1]['items']:
            if not goals_obj.search([('name', '=', goal['name'])]):
                vals = {'name': goal['name'],
                        'google_ref': 'ga:goal' + goal['id'] + 'Completions'}
                goals_obj.create(vals)

    def check_no_overlap(self, version_ids):
        if self.search_count(['|', ('state', '=', 'running'),
                              ('state', '=', 'paused')]) >= 24:
            return {'existing': TOO_MUCH_EXPERIMENTS, 'name': ""}

        # Check if version_ids don't overlap with running experiments
        version_keys = set([v['key'] for v in
                            self.env['ir.ui.view'].search_read(
                                [('version_id', 'in', version_ids)], ['key'])])
        exp_mod = self.env['website_version_ce.experiment']
        exps = exp_mod.search([
            ('state', '=', 'running'),
            ('website_id', '=', self.env.context.get('website_id'))])
        for exp in exps:
            for exp_ver in exp.experiment_version_ids:
                for view in exp_ver.version_id.view_ids:
                    if view.key in version_keys:
                        # return the experiment name if there's overlap
                        return {'existing': OVERLAP_EXPERIMENT,
                                'name': exp.name}
        return {'existing': CREATE_EXPERIMENT, 'name': ""}
