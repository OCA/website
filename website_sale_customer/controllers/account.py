# -*- coding: utf-8 -*-

from openerp import SUPERUSER_ID
from openerp import http
from openerp.http import request

from ..utils import validate_email
from ..utils import HAS_PyDNS
from ..utils import validate_phonenumber


class ShopUserAccountController(http.Controller):
    """ This is mainly a refactoring of `website_sale` checkout controller.
    """
    my_account_template = "website_sale_customer.my_account"
    mandatory_billing_fields = [
        "name", "phone", "email",
        "street2", "city", "country_id", "zip",
    ]
    optional_billing_fields = [
        "street", "state_id", "vat",
        "vat_subjected",
    ]
    mandatory_shipping_fields = [
        "name", "phone", "street",
        "city", "country_id", "zip",
    ]
    optional_shipping_fields = ["state_id", ]
    mandatory_fields = {}.fromkeys(
        mandatory_billing_fields +
        ['shipping_%s' % x for x in mandatory_shipping_fields],
        True
    )
    # use this to inject your form fields helpers
    form_fields_helpers = {}

    @http.route(['/shop/my-account'], type='http', auth="user", website=True)
    def my_account(self, **post):
        values = self.user_info_values(post)
        if request.httprequest.method == 'POST':
            values["error"], values['error_messages'] = \
                self.validate_user_form(values["user_info"])
            if values["error"]:
                return request.website.render(self.my_account_template, values)
            self.save_user_form(values['user_info'])
        return request.website.render(self.my_account_template, values)

    def user_info_values(self, data=None):
        cr, uid, context, registry = \
            request.cr, request.uid, request.context, request.registry
        partner_model = registry.get('res.partner')
        user_model = registry.get('res.users')
        country_model = registry.get('res.country')
        state_model = registry.get('res.country.state')

        country_ids = country_model.search(cr, SUPERUSER_ID, [],
                                           context=context)
        countries = country_model.browse(cr, SUPERUSER_ID, country_ids,
                                         context)
        states_ids = state_model.search(cr, SUPERUSER_ID, [],
                                        context=context)
        states = state_model.browse(cr, SUPERUSER_ID, states_ids, context)
        partner = user_model.browse(cr, SUPERUSER_ID, uid, context).partner_id

        shipping_id = None
        shipping_ids = []
        user_info = {}
        if not data:
            if request.uid != request.website.user_id.id:
                user_info.update(self.user_info_parse("billing", partner))
                shipping_ids = partner_model.search(
                    cr, SUPERUSER_ID,
                    [("parent_id", "=", partner.id),
                     ('type', "=", 'delivery')],
                    context=context
                )
        else:
            user_info = self.user_info_parse('billing', data)
            try:
                shipping_id = int(data["shipping_id"])
            except ValueError:
                pass
            if shipping_id == -1:
                user_info.update(self.user_info_parse('shipping', data))

        shipping_ids = list(set(shipping_ids) - set([partner.id]))

        if shipping_id == partner.id:
            shipping_id = 0
        elif shipping_id > 0 and shipping_id not in shipping_ids:
            shipping_ids.append(shipping_id)
        elif shipping_id is None and shipping_ids:
            shipping_id = shipping_ids[0]

        ctx = dict(context, show_address=1)
        shippings = []
        if shipping_ids:
            shippings = shipping_ids and partner_model.browse(
                cr, SUPERUSER_ID, list(shipping_ids), ctx) or []
        if shipping_id > 0:
            shipping = partner_model.browse(cr, SUPERUSER_ID, shipping_id, ctx)
            user_info.update(self.user_info_parse("shipping", shipping))

        user_info['shipping_id'] = shipping_id

        # Default_model.search by user country
        if not user_info.get('country_id'):
            country_code = request.session['geoip'].get('country_code')
            if country_code:
                country_ids = country_model.search(
                    cr, uid, [('code', '=', country_code)],
                    context=context)
                if country_ids:
                    user_info['country_id'] = country_ids[0]

        values = {
            'countries': countries,
            'states': states,
            'user_info': user_info,
            'shipping_id': partner.id != shipping_id and shipping_id or 0,
            'shippings': shippings,
            'error': {},
            'form_fields_helpers': self.form_fields_helpers,
            'mandatory_fields': self.mandatory_fields,
            'has_check_vat': hasattr(registry['res.partner'], 'check_vat')
        }
        return self.prepare_values(values)

    def prepare_values(self, values):
        """ override this to inject defaults or do other stuff
        """
        return values

    def user_info_parse(self, address_type, data, remove_prefix=False):
        """ data is a dict OR a partner_model.browse record
        """
        # set mandatory and optional fields
        assert address_type in ('billing', 'shipping')
        if address_type == 'billing':
            all_fields = self.mandatory_billing_fields + \
                self.optional_billing_fields
            prefix = ''
        else:
            all_fields = self.mandatory_shipping_fields + \
                self.optional_shipping_fields
            prefix = 'shipping_'

        # set data
        if isinstance(data, dict):
            query = dict(
                (prefix + field_name, data[prefix + field_name])
                for field_name in all_fields
                if data.get(prefix + field_name)
            )
        else:
            query = dict(
                (prefix + field_name, getattr(data, field_name))
                for field_name in all_fields
                if getattr(data, field_name)
            )
            if address_type == 'billing' and data.parent_id:
                query[prefix + 'street'] = data.parent_id.name

        if query.get(prefix + 'state_id'):
            query[prefix + 'state_id'] = int(query[prefix + 'state_id'])
        if query.get(prefix + 'country_id'):
            query[prefix + 'country_id'] = int(query[prefix + 'country_id'])

        if query.get(prefix + 'vat'):
            query[prefix + 'vat_subjected'] = True

        if not remove_prefix:
            return query

        return dict(
            (field_name, data[prefix + field_name])
            for field_name in all_fields
            if data.get(prefix + field_name)
        )

    def validate_user_form(self, data):
        # Validation
        error = {}
        for field_name in self.mandatory_billing_fields:
            if not data.get(field_name):
                error[field_name] = 'missing'
        for k, v in data.iteritems():
            validator_key = k
            # handle prefix
            if k != 'shipping_id' and validator_key.startswith('shipping_'):
                validator_key = k[len('shipping_'):]
            validator_name = '_validate_%s' % validator_key
            if hasattr(self, validator_name):
                validator = getattr(self, validator_name)
                validator(k, v, data, error=error)
        error_messages = self.get_error_messages(error)
        return error, error_messages

    def _validate_vat(self, key, value, data, error={}):
        cr, uid, registry = \
            request.cr, request.uid, request.registry

        partner_model = registry["res.partner"]

        if value and hasattr(partner_model, "check_vat"):
            if request.website.company_id.vat_check_vies:
                # force full VIES online check
                check_func = partner_model.vies_vat_check
            else:
                # quick and partial off-line checksum validation
                check_func = partner_model.simple_vat_check
            vat_country, vat_number = partner_model._split_vat(value)
            # simple_vat_check
            if not check_func(cr, uid, vat_country, vat_number, context=None):
                error[key] = 'error'
        return error

    def _validate_shipping_id(self, key, value, data, error={}):
        if value == -1:
            for field_name in self.mandatory_shipping_fields:
                field_name = 'shipping_' + field_name
                if not data.get(field_name):
                    error[field_name] = 'missing'
        return error

    def _validate_email(self, key, value, data, error={}):
        if not validate_email(value, verify=HAS_PyDNS):
            error[key] = 'wrong'
        return error

    def _validate_phone(self, key, value, data, error={}):
        if not validate_phonenumber(value):
            error[key] = 'wrong'
        return error

    def get_error_messages(self, errors):
        """ override this to inject your error messages
        """
        return {}

    def save_user_form(self, user_info):
        cr, uid, context, registry = \
            request.cr, request.uid, request.context, request.registry

        partner_model = registry.get('res.partner')
        user_model = registry.get('res.users')
        partner_lang = request.lang if request.lang in [
            lang.code for lang in request.website.language_ids] else None

        billing_info = {}
        if partner_lang:
            billing_info['lang'] = partner_lang
        billing_info.update(self.user_info_parse('billing', user_info, True))

        # set partner_id
        partner_id = None
        if request.uid != request.website.user_id.id:
            partner_id = user_model.browse(cr, SUPERUSER_ID, uid,
                                           context=context).partner_id.id
        # save partner informations
        partner_model.write(cr, SUPERUSER_ID, [partner_id], billing_info,
                            context=context)

        # create a new shipping partner
        if user_info.get('shipping_id') == -1:
            shipping_info = {}
            if partner_lang:
                shipping_info['lang'] = partner_lang
            shipping_info.update(
                self.user_info_parse('shipping', user_info, True))
            shipping_info['type'] = 'delivery'
            shipping_info['parent_id'] = partner_id
            user_info['shipping_id'] = partner_model.create(
                cr, SUPERUSER_ID, shipping_info, context)
