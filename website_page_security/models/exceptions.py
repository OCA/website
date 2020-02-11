# -*- coding: utf-8 -*-
# Copyright 2019 Therp BV <https://therp.nl>.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


class AccessDeniedMissingGroup(Exception):

    def __init__(self, request, page):
        super(AccessDeniedMissingGroup, self).__init__(
            'Access denied: user does not have security groups for this page')
        self.request = request
        self.page = page
