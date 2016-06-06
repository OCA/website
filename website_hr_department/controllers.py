# -*- coding: utf-8 -*-
##############################################################################
#
#     This file is part of website_hr_department, an Odoo module.
#
#     Copyright (c) 2015 ACSONE SA/NV (<http://acsone.eu>)
#
#     website_hr_department is free software: you can redistribute it and/or
#     modify it under the terms of the GNU Affero General Public License
#     as published by the Free Software Foundation, either version 3 of
#     the License, or (at your option) any later version.
#
#     website_hr_department is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the
#     GNU Affero General Public License
#     along with website_hr_department.
#     If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import http
from openerp.addons.website_hr.controllers.main import website_hr


class WebsiteHr(website_hr):

    def __get_parent_department(self, department):
        """Return the parent department. The method perform a search
        on the parent_id to enforce the security rules since on a manytoone
        field, the id of the related object is always available on the record
        but can raise an exception if it's accessed using the orm if you
        don't have the sufficient privileges
        """
        parent_id_id = department.parent_id.id
        if not parent_id_id:
            return False
        secure_department_env = department
        sudo_parent = department.parent_id.sudo()
        parent = secure_department_env.search([('id', '=', parent_id_id)])
        while not parent and sudo_parent.id:
            # this level in the department hierarchy is not published
            # skip this level
            parent = secure_department_env.search(
                [('id', '=', sudo_parent.id)])
            sudo_parent = sudo_parent.parent_id
        return parent

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
            parent = self.__get_parent_department(department)
            while parent:
                breadcrumb.append(parent)
                parent = self.__get_parent_department(parent)
            breadcrumb.reverse()
        values = {
            'employees': employees,
            'departments': departments,
            'department': department,
            'breadcrumb': breadcrumb,
        }
        return request.website.render(
            'website_hr_department.departments', values)
