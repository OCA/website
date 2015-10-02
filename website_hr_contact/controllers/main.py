# -*- coding: utf-8 -*-
##############################################################################
#
#     This file is part of website_hr_contact, an Odoo module.
#
#     Copyright (c) 2015 ACSONE SA/NV (<http://acsone.eu>)
#
#     website_hr_contact is free software: you can redistribute it and/or
#     modify it under the terms of the GNU Affero General Public License
#     as published by the Free Software Foundation, either version 3 of
#     the License, or (at your option) any later version.
#
#     website_hr_contact is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU Affero General Public License for more details.
#
#     You should have received a copy of the
#     GNU Affero General Public License
#     along with website_hr_contact.
#     If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import werkzeug

from openerp import http
from openerp.addons.website.models.website import slug
from openerp.osv.orm import browse_record


class QueryURL(object):
    def __init__(self, path='', path_args=None, **args):
        self.path = path
        self.args = args
        self.path_args = set(path_args or [])

    def __call__(self, path=None, path_args=None, **kw):
        path = path or self.path
        for k, v in self.args.items():
            kw.setdefault(k, v)
        path_args = set(path_args or []).union(self.path_args)
        paths, fragments = [], []
        for key, value in kw.items():
            if value and key in path_args:
                if isinstance(value, browse_record):
                    paths.append((key, slug(value)))
                else:
                    paths.append((key, value))
            elif value:
                if isinstance(value, list) or isinstance(value, set):
                    fragments.append(
                        werkzeug.url_encode([(key, item) for item in value]))
                else:
                    fragments.append(werkzeug.url_encode([(key, value)]))
        for key, value in paths:
            path += '/' + key + '/%s' % value
        if fragments:
            path += '?' + '&'.join(fragments)
        return path


class WebsiteHrAddressbook(http.Controller):
    _items_per_page = 20

    def _get_children_department_recursive(self, root, visible_departments):
        tree = []
        for department in root.child_ids:
            children = self._get_children_department_recursive(
                department, visible_departments)
            if department in visible_departments:
                tree.append({
                    'department': visible_departments.filtered(
                        lambda rec: rec.id == department.id),
                    'children': children
                    })
            else:
                tree.extend(children)
        return tree

    def _get_departments_tree(self, department=None, search=None, **post):
        """ Build a department tree with only published departments
        The tree only contains published department even if the parent
        department is not published.
        """
        tree = []
        request = http.request
        hr_department = request.env['hr.department']
        sudo_hr_department = hr_department.sudo()
        visible_departments = hr_department.search([(1, '=', 1)])
        departments = sudo_hr_department.search([('parent_id', '=', False)])
        for department in departments:
            children = self._get_children_department_recursive(
                department, visible_departments)
            if department in visible_departments:
                tree.append({
                    'department': visible_departments.filtered(
                        lambda rec: rec.id == department.id),
                    'children': children
                    })
            else:
                tree.extend(children)
        return tree

    def _get_employees_domain(self, department=None, search=None, **post):
        domain = []
        if department:
            domain.append(('department_id', '=', department.id))
        if search:
            domain.append(('name', 'ilike', search))
        return domain

    @http.route(['/page/hr_contact/employees',
                 '/page/hr_contact/employees/page/<int:page>',
                 '/page/hr_contact/employees/department/'
                 '<model("hr.department"):department>',
                 '/page/hr_contact/employees/department/'
                 '<model("hr.department"):department>/page/<int:page>'
                 ], type='http', auth="public", website=True)
    def employees(self, department=None, search='', page=1, **post):
        request = http.request
        hr_employee = request.env['hr.employee']
        departments_tree = self._get_departments_tree(
            department, search, **post)

        domain = self._get_employees_domain(department, search, **post)
        employees = hr_employee.search(domain)

        url_builder = QueryURL(
            '/page/hr_contact/employees', ['department', 'page'],
            department=department)

        count = len(employees)
        pager = request.website.pager(
            url=url_builder(),
            total=count,
            page=page,
            step=self._items_per_page,
            url_args={'search': search},
        )
        pager_begin = (page - 1) * self._items_per_page
        pager_end = page * self._items_per_page
        employees = employees[pager_begin:pager_end]

        values = {
            'employees': employees,
            'departments_tree': departments_tree,
            'department': department,
            'pager': pager,
            'url_builder': url_builder,
            'search': search,
            'count': count,
        }
        return request.website.render(
            'website_hr_contact.employees', values)
