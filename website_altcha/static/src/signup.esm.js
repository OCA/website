import {AltchaLegacyClassFunctionality} from "./altcha.esm";
import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.SignupAltcha = publicWidget.Widget.extend({
    ...AltchaLegacyClassFunctionality,
    selector: ".oe_signup_form",
});

publicWidget.registry.ResetPasswordAltcha = publicWidget.Widget.extend({
    ...AltchaLegacyClassFunctionality,
    selector: ".oe_reset_password_form",
});
