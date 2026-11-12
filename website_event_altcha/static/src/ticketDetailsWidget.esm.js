/* Copyright 2026 Hunki Enterprises BV */
import {ModalRegistration} from "@website_event/js/interactions/modal_registration";
import {altchaInteractionFunctionality} from "@website_altcha/altcha.esm";
import {patch} from "@web/core/utils/patch";

patch(
    ModalRegistration.prototype,
    altchaInteractionFunctionality({
        altcha_prepend_to: "form div.modal-footer",
    })
);

patch(ModalRegistration.prototype, {
    start() {
        super.start();
        const altchaWidget = this.el.querySelector("altcha-widget");
        const button = this.el.querySelector("form button[type='submit']");
        if (!altchaWidget || !button) {
            return;
        }
        const updateButton = (state) => {
            button.disabled = state !== "verified";
        };
        updateButton(altchaWidget.getState?.());
        this.addListener(altchaWidget, "statechange", (ev) =>
            updateButton(ev.detail.state)
        );
    },
});
