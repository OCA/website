import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo11-addons-oca-website",
    description="Meta package for oca-website Odoo addons",
    version=version,
    install_requires=[
        'odoo11-addon-website_addthis',
        'odoo11-addon-website_adv_image_optimization',
        'odoo11-addon-website_analytics_piwik',
        'odoo11-addon-website_anchor_smooth_scroll',
        'odoo11-addon-website_canonical_url',
        'odoo11-addon-website_cookie_notice',
        'odoo11-addon-website_crm_privacy_policy',
        'odoo11-addon-website_crm_recaptcha',
        'odoo11-addon-website_form_builder',
        'odoo11-addon-website_form_metadata',
        'odoo11-addon-website_form_recaptcha',
        'odoo11-addon-website_img_dimension',
        'odoo11-addon-website_js_below_the_fold',
        'odoo11-addon-website_legal_page',
        'odoo11-addon-website_logo',
        'odoo11-addon-website_media_size',
        'odoo11-addon-website_menu_by_user_status',
        'odoo11-addon-website_multi_theme',
        'odoo11-addon-website_no_crawler',
        'odoo11-addon-website_odoo_debranding',
        'odoo11-addon-website_snippet_anchor',
        'odoo11-addon-website_snippet_preset',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
