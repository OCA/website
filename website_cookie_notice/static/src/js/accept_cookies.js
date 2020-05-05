/* © 2015 Antiun Ingeniería, S.L.
 * © 2015 Lorenzo Battistini - Agile Business Group
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

odoo.define("website_cookie_notice.cookie_notice", function(require) {
    "use strict";

    var ajax = require("web.ajax");
    require("web.dom_ready");

    $(".cc-cookies .btn-primary").click(function(e) {
        e.preventDefault();
        ajax.jsonRpc("/website_cookie_notice/ok", "call").then(function(data) {
            if (data.result === "ok") {
                $(e.target)
                    .closest(".cc-cookies")
                    .hide("fast");
            }
        });
    });
});
