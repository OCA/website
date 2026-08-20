{
    "name": "Portal Invitation by Website",
    "summary": "Restrict portal users to a specific website from the invitation wizard",
    "version": "19.0.1.0.0",
    "author": "Tecnativa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/website",
    "license": "AGPL-3",
    "category": "Website",
    "depends": ["portal", "website"],
    "data": [
        "data/mail_template_portal_welcome.xml",
        "views/portal_wizard_views.xml",
    ],
    "installable": True,
}
