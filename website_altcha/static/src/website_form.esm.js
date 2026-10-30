import {Form} from "@website/snippets/s_website_form/form";
import {altchaInteractionFunctionality} from "@website_altcha/altcha.esm";
import {patch} from "@web/core/utils/patch";

patch(
    Form.prototype,
    altchaInteractionFunctionality({
        altcha_before: ".s_website_form_submit",
        altcha_should_insert() {
            return !this.el.classList.contains("s_website_form_no_recaptcha");
        },
    })
);
