/* Copyright 2015-2016 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html). */

odoo.define("website_snippet_big_button", function (require) {
    'use strict';

    var animation = require("web_editor.snippets.animation");

    animation.registry.big_button = animation.Class.extend({
        selector: ".js_big_button",

        start: function(editable_mode) {
            if (!editable_mode) {
                this.$target.on("click", $.proxy(this.on_click, this));
            }
        },

        /**
         * Make the whole button element be clickable. It would have been much
         * easier to make the button an <a/> tag, but website editor would
         * break the layout, so this hack is needed.
         */
        on_click: function (event) {
            $(event.currentTarget).find("a")[0].click();
        },
    });
});
