# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo.addons.web_editor.tests.test_ui import TestUi

from . import controllers
from . import models
from .post_init import post_init


# patch away failing tests, this is exactly what we change
TestUi.test_02_admin_rte_inline = lambda *args, **kwargs: None
