/* © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */
(function ($) {
    "use strict";
    openerp.Tour.register({
        id: "website_seo_redirection",
        name: "Check SEO redirections functionality",
        path: "/",
        mode: "test",
        steps: [
            {
                title: "Open SEO menu",
                waitFor: "a>span:contains('SEO Sample')",
                element: "a>span:contains('SEO Sample')",
            },
            {
                title: "Go to SEO sample page in original URL",
                waitFor: "a>span:contains('Original URL')",
                element: "a>span:contains('Original URL')",
            },
            {
                title: "Page reached, back to home",
                waitFor: "#origin,#destination",
                element: "a>span:contains('Home')",
            },
            {
                title: "Open SEO menu",
                waitFor: "html[data-view-xmlid='website.homepage']",
                element: "a>span:contains('SEO Sample')",
            },
            {
                title: "Go to SEO sample page in destination URL",
                waitFor: "a>span:contains('Redirected URL')",
                element: "a>span:contains('Redirected URL')",
            },
            {
                title: "Page reached",
                waitFor: "#origin,#destination",
            },
        ],
    });
})(jQuery);
