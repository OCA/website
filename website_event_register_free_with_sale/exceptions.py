# -*- coding: utf-8 -*-
# Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import exceptions


class NoNeedForSOError(exceptions.ValidationError):
    """Alters checkout workflow by aborting it after registering.

    Useful when you want to register for free and there is nothing to invoice.
    """
    def __init__(self, registrations):
        self.registrations = registrations
