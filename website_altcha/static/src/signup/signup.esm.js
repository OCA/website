import "@website/snippets/s_website_form/000";
import {Altcha} from "@website_altcha/altcha/altcha.esm";
import publicWidget from "@web/legacy/js/public/public_widget";
import {renderToString} from "@web/core/utils/render";

export const AltchaFunctionality = {
    init() {
        this._super(...arguments);
        this._altcha = new Altcha();
    },

    async willStart() {
        this._altcha.loadLibs();
        return this._super(...arguments);
    },
    start: function () {
        if (this._altcha._publicKey && !this.$el.find(".o_altcha_widget").length) {
            this.$el
                .find("div.oe_login_buttons")
                .prepend(renderToString("website_altcha.AltchaWidget", {}));
        }
        return this._super(...arguments);
    },
};

publicWidget.registry.SignupAltcha = publicWidget.Widget.extend({
    ...AltchaFunctionality,
    selector: ".oe_signup_form",
});

publicWidget.registry.ResetPasswordAltcha = publicWidget.Widget.extend({
    ...AltchaFunctionality,
    selector: ".oe_reset_password_form",
});

publicWidget.registry.s_website_form.include({
    init() {
        this._super(...arguments);
        this._altcha = new Altcha();
    },

    async willStart() {
        this._altcha.loadLibs();
        return this._super(...arguments);
    },

    /**
     * @override
     */
    start: function () {
        const res = this._super(...arguments);
        if (this.$target[0].classList.contains("s_website_form_no_recaptcha")) {
            return res;
        }
        if (this._altcha._publicKey) {
            this.$el
                .find(".s_website_form_submit")
                .before(renderToString("website_altcha.AltchaWidget", {}));
        }
        return res;
    },
});
publicWidget.registry.EditModeWebsiteForm.include({
    start: function () {
        const res = this._super(...arguments);
        if (this.editableMode) {
            // We should delete the altcha widget in edit mode
            this.$el.find(".o_altcha_widget").remove();
            this.$el.find(".o_altcha_widget_container").remove();
        }
        return res;
    },
});
