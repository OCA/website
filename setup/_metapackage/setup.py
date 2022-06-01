import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo13-addons-oca-website",
    description="Meta package for oca-website Odoo addons",
    version=version,
    install_requires=[
        'odoo13-addon-website_analytics_piwik',
        'odoo13-addon-website_breadcrumb',
        'odoo13-addon-website_cookie_notice',
        'odoo13-addon-website_cookiebot',
        'odoo13-addon-website_cookiefirst',
        'odoo13-addon-website_crm_privacy_policy',
        'odoo13-addon-website_crm_quick_answer',
        'odoo13-addon-website_crm_recaptcha',
        'odoo13-addon-website_form_recaptcha',
        'odoo13-addon-website_google_tag_manager',
        'odoo13-addon-website_legal_page',
        'odoo13-addon-website_menu_by_user_status',
        'odoo13-addon-website_menu_icon',
        'odoo13-addon-website_no_crawler',
        'odoo13-addon-website_odoo_debranding',
        'odoo13-addon-website_snippet_big_button',
        'odoo13-addon-website_snippet_country_dropdown',
        'odoo13-addon-website_snippet_marginless_gallery',
        'odoo13-addon-website_snippet_timeline',
        'odoo13-addon-website_typed_text',
        'odoo13-addon-website_video_preview',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 13.0',
    ]
)
