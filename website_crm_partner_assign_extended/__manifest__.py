# Copyright 2023 - TODAY, Kaynnan Lemes <kaynnan.lemes@escodoo.com.br>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Filter resellers by state and city",
    "summary": """Allow filtering of resellers by state and city on the website""",
    "author": "Escodoo, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/website",
    "category": "Website",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "depends": ["website_crm_partner_assign", "base_address_city"],
    "data": ["views/website_crm_partner_assign_extended.xml"],
}
