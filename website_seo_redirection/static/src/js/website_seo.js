/* © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */
odoo.define('website_seo_redirection.website_seo', function (require) {
    "use strict";
    var ajax = require("web.ajax");
    var base = require("web_editor.base");
    var core = require("web.core");
    var Model = require('web.Model');
    var seo = require("website.seo");

    ajax.loadXML(
        '/website_seo_redirection/static/src/xml/website_seo.xml',
        core.qweb
    );

    seo.Configurator.include({
        start: function () {
            this._super();
            this.$seo_redirection = this.$el.find(
                "#js_website_seo_redirection");
            this.$seo_redirection.val(
                document.location.pathname
            );
        },
        saveMetaData: function (data) {
            return $.when(this.update_seo_redirection(), this._super(data))
                .done($.proxy(this.redirect_if_required, this));
        },
        update_seo_redirection: function () {
            var newurl = this.$seo_redirection.val();
            if (newurl === document.location.pathname) {
                return $.Deferred().resolve("no-reload");
            }
            return new Model("website.seo.redirection").call(
                "smart_add",
                [document.location.pathname, newurl, base.get_context()]
            );
        },
        redirect_if_required: function (result) {
            if (result !== "no-reload") {
                document.location =
                    this.$seo_redirection.val() + document.location.search;
            }
        },
    });
});
