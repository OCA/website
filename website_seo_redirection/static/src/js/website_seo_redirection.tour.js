/* © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */
odoo.define('website_seo_redirection.tour', function(require) {
    'use strict';

    var Tour = require('web.Tour');

    Tour.register({
        id: "website_seo_redirection",
        name: "Check SEO redirections functionality",
        path: "/",
        mode: "test",
        steps: [
            {
                title: "Open SEO menu",
                waitFor: "a:contains('SEO Sample')",
                element: "a:contains('SEO Sample')",
            },
            {
                title: "Go to SEO sample page in original URL",
                waitFor: "a:contains('Original URL')",
                element: "a:contains('Original URL')",
            },
            {
                title: "Page reached, back to home",
                waitFor: "#origin,#destination",
                element: "a:contains('Home')",
            },
            {
                title: "Open SEO menu",
                waitFor: "meta[property='og:title'][content='Homepage']",
                element: "a:contains('SEO Sample')",
            },
            {
                title: "Go to SEO sample page in destination URL",
                waitFor: "a:contains('Redirected URL')",
                element: "a:contains('Redirected URL')",
            },
            {
                title: "Page reached",
                waitFor: "#origin,#destination",
            },
        ],
    });
});
