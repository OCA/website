# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import http
from odoo.addons.website_hr.controllers.main import WebsiteHr


class WebsiteHr(WebsiteHr):

    @http.route(['/page/departments',
                 '/page/departments/<model("hr.department"):department>'
                 ], type='http', auth="public", website=True)
    def departments(self, department=None, **post):
        request = http.request
        hr_department = request.env['hr.department']
        departments = hr_department.search([('parent_id', '=', False)])

        hr_employee = request.env['hr.employee']
        employees = []
        breadcrumb = []
        if department:
            employees = hr_employee.search(
                [('department_id', '=', department.id)])
            breadcrumb.append(department)
            parent = department.parent_id
            while parent:
                breadcrumb.append(parent)
                parent = parent.parent_id
            breadcrumb.reverse()
        values = {
            'employees': employees,
            'departments': departments,
            'department': department,
            'breadcrumb': breadcrumb,
        }
        return request.render(
            'website_hr_department.departments', values)
