# -*- coding: utf-8 -*-
# © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

from openerp import exceptions


class NoOriginError(exceptions.ValidationError):
    pass


class NoRedirectionError(exceptions.ValidationError):
    pass
