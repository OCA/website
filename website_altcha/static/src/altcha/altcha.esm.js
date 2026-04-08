/* global document, window */

import {_t} from "@web/core/l10n/translation";
import {loadBundle} from "@web/core/assets";
import {session} from "@web/session";

export class Altcha {
    /**
     * @override
     */
    constructor() {
        this._publicKey = session.altcha_public_key;
    }
    /**
     * Loads the altcha libraries.
     *
     * @returns {Promise|Boolean} promise if libs are loading else false if the altcha key is empty.
     */
    loadLibs() {
        if (this._publicKey) {
            this._altchaReady = loadBundle(`web.altcha_libs`);
            return this._altchaReady.then(() =>
                Boolean(document.querySelector(".altcha-widget"))
            );
        }
        return false;
    }
    /**
     * Returns an object with the token if altcha call succeeds
     * If no key is set an object with a message is returned
     * If an error occurred an object with the error message is returned
     *
     * @param {String} action
     * @returns {Promise|Object}
     */
    async getToken(action) {
        if (!this._publicKey) {
            return {
                message: _t("No altcha site key set."),
            };
        }
        await this._altchaReady;
        try {
            return {
                token: await window.altcha.execute(this._publicKey, {action: action}),
            };
        } catch {
            return {
                error: _t("The altcha site key is invalid."),
            };
        }
    }
}
