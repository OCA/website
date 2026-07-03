import {AltchaLegacyClassFunctionality} from "@website_altcha/altcha.esm";
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.GenericAltcha = publicWidget.Widget.extend({
    ...AltchaLegacyClassFunctionality,
    selector: "form.website_altcha_form, form.js_website_submit_form",
    altcha_prepend_to:
        "*:has( > input[type='submit']), *:has( > button[type='submit'])",
});
