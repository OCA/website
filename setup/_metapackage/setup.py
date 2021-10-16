import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-oca-website",
    description="Meta package for oca-website Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-website_crm_quick_answer',
        'odoo14-addon-website_google_tag_manager',
        'odoo14-addon-website_legal_page',
        'odoo14-addon-website_odoo_debranding',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
