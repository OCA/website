import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo-addons-oca-website",
    description="Meta package for oca-website Odoo addons",
    version=version,
    install_requires=[
        'odoo-addon-website_breadcrumb>=15.0dev,<15.1dev',
        'odoo-addon-website_cookiebot>=15.0dev,<15.1dev',
        'odoo-addon-website_cookiefirst>=15.0dev,<15.1dev',
        'odoo-addon-website_crm_privacy_policy>=15.0dev,<15.1dev',
        'odoo-addon-website_crm_quick_answer>=15.0dev,<15.1dev',
        'odoo-addon-website_google_tag_manager>=15.0dev,<15.1dev',
        'odoo-addon-website_legal_page>=15.0dev,<15.1dev',
        'odoo-addon-website_odoo_debranding>=15.0dev,<15.1dev',
        'odoo-addon-website_plausible>=15.0dev,<15.1dev',
        'odoo-addon-website_snippet_big_button>=15.0dev,<15.1dev',
        'odoo-addon-website_snippet_country_dropdown>=15.0dev,<15.1dev',
        'odoo-addon-website_whatsapp>=15.0dev,<15.1dev',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 15.0',
    ]
)
