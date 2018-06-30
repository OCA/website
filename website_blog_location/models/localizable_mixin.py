# -*- coding: utf-8 -*-
# © 2017 Therp BV <http://therp.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models
# pylint: disable=W0402
from openerp.osv.expression import AND


class LocalizableMixin(models.AbstractModel):
    """This is a mixin to support operations on models which have a location
    expressed in latitude and longitude"""
    # TODO: if this is useful, put it in its own module
    _name = 'base.localizable.mixin'
    _description = 'Makes records localizable on a map'

    latitude = fields.Float('Latitude')
    longitude = fields.Float('Longitude')

    @api.model
    @api.returns('self')
    def _get_all_localized(self, domain=None):
        """return all records with a location"""
        return self.search(AND[
            domain or [],
            [
                ('latitude', '!=', False),
                ('longitude', '!=', False),
            ],
        ])

    @api.multi
    def _get_location_url(self):
        """return an URL the user is sent to when clicking on a location"""
        raise NotImplementedError('You need to implement this function')
