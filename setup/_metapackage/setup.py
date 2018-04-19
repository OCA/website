import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo10-addons-oca-website",
    description="Meta package for oca-website Odoo addons",
    version=version,
    install_requires=[
        'odoo10-addon-website_analytics_piwik',
        'odoo10-addon-website_anchor_smooth_scroll',
        'odoo10-addon-website_blog_category',
        'odoo10-addon-website_breadcrumb',
        'odoo10-addon-website_container_fluid',
        'odoo10-addon-website_cookie_notice',
        'odoo10-addon-website_crm_privacy_policy',
        'odoo10-addon-website_crm_quick_answer',
        'odoo10-addon-website_crm_recaptcha',
        'odoo10-addon-website_field_autocomplete',
        'odoo10-addon-website_form_builder',
        'odoo10-addon-website_form_recaptcha',
        'odoo10-addon-website_legal_page',
        'odoo10-addon-website_logo',
        'odoo10-addon-website_multi_theme',
        'odoo10-addon-website_no_crawler',
        'odoo10-addon-website_odoo_debranding',
        'odoo10-addon-website_sale_hide_empty_category',
        'odoo10-addon-website_sale_line_total',
        'odoo10-addon-website_seo_redirection',
        'odoo10-addon-website_snippet_anchor',
        'odoo10-addon-website_snippet_barcode',
        'odoo10-addon-website_snippet_country_dropdown',
        'odoo10-addon-website_snippet_data_slider',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
