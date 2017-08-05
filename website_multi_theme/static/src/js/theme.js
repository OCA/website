/* Copyright 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */

odoo.define('website_multi_theme.theme', function(require){
    "use strict";

    var theme = require('website.theme');

    // Know if a multi website theme is enabled
    function multi_theme_links () {
        return $("link[href*='website_multi_theme.auto']");
    }

    theme.include({
        update_style: function (enable, disable, reload) {
            var links = multi_theme_links();
            if (links.length) {
                // Placeholder for dynamically-loaded assets upstream
                links.last().after(
                    $("<link rel='fake' href='/web.assets_frontend.fake'/>")
                );
            }
            return this._super.apply(this, arguments).done(function () {
                links.remove();
            });
        }
    });

    return {
        multi_theme_links: multi_theme_links,
    }
});
