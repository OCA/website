/* global document */
import publicWidget from "@web/legacy/js/public/public_widget";
import {Component} from "@odoo/owl";

publicWidget.registry.SubmitButton = publicWidget.Widget.extend({
    selector: ".s_website_form_send", // Updated selector

    async start() {
        await this._super(...arguments);
        this.SubmitButton = this.el;
        const legalDiv = document.querySelector(".s_website_form_legal");
        if (legalDiv) {
            this._disable();
        } else {
            this._enable();
        }
        Component.env.bus.addEventListener(
            "enableSubmitButton",
            this._enable.bind(this)
        );
        Component.env.bus.addEventListener(
            "disableSubmitButton",
            this._disable.bind(this)
        );
    },

    _enable() {
        this.SubmitButton.classList.remove("disabled");
    },

    _disable() {
        this.SubmitButton.classList.add("disabled");
    },
});
export default publicWidget.registry.PaymentButton;
