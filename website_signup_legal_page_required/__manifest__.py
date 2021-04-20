# Copyright 2015 Tecnativa
# Copyright 2016 Alessio Gerace - Agile Business Group
# Copyright 2018 Lorenzo Battistini - Agile Business Group
# Copyright 2021 Lorenzo Battistini @ TAKOBI
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Require accepting legal terms",
    "summary": "Force the user to accept the legal terms to open an account.",
    "version": "12.0.1.0.0",
    "category": "Website",
    "website": "https://github.com/OCA/website",
    "author": "Antiun Ingeniería S.L.,"
              " Agile Business Group, José Luis Sandoval Alaguna,"
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "website_legal_page",
    ],
    "data": [
        "views/pages.xml",
        "views/res_users.xml",
    ],
    "application": False,
    "installable": True,
}
