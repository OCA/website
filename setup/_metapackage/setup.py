import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo9-addons-oca-website",
    description="Meta package for oca-website Odoo addons",
    version=version,
    install_requires=[
        'odoo9-addon-website_anchor_smooth_scroll',
        'odoo9-addon-website_blog_excerpt_img',
        'odoo9-addon-website_blog_mgmt',
        'odoo9-addon-website_blog_share',
        'odoo9-addon-website_breadcrumb',
        'odoo9-addon-website_canonical_url',
        'odoo9-addon-website_container_fluid',
        'odoo9-addon-website_cookie_notice',
        'odoo9-addon-website_crm_privacy_policy',
        'odoo9-addon-website_crm_quick_answer',
        'odoo9-addon-website_crm_recaptcha',
        'odoo9-addon-website_field_autocomplete',
        'odoo9-addon-website_form_metadata',
        'odoo9-addon-website_form_recaptcha',
        'odoo9-addon-website_forum_censored',
        'odoo9-addon-website_google_tag_manager',
        'odoo9-addon-website_img_bg_style',
        'odoo9-addon-website_legal_page',
        'odoo9-addon-website_logo',
        'odoo9-addon-website_no_crawler',
        'odoo9-addon-website_odoo_debranding',
        'odoo9-addon-website_payment_v10',
        'odoo9-addon-website_portal_address',
        'odoo9-addon-website_portal_contact',
        'odoo9-addon-website_portal_purchase',
        'odoo9-addon-website_portal_sale_v10',
        'odoo9-addon-website_portal_v10',
        'odoo9-addon-website_seo_redirection',
        'odoo9-addon-website_snippet_anchor',
        'odoo9-addon-website_snippet_big_button',
        'odoo9-addon-website_snippet_country_dropdown',
        'odoo9-addon-website_snippet_marginless_gallery',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
