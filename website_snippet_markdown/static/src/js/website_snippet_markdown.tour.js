odoo.define("website_snippet_markdown.tour", function (require) {
   "use strict";

    var tour = require("web_tour.tour");
    var base = require("web_editor.base");

    var options = {
        url: "/",
        test: true,
        wait_for: base.ready()
    };

    var steps = [
        {
            trigger: "#oe_main_menu_navbar a[data-action=edit]"
        }
    ];

    tour.register("website_snippet_markdown.tour", options, steps);
});