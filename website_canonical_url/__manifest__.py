# Copyright initOS GmbH 2016
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': "Website Canonical URL",
    'summary': "Canonical URL in Website Headers",
    'author': "initOS GmbH, Tecnativa, "
              "Camptocamp, Odoo Community Association (OCA)",
    'website': "https://github.com/OCA/website",
    'category': 'Website',
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'website',
    ],
    'data': [
        'views/website_views.xml',
        'templates/layout.xml',
    ],
    'demo': [
        'demo/pages.xml',
    ],
}
