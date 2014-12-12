# -*- encoding: utf-8 -*-
#
# OpenERP, Open Source Management Solution
# This module copyright (C) 2013 Savoir-faire Linux
#    (<http://www.savoirfairelinux.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

from openerp.tests import common


class test_product_template(common.TransactionCase):
    def setUp(self):
        super(test_product_template, self).setUp()
        self.product_template_model = self.env['product.template']
        self.product = self.product_template_model.create(
            {'name': "t_name"}
        )

    def test_build_description_sale_human_names(self):
        """Double check if description saves the name of the field
        not the technical names.
        """
        product = self.product_template_model.create(
            {
                'name': "t_name",
                'list_price': 64,
            },
        )
        self.assertEqual(
            product.build_description_sale(('name', 'list_price')),
            u'Sale Price: 64.0\nName: t_name',
        )

    def test_build_description_sale_translations_names(self):
        """Double check if description saves the translations of the name
        of the fields.
        """
        product = self.product_template_model.with_context(
            {'lang': 'fr'}
        ).create({'name': 't_name',},)

        self.assertEqual(
            product.build_description_sale(('name',)),
            u'Nom: t_name',
        )

    def test_build_description_sale_accept_special_caracters(self):
        """Double check if the process accepts special characters"""
        product = self.product_template_model.create(
            {'name': "éè & more"}
        )
        self.assertEqual(
            product.build_description_sale(('name',)), u'Name: éè & more'
        )

    def test_build_description_sale_ask_for_list_as_arg(self):
        """Double check the behaviour if the arg is not a list/tuple"""
        self.assertRaises(
            AssertionError,
            self.product.build_description_sale,
            'n'
        )

    def test_copy_into_description_sale_ask_for_list_as_arg(self):
        """Double check the behaviour if the arg is not a list/tuple"""
        self.assertRaises(
            AssertionError,
            self.product.copy_into_description_sale,
            'n'
        )

    def test_copy_into_description_sale_not_accept_description_as_field(self):
        """description should not be in field_to_copy as it is the target of
        the copy"""
        self.assertRaises(
            AssertionError,
            self.product.copy_into_description_sale,
            ('description',)
        )

    def test_copy_into_description_sale_fields_basestring(self):
        """all the members of fields_to_copy have to be a name of a field.
        'n' is not a field of product so assertionError should be raised."""
        self.assertRaises(
            AssertionError,
            self.product.copy_into_description_sale,
            ('n',)
        )

    def test_copy_into_description_sale_update_description_sale(self):
        """Double checks the description_sale is updated during the process"""
        original_description = self.product.description_sale
        self.product.copy_into_description_sale(('name',))
        self.assertNotEqual(
            self.product.description_sale, original_description
        )
