/** @odoo-module **/

import options from "@web_editor/js/editor/snippets.options";
import {renderToElement} from "@web/core/utils/render";

options.registry.WebsiteFormEditor.include({
    willStart: async function () {
        var res = this._super(...arguments);
        this.recaptcha_site_key = await this.orm.call(
            "website",
            "get_recaptcha_v2_site_key"
        );
        return res;
    },
    toggleRecaptchaV2: async function () {
        const recaptchaV2 = this.$target[0].querySelector(
            ".s_website_form_recaptcha_v2"
        );
        if (recaptchaV2) {
            recaptchaV2.remove();
        } else {
            const legal = renderToElement("website_recaptcha_v2_form.recaptcha_v2", {
                recaptcha_site_key: this.recaptcha_site_key,
            });
            this.$target.find(".s_website_form_submit").before(legal);
        }
    },
    _computeWidgetState: function (methodName, params) {
        switch (methodName) {
            case "toggleRecaptchaV2":
                return (
                    !this.$target[0].querySelector(".s_website_form_recaptcha_v2") || ""
                );
        }
        return this._super(methodName, params);
    },
});
