odoo.define("website_recaptcha_v2_form.form_editor", function (require) {
    "use strict";

    var options = require("web_editor.snippets.options");
    const core = require("web.core");
    const rpc = require("web.rpc");
    const qweb = core.qweb;
    require("website.form_editor");

    options.registry.WebsiteFormEditor.include({
        willStart: async function () {
            var res = this._super(...arguments);
            this.recaptcha_site_key = await rpc.query({
                model: "website",
                method: "get_recaptcha_v2_site_key",
            });
            return res;
        },
        toggleRecaptchaV2: async function () {
            const recaptchaV2 = this.$target[0].querySelector(
                ".s_website_form_recaptcha_v2"
            );
            if (recaptchaV2) {
                recaptchaV2.remove();
            } else {
                const legal = qweb.render("website_recaptcha_v2_form.recaptcha_v2", {
                    recaptcha_site_key: this.recaptcha_site_key,
                });
                this.$target.find(".s_website_form_submit").before(legal);
            }
        },
        _computeWidgetState: function (methodName, params) {
            switch (methodName) {
                case "toggleRecaptchaV2":
                    return (
                        !this.$target[0].querySelector(
                            ".s_website_form_recaptcha_v2"
                        ) || ""
                    );
            }
            return this._super(methodName, params);
        },
    });
});
