// Copyright 2020 Odoo
// Copyright 2020 Tecnativa - Alexandre Díaz
// License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).
odoo.define("website_megamenu.rte", function (require) {
    "use strict";

    var rte = require("web_editor.rte");

    rte.Class.include({
        /**
         * @override
         */
        _saveElement: function ($el) {
            var self = this;
            var viewID = $el.data("oe-id");
            if (!viewID) {
                return Promise.resolve();
            }
            return this._super.apply(this, arguments).then(function () {
                if ($el.data("oe-field") === "mega_menu_content") {
                    var classes = _.without(
                        $el.attr("class").split(" "),
                        "dropdown-menu",
                        "o_mega_menu",
                        "show",
                        "oe_structure"
                    );
                    return self._rpc({
                        model: "website.menu",
                        method: "write",
                        args: [
                            [Number($el.data("oe-id"))],
                            {
                                mega_menu_classes: classes.join(" "),
                            },
                        ],
                    });
                }
            });
        },
    });
});
