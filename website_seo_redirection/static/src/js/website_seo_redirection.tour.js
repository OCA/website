/* © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */
odoo.define('website_seo_redirection.tour', function (require) {
    'use strict';

    var tour = require('web_tour.tour');
    var base = require('web_editor.base');

    tour.register(
        "website_seo_redirection",
        {
            url: "/",
            name: "Check SEO redirections functionality",
            test: true,
            wait_for: base.ready(),
        },
        [
            {
                content: "Open SEO menu",
                trigger: "a:contains('SEO Sample')",
            },
            {
                content: "Go to SEO sample page in original URL",
                trigger: "a:contains('Original URL')",
            },
            {
                content: "Page reached, back to home",
                extra_trigger: "#origin, #destination",
                trigger: "a:contains('Home')",
            },
            {
                content: "Open SEO menu",
                trigger: "a:contains('SEO Sample')",
            },
            {
                content: "Go to SEO sample page in destination URL",
                trigger: "a:contains('Redirected URL')",
            },
            {
                content: "Page reached",
                trigger: "#origin, #destination",
            },
        ]
    );

    return {};

});
