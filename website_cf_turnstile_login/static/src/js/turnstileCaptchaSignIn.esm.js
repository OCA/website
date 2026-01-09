/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import {turnStile} from "@website_cf_turnstile/js/turnstile";
import {session} from "@web/session";

const signinTurnStile = {
    ...turnStile,

    async willStart() {
        this._super(...arguments);
        if (!session.turnstile_site_key) {
            return;
        }
        const button = this.el.querySelector('button[type="submit"]');
        this.addSpinner(button);
        this.cleanTurnstile();
        const turnstileNodes = this.addTurnstile(this.action);
        turnstileNodes?.insertBefore(button);
        this.renderTurnstile(turnstileNodes);
    },
};

publicWidget.registry.turnstileCaptchaSignin = publicWidget.Widget.extend({
    ...signinTurnStile,
    selector: ".oe_login_form",
    action: "signin",
});

export default signinTurnStile;
