import {loadBundle} from "@web/core/assets";
import {renderToString} from "@web/core/utils/render";
import {session} from "@web/session";

export const AltchaBaseFunctionality = {
    altcha_prepend_to: "div.oe_login_buttons",
    altcha_enabled: false,

    altcha_init() {
        this.altcha_enabled = Boolean(session.altcha_public_key);
    },

    /**
     * Loads the altcha libraries.
     *
     * @returns {Promise|Boolean} promise if libs are loading else false if the altcha key is empty.
     */
    async altcha_load_libs() {
        if (this.altcha_enabled) {
            this._altchaReady = loadBundle(`web.altcha_libs`);
            return this._altchaReady;
        }
        return false;
    },
    altcha_insert_widget() {
        if (this.altcha_enabled && !this.$el.find("altcha-widget").length) {
            this.$el
                .find(this.altcha_prepend_to)
                .prepend(renderToString("website_altcha.AltchaWidget", {}));
        }
    },
};

export const AltchaLegacyClassFunctionality = {
    ...AltchaBaseFunctionality,
    init() {
        this._super(...arguments);
        this.altcha_init();
    },

    async willStart() {
        this.altcha_load_libs();
        return this._super(...arguments);
    },
    start() {
        this.altcha_insert_widget();
        return this._super(...arguments);
    },
};
