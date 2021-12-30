/* Copyright 2015-2017 Tecnativa - Jairo Llopis <jairo.llopis@tecnativa.com>
 * Copyright 2019 Tecnativa - Cristina Martin R.
 * Copyright 2020 Tecnativa - Alexandre D. Díaz
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html). */

odoo.define("website_snippet_marginless_gallery.tour", function(require) {
    "use strict";
    const core = require("web.core");
    const tour = require("web_tour.tour");
    const base = require("web_editor.base");

    const _t = core._t;

    tour.register(
        "marginless_gallery",
        {
            url: "/",
            wait_for: base.ready(),
        },
        [
            {
                trigger: "a[data-action=edit]",
                content: _t("<b>Click Edit</b> to start designing your homepage."),
                extra_trigger: ".homepage",
                position: "bottom",
            },
            {
                trigger: "#snippet_feature .oe_snippet:contains('Marginless Gallery')",
                content: _t("Drag <i>Marginless Gallery</i> and drop it on the page."),
                position: "bottom",
                run: "drag_and_drop #wrap",
            },
        ]
    );
});
