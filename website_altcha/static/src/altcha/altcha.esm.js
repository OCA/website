/** @odoo-module **/

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
                Boolean(document.querySelector(".o_altcha_widget"))
            );
        }
        return false;
    }
}
