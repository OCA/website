# -*- coding: utf-8 -*-
# Python source code encoding : https://www.python.org/dev/peps/pep-0263/
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    This module copyright :
#        (c) 2015 Antiun Ingenieria, SL (Madrid, Spain, http://www.antiun.com)
#                 Antonio Espinosa <antonioea@antiun.com>
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
##############################################################################

from openerp import models, api, _
from openerp.exceptions import Warning
import requests
import re
import logging
from lxml import etree
from collections import OrderedDict

logger = logging.getLogger(__name__)


class NaceImport(models.TransientModel):
    _name = 'nace.import'
    _description = 'Import NACE activities from European RAMON service'
    _parents = [False, False, False, False]
    _available_langs = {
        'bg_BG': 'BG',  # Bulgarian
        'cs_CZ': 'CZ',  # Czech
        'da_DK': 'DA',  # Danish
        'de_DE': 'DE',  # German
        'et_EE': 'EE',  # Estonian
        'el_GR': 'EL',  # Greek
        'es_AR': 'ES',  # Spanish (AR)
        'es_BO': 'ES',  # Spanish (BO)
        'es_CL': 'ES',  # Spanish (CL)
        'es_CO': 'ES',  # Spanish (CO)
        'es_CR': 'ES',  # Spanish (CR)
        'es_DO': 'ES',  # Spanish (DO)
        'es_EC': 'ES',  # Spanish (EC)
        'es_GT': 'ES',  # Spanish (GT)
        'es_HN': 'ES',  # Spanish (HN)
        'es_MX': 'ES',  # Spanish (MX)
        'es_NI': 'ES',  # Spanish (NI)
        'es_PA': 'ES',  # Spanish (PA)
        'es_PE': 'ES',  # Spanish (PE)
        'es_PR': 'ES',  # Spanish (PR)
        'es_PY': 'ES',  # Spanish (PY)
        'es_SV': 'ES',  # Spanish (SV)
        'es_UY': 'ES',  # Spanish (UY)
        'es_VE': 'ES',  # Spanish (VE)
        'es_ES': 'ES',  # Spanish
        'fi_FI': 'FI',  # Finnish
        'fr_BE': 'FR',  # French (FR)
        'fr_CA': 'FR',  # French (CA)
        'fr_CH': 'FR',  # French (CH)
        'fr_FR': 'FR',  # French
        'hr_HR': 'HR',  # Croatian
        'hu_HU': 'HU',  # Hungarian
        'it_IT': 'IT',  # Italian
        'lt_LT': 'LT',  # Lithuanian
        'lv_LV': 'LV',  # Latvian
        # '': 'MT',  # Il-Malti, has no language in Odoo
        'nl_BE': 'NL',  # Dutch (BE)
        'nl_NL': 'NL',  # Dutch
        'nb_NO': 'NO',  # Norwegian Bokmål
        'pl_PL': 'PL',  # Polish
        'pt_BR': 'PT',  # Portuguese (BR)
        'pt_PT': 'PT',  # Portuguese
        'ro_RO': 'RO',  # Romanian
        'ru_RU': 'RU',  # Russian
        'sl_SI': 'SI',  # Slovenian
        'sk_SK': 'SK',  # Slovak
        'sv_SE': 'SV',  # Swedish
        'tr_TR': 'TR',  # Turkish
    }
    _map = OrderedDict([
        ('level', {'xpath': '', 'attrib': 'idLevel', 'type': 'integer',
                   'translate': False, 'required': True}),
        ('code', {'xpath': '', 'attrib': 'id', 'type': 'string',
                  'translate': False, 'required': True}),
        ('name', {'xpath': './Label/LabelText', 'type': 'string',
                  'translate': True, 'required': True}),
        ('generic', {
            'xpath': './Property[@name="Generic"]'
                     '/PropertyQualifier[@name="Value"]/PropertyText',
            'type': 'string',  'translate': False, 'required': False}),
        ('rules', {
            'xpath': './Property[@name="ExplanatoryNote"]'
                     '/PropertyQualifier[@name="Rules"]/PropertyText',
            'type': 'string', 'translate': False, 'required': False}),
        ('central_content', {
            'xpath': './Property[@name="ExplanatoryNote"]'
                     '/PropertyQualifier[@name="CentralContent"]/PropertyText',
            'type': 'string', 'translate': True, 'required': False}),
        ('limit_content', {
            'xpath': './Property[@name="ExplanatoryNote"]'
                     '/PropertyQualifier[@name="LimitContent"]/PropertyText',
            'type': 'string', 'translate': True, 'required': False}),
        ('exclusions', {
            'xpath': './Property[@name="ExplanatoryNote"]'
                     '/PropertyQualifier[@name="Exclusions"]/PropertyText',
            'type': 'string', 'translate': True, 'required': False}),
    ])

    _url_base = 'http://ec.europa.eu'
    _url_path = '/eurostat/ramon/nomenclatures/index.cfm'
    _url_params = {
        'TargetUrl': 'ACT_OTH_CLS_DLD',
        'StrNom': 'NACE_REV2',
        'StrFormat': 'XML',
        'StrLanguageCode': 'EN',
        # 'IntKey': '',
        # 'IntLevel': '',
        # 'TxtDelimiter': ';',
        # 'bExport': '',
    }

    def _check_node(self, node):
        if node.get('id') and node.get('idLevel'):
            return True
        return False

    def _mapping(self, node, translate):
        item = {}
        for k, v in self._map.iteritems():
            field_translate = v.get('translate', False)
            field_xpath = v.get('xpath', '')
            field_attrib = v.get('attrib', False)
            field_type = v.get('type', 'string')
            field_required = v.get('required', False)
            if field_translate == translate:
                value = ''
                if field_xpath:
                    n = node.find(field_xpath)
                else:
                    n = node
                if n is not None:
                    if field_attrib:
                        value = n.get(field_attrib, '')
                    else:
                        value = n.text
                    if field_type == 'integer':
                        try:
                            value = int(value)
                        except:
                            value = 0
                else:
                    logger.debug("xpath = '%s', not found" % field_xpath)
                if field_required and not value:
                    raise Warning(
                        _('Value not found for mandatory field %s' % k))
                item[k] = value
        return item

    def _download_nace(self, lang_code):
        params = self._url_params.copy()
        params['StrLanguageCode'] = lang_code
        url = self._url_base + self._url_path + '?'
        url += '&'.join([k + '=' + v for k, v in params.iteritems()])
        logger.info('Starting to download %s' % url)
        try:
            res_request = requests.get(url)
        except Exception, e:
            raise Warning(
                _('Got an error when trying to download the file: %s.') %
                str(e))
        if res_request.status_code != requests.codes.ok:
            raise Warning(
                _('Got an error %d when trying to download the file %s.')
                % (res_request.status_code, url))
        logger.info('Download successfully %d bytes' %
                    len(res_request.content))
        # Workaround XML: Remove all characters before <?xml
        pattern = re.compile(r'^.*<\?xml', re.DOTALL)
        content_fixed = re.sub(pattern, '<?xml', res_request.content)
        if not re.match(r'<\?xml', content_fixed):
            raise Warning(_('Downloaded file is not a valid XML file'))
        return content_fixed

    @api.model
    def create_or_update_nace(self, node):
        if not self._check_node(node):
            return False

        nace_model = self.env['res.partner.nace']
        data = self._mapping(node, False)
        data.update(self._mapping(node, True))
        level = data.get('level', 0)
        if level >= 2 and level <= 5:
            data['parent_id'] = self._parents[level - 2]
        nace = nace_model.search([('level', '=', data['level']),
                                  ('code', '=', data['code'])])
        if nace:
            nace.write(data)
        else:
            nace = nace_model.create(data)
        if level >= 1 and level <= 4:
            self._parents[level - 1] = nace.id
        return nace

    @api.model
    def translate_nace(self, node, lang):
        translation_model = self.env['ir.translation']
        nace_model = self.env['res.partner.nace']
        index = self._mapping(node, False)
        trans = self._mapping(node, True)
        nace = nace_model.search([('level', '=', index['level']),
                                  ('code', '=', index['code'])])
        if nace:
            for field, value in trans.iteritems():
                name = 'res.partner.nace,' + field
                query = [('res_id', '=', nace.id),
                         ('type', '=', 'model'),
                         ('name', '=', name),
                         ('lang', '=', lang.code)]
                translation = translation_model.search(query)
                data = {
                    'value': value,
                    'state': 'translated'
                }
                if translation:
                    translation_model.write(data)
                else:
                    data['res_id'] = nace.id
                    data['type'] = 'model'
                    data['name'] = name
                    data['lang'] = lang.code
                    translation_model.create(data)

    @api.one
    def run_import(self):
        nace_model = self.env['res.partner.nace'].\
            with_context(defer_parent_store_computation=True)
        lang_model = self.env['res.lang']
        # Available lang list
        langs = lang_model.search(
            [('code', 'in', self._available_langs.keys()),
             ('active', '=', True)])
        # All current NACEs, delete if not found above
        naces_to_delete = nace_model.search([])
        # Download NACEs in english, create or update
        logger.info('Import NACE Rev.2 English')
        xmlcontent = self._download_nace('EN')
        dom = etree.fromstring(xmlcontent)
        for node in dom.iter('Item'):
                logger.debug('Reading level=%s, code=%s' %
                             (node.get('idLevel', 'N/A'),
                              node.get('id', 'N/A')))
                nace = self.create_or_update_nace(node)
                if nace and nace in naces_to_delete:
                    naces_to_delete -= nace
        # Download NACEs in other languages, translate them
        for lang in langs:
            logger.info('Import NACE Rev.2 %s' % lang.code)
            nace_lang = self._available_langs[lang.code]
            xmlcontent = self._download_nace(nace_lang)
            dom = etree.fromstring(xmlcontent)
            for node in dom.iter('Item'):
                logger.debug('Reading lang=%s, level=%s, code=%s' %
                             (nace_lang, node.get('idLevel', 'N/A'),
                              node.get('id', 'N/A')))
                self.translate_nace(node, lang)
        # Delete obsolete NACEs
        if naces_to_delete:
            naces_to_delete.unlink()
            logger.info('%d NACEs entries deleted' % len(naces_to_delete))
        logger.info(
            'The wizard to create NACEs entries from RAMON '
            'has been successfully completed.')

        return True
