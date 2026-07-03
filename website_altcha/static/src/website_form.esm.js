import "@website/snippets/s_website_form/000";
import {AltchaLegacyClassFunctionality} from "./altcha.esm";
import publicWidget from "@web/legacy/js/public/public_widget";
import {renderToString} from "@web/core/utils/render";

publicWidget.registry.s_website_form.include({
    ...AltchaLegacyClassFunctionality,
});
publicWidget.registry.s_website_form.include({
    altcha_insert_widget() {
        // Intentional no-op
    },
    start: function () {
        const res = this._super(...arguments);
        if (this.$target[0].classList.contains("s_website_form_no_recaptcha")) {
            return res;
        }
        if (this.altcha_enabled) {
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
