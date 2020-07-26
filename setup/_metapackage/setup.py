import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo12-addons-oca-website",
    description="Meta package for oca-website Odoo addons",
    version=version,
    install_requires=[
        'odoo12-addon-website_adv_image_optimization',
        'odoo12-addon-website_anchor_smooth_scroll',
        'odoo12-addon-website_blog_excerpt_img',
        'odoo12-addon-website_breadcrumb',
        'odoo12-addon-website_canonical_url',
        'odoo12-addon-website_cookie_notice',
        'odoo12-addon-website_crm_privacy_policy',
        'odoo12-addon-website_crm_quick_answer',
        'odoo12-addon-website_crm_recaptcha',
        'odoo12-addon-website_form_builder',
        'odoo12-addon-website_form_recaptcha',
        'odoo12-addon-website_google_tag_manager',
        'odoo12-addon-website_img_dimension',
        'odoo12-addon-website_js_below_the_fold',
        'odoo12-addon-website_js_below_the_fold_payment',
        'odoo12-addon-website_lazy_load_image',
        'odoo12-addon-website_legal_page',
        'odoo12-addon-website_logo',
        'odoo12-addon-website_media_size',
        'odoo12-addon-website_megamenu',
        'odoo12-addon-website_no_crawler',
        'odoo12-addon-website_odoo_debranding',
        'odoo12-addon-website_snippet_anchor',
        'odoo12-addon-website_snippet_big_button',
        'odoo12-addon-website_snippet_country_dropdown',
        'odoo12-addon-website_snippet_marginless_gallery',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
    ]
)
