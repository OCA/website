{
    "name": "portal_email_readonly",
    "summary": """
         This module is an addition to Odoo's portal module, and makes sure
         that the email field on the 'My Account' page in the portal / website / webshop
         is not editable by the portal user. This can be very useful when making use of an
         extended authentication tooling that uses the email address as the user id,
         and you do not want this to be changed. The module also introduces an error
         pop-up when a back office user is trying to change the email address field in
         any res.partner record after portal access has been granted to the res.user of
         the concerning res.partner.""",
    "author": "TOSC - K.Sushma, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/website",
    # Categories can be used to filter modules in modules listing
    "category": "Hidden",
    "version": "16.0.0.0.0",
    "license": "",
    # any module necessary for this one to work correctly
    "depends": ["portal"],
    # always loaded
    "data": [
        "views/portal_templates.xml",
    ],
    # only loaded in demonstration mode
    "demo": [],
}
