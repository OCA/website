/* Copyright 2026 Nitrokey GmbH */
import "@website_mass_mailing/js/website_mass_mailing";
import {AltchaLegacyClassFunctionality} from "@website_altcha/altcha.esm";
import publicWidget from "@web/legacy/js/public/public_widget";
import {rpcBus} from "@web/core/network/rpc";

const SUBSCRIBE_ROUTE = "/website_mass_mailing/subscribe";

publicWidget.registry.subscribe.include({
    ...AltchaLegacyClassFunctionality,
    // Append after the email input, that one must stay the snippet's first input
    altcha_prepend_to: false,
    altcha_append_to: ".js_subscribe_wrap",
});

publicWidget.registry.subscribe.include({
    // Skip edit mode where the widget would end up being saved
    altcha_insert_widget() {
        if (!this.editableMode) {
            this._super(...arguments);
        }
    },

    // The subscription is an rpc call, so the payload cannot travel as a form
    // field: solve the challenge and inject it into the request's parameters
    async _onSubscribeClick() {
        // Capture the super method, it is only bound until the first await
        const _super = this._super.bind(this);
        const widget = this.el.querySelector("altcha-widget");
        if (!widget) {
            return _super(...arguments);
        }
        await this._altchaReady;
        const payload =
            widget.getState?.() === "verified"
                ? widget.querySelector('input[name="altcha"]')?.value
                : (await widget.verify?.())?.payload;
        // The event is fired synchronously before the request is serialized
        const injectPayload = ({detail}) => {
            if (detail.url === SUBSCRIBE_ROUTE) {
                detail.data.params.altcha = payload;
            }
        };
        rpcBus.addEventListener("RPC:REQUEST", injectPayload);
        try {
            return await _super(...arguments);
        } finally {
            rpcBus.removeEventListener("RPC:REQUEST", injectPayload);
        }
    },
});
