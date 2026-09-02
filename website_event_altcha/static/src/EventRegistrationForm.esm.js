/* Copyright 2026 Hunki Enterprises BV */
import {AltchaLegacyClassFunctionality} from "@website_altcha/altcha.esm";
import EventRegistrationForm from "@website_event/js/website_event";

EventRegistrationForm.include({
    ...AltchaLegacyClassFunctionality,
});

EventRegistrationForm.include({
    altcha_prepend_to: "div.modal-footer",
    start() {
        const result = this._super(...arguments);
        const altcha_widget = this.el.querySelector("altcha-widget");
        if (altcha_widget) {
            const button = this.el.querySelector("button.btn-primary");
            altcha_widget.addEventListener("statechange", (ev) => {
                button.disabled = ev.detail.state !== "verified";
            });
            altcha_widget.addEventListener("load", () => {
                button.disabled = altcha_widget.getState() !== "verified";
            });
        }
        return result;
    },
    _addTurnstile(form) {
        const altcha_widget = this.el.querySelector("altcha-widget");
        if (altcha_widget) {
            form.querySelector("div.modal-footer").prepend(altcha_widget);
        }
        this._super(...arguments);
    },
});
