import {Interaction} from "@web/public/interaction";
import {altchaInteractionFunctionality} from "@website_altcha/altcha.esm";
import {patch} from "@web/core/utils/patch";
import {registry} from "@web/core/registry";

export class GenericAltcha extends Interaction {
    static selector = "form.website_altcha_form, form.js_website_submit_form";
}

patch(
    GenericAltcha.prototype,
    altchaInteractionFunctionality({
        altcha_prepend_to:
            "*:has(> input[type='submit']), *:has(> button[type='submit'])",
    })
);

registry.category("public.interactions").add("website_altcha.generic", GenericAltcha);
