# License AGPL-3.0.
{
    "name": "Website Mass Mailing Double opt-in",
    "version": "15.0.1.0.0",
    "category": "Website",
    "author": "ERP Harbor Consulting Services,"
    "Nitrokey GmbH,"
    "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/website",
    "summary": """
    Website Mass Mailing Double opt-in
    Website Mass Mailing Double Opt in is part of website and used to get
    subscription list from newsletter template.

    All the Subscriber can be see under mailing list under newsletter template.
    Added custom template for subscribed message.
    """,
    "depends": [
        "website_mass_mailing",
    ],
    "data": [
        "security/mass_mailing_security.xml",
        "security/ir.model.access.csv",
        "data/mail_template.xml",
        "data/newsletter.xml",
        "views/mass_mailing_view.xml",
        "views/invalid_confirmation.xml",
        "views/unsubscribe_templates.xml",
        "views/subscribe_template.xml",
    ],
    "assets": {
        "web.assets_tests": [
            "website_mass_mailing_double_opt_in/static/tests/**/*",
        ],
    },
    "installable": True,
}
