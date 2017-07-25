/* Copyright 2015-2017 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html). */

odoo.define("web_module_name.tour", function (require) {
    "use strict";
    var base = require("web_editor.base");
    var Tour = require("web.Tour");

    return base.ready().done($.proxy(Tour, "register", {
        id: "marginless_gallery",
        name: "Insert a marginless gallery snippet",
        path: "/",
        mode: "test",
        steps: [
            {
                title: "Edit the homepage (1)",
                waitFor: "button[data-action=edit]",
                element: "button[data-action=edit]",
            },
            {
                title: "Drag and drop a marginless gallery snippet (1)",
                waitFor: ".oe_snippet:contains('Marginless Gallery'):visible",
                snippet: ".oe_snippet:contains('Marginless Gallery')",
            },
            {
                title: "Cancel modal dialog",
                waitFor: ".modal button:contains('Cancel'):visible",
                element: ".modal button:contains('Cancel'):visible",
            },
            {
                title: "Drag and drop a marginless gallery snippet (2)",
                waitFor: ".oe_snippet:contains('Marginless Gallery'):visible",
                snippet: ".oe_snippet:contains('Marginless Gallery')",
            },
            {
                title: "Set no fixed height",
                waitFor: ".modal .btn-primary:visible",
                element: ".modal .btn-primary:visible",
            },
            {
                title: "Click on the snippet to see options",
                waitNot: ".modal:visible",
                element: "#wrap .marginless-gallery",
            },
            {
                title: "Click on Customize",
                waitFor: "#wrap .marginless-gallery, \
                          .btn-primary:contains('Customize'):visible",
                element: ".btn-primary:contains('Customize'):visible",
            },
            {
                title: "Click on Change Images Height",
                element: "li[data-change_images_height]:visible a",
            },
            {
                title: "Set image height of 200px",
                waitFor: ".modal-body input:visible",
                element: ".modal-body input:visible",
                sampleText: "200",
            },
            {
                title: "Accept modal dialog",
                waitFor: ".modal input:contains('200'):visible",
                element: ".modal .btn-primary:visible",
            },
            {
                title: "Check that the right height has been saved",
                waitNot: ".modal:visible",
                waitFor: "#wrap .marginless-gallery \
                          .col-md-3[style*='height: 200px']",
            },
        ],
    }));
});
