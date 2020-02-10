# Copyright 2004 Tech-Receptives Solutions Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Website reCAPTCHA Reloaded',
    'version': '12.0.0.1.0',
    'category': 'Website',
    'depends': ['website'],
    'author': 'Tech Receptives',
    'license': 'AGPL-3',
    'website': 'https://www.techreceptives.com',
    'description': """
    Odoo Website reCAPTCHA Reloaded
    ================================
    This modules allows you to integrate Google reCAPTCHA v2.0 to your website
    forms. You can configure your Google reCAPTCHA site and public keys
    in "Settings" -> "Website Settings"

    You will need to install various website_<module>_recaptcha modules
    to use it in your various pages.
    """,
    'data': [
      'views/website_view.xml',
      'views/res_config.xml',
     ],
    'installable': True,
}
