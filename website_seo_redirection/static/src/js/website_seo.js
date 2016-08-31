/* © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */
(function () {
    "use strict";
    var website = openerp.website;
    website.add_template_file(
        '/website_seo_redirection/static/src/xml/website_seo.xml');

    website.seo.Configurator.include({
        start: function () {
            this.$seo_redirection = this.$el.find(
                "#js_website_seo_redirection");
            this.$seo_redirection.val(
                document.location.pathname
            );
            return this._super();
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
            return website.session.model("website.seo.redirection").call(
                "smart_add",
                [document.location.pathname, newurl, website.get_context()]
            );
        },
        redirect_if_required: function (result) {
            if (result != "no-reload") {
                document.location =
                    this.$seo_redirection.val() + document.location.search;
            }
        },
    });
})();
