odoo.define([], function () {
    "use strict";
    window.callback_success_recaptcha = function () {
        console.info("success_token");
    };

    window.callback_expired_recaptcha = function () {
        window.location.reload();
    };
});
