/* Copyright 2017 LasLabs Inc.
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */
odoo.define('website_blog_category.tour', function (require) {
    'use strict';

    var tour = require('web_tour.tour');
    var base = require('web_editor.base');

    tour.register(
        "website_blog_category",
        {
            url: "/blog/our-blog-1",
            name: "Test category browsing functionality",
            test: true,
            wait_for: base.ready(),
        },
        [
            {
                content: "Open Customize Menu",
                trigger: '#customize-menu-button',
            },
            {
                content: "Enable Categories Display",
                trigger: "#customize-menu a:contains(Categories)",
            },
            {
                content: "Click CMS Category",
                trigger: ".website_blog_categories li a:contains(CMS)",
            },
            {
                content: "Link is Active",
                trigger: ".website_blog_categories li a:contains(CMS)",
            },
            {
                content: "Correct Post is Shown",
                trigger: "a h2:contains(Integrating your CMS and E-Commerce)",
            },
        ]
    );

    return {};

});
