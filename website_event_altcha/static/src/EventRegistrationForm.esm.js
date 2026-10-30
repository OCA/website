/* Copyright 2026 Hunki Enterprises BV */
import {ModalRegistration} from "@website_event/interactions/modal_registration";
import {loadBundle} from "@web/core/assets";
import {patch} from "@web/core/utils/patch";
import {session} from "@web/session";

patch(ModalRegistration.prototype, {
    setup() {
        super.setup();
        this.altchaEnabled = Boolean(session.altcha_public_key);
    },

    async willStart() {
        await super.willStart(...arguments);
        if (this.altchaEnabled) {
            await loadBundle("web.altcha_libs");
        }
    },

    start() {
        super.start();
        if (!this.altchaEnabled) {
            return;
        }
        const footer = this.el.querySelector("form div.modal-footer");
        const button = this.el.querySelector("form button[type='submit']");
        if (!footer || !button) {
            return;
        }
        if (!this.el.querySelector("altcha-widget")) {
            this.renderAt("website_altcha.AltchaWidget", {}, footer, "afterbegin");
        }
        const altchaWidget = this.el.querySelector("altcha-widget");
        const updateButton = (state) => {
            button.disabled = state !== "verified";
        };
        updateButton(altchaWidget.getState?.());
        this.addListener(altchaWidget, "statechange", (ev) =>
            updateButton(ev.detail.state)
        );
        this.addListener(altchaWidget, "load", () =>
            updateButton(altchaWidget.getState?.())
        );
    },
});
