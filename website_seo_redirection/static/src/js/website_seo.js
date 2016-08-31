/* © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */
(function () {
    "use strict";

    var website = openerp.website;
    website.add_template_file(
        '/website_seo_redirection/static/src/xml/website_seo.xml');

    website.seo.Configurator.include({
        start: function () {
            this.$el.find(".js_website_seo_redirection").val(
                document.location.pathname
            );
        },
    });
})();
