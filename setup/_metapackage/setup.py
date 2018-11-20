import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-website",
    description="Meta package for oca-website Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-website_crm_privacy_policy',
        'odoo12-addon-website_legal_page',
        'odoo12-addon-website_odoo_debranding',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
