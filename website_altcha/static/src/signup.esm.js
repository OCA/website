import {Interaction} from "@web/public/interaction";
import {altchaInteractionFunctionality} from "@website_altcha/altcha.esm";
import {patch} from "@web/core/utils/patch";
import {registry} from "@web/core/registry";

export class SignupAltcha extends Interaction {
    static selector = ".oe_signup_form, .oe_reset_password_form";
}

patch(SignupAltcha.prototype, altchaInteractionFunctionality());

registry.category("public.interactions").add("website_altcha.signup", SignupAltcha);
