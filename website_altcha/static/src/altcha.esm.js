import {loadBundle} from "@web/core/assets";
import {renderToString} from "@web/core/utils/render";
import {session} from "@web/session";

const ALTCHA_POSITIONS = [
    ["altcha_before", "beforebegin"],
    ["altcha_after", "afterend"],
    ["altcha_append_to", "beforeend"],
    ["altcha_prepend_to", "afterbegin"],
];

export const AltchaBaseFunctionality = {
    altcha_prepend_to: "div.oe_login_buttons",
    altcha_append_to: false,
    altcha_before: false,
    altcha_after: false,
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
    /**
     * Hook to skip the insertion on specific elements.
     *
     * @returns {Boolean}
     */
    altcha_should_insert() {
        return true;
    },

    altcha_insert_widget() {
        if (
            !this.altcha_enabled ||
            !this.altcha_should_insert() ||
            this.el.querySelector("altcha-widget")
        ) {
            return;
        }
        for (const [prop, position] of ALTCHA_POSITIONS) {
            if (this[prop]) {
                this.el
                    .querySelector(this[prop])
                    ?.insertAdjacentHTML(
                        position,
                        renderToString("website_altcha.AltchaWidget", {})
                    );
                return;
            }
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

/**
 * Patch for Interactions. Returns a new object on every call because
 * patch() cannot reuse the same object on several prototypes (it would
 * break `super`).
 *
 * @param {Object} [config] altcha_* properties or method overrides
 * @returns {Object}
 */
export function altchaInteractionFunctionality(config = {}) {
    return {
        ...AltchaBaseFunctionality,
        ...config,
        setup() {
            super.setup();
            this.altcha_init();
        },
        async willStart() {
            await super.willStart(...arguments);
            await this.altcha_load_libs();
        },
        start() {
            super.start();
            this.altcha_insert_widget();
            this.registerCleanup(() =>
                this.el.querySelector("altcha-widget")?.remove()
            );
        },
    };
}
