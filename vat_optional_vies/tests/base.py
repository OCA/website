# -*- coding: utf-8 -*-
# See README.rst file on addon root folder for license details

from openerp.tests.common import TransactionCase

# Define test_cases as tuples or dictionaries

# project_date_cases = (
#     # name, start_date, end date
#     ('pj_0', '2015-08-01', '2015-10-03'),  # Saturday
#     ('pj_1', '2015-08-02', '2015-10-10'),  # Sunday
#     ('pj_2', '2015-08-03', '2015-10-17'),  # Monday
# )

# task_days_cases = {
#     'date_begin': (
#         # name, from_days, estimate_days
#         ('task_0', 0, 5),  # 03/08/2015 to 07/08/2015
#         ('task_1', 4, 1),  # 06/08/2015 to 06/08/2015
#         ('task_2', 5, 11),  # 07/08/2015 to 19/08/2015
#         ('task_3', 12, 20),  # 18/08/2015 to 14/09/2015
#         ('task_4', 21, 2),  # 31/08/2015 to 01/09/2015
#     ),
# }

# Define test_solutions as tuples or dictionaries

# project_dates_solutions = {
#     'tasks': {
#         'date_begin': (
#             ('pj_0', '2015-08-01', '???'),  # Saturday
#             ('pj_1', '2015-08-02', '???'),  # Sunday
#             ('pj_2', '2015-08-03', '???'),  # Monday
#         ),
#     }
# }


class BaseCase(TransactionCase):
    # Use case : Prepare some data for current test case
    def setUp(self):
        super(BaseCase, self).setUp()
        # More initializations here ...

    # Use case : Clean data after current test case
    def tearDown(self):
        # Clean data here ...
        super(BaseCase, self).tearDown()

    # Auxiliar common methods here
    # Method name can't start with 'test_'

    # Common test methods here
    # Method name must start with 'test_'
