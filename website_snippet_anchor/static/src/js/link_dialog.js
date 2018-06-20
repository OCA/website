/* Copyright 2015, 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html). */

"use strict";
odoo.define("website_snippet_anchor.link_dialog", function (require) {
    var core = require("web.core");
    var widget = require("web_editor.widget");

    // Load QWeb js snippets
    core.qweb.add_template(
        "/website_snippet_anchor/static/src/xml/link_dialog.xml");

    // Add anchor to link dialog
    widget.LinkDialog.include({
        /**
         * Allow the user to use only an anchor.
         */
        get_data: function (test) {
            var $anchor = this.$("#anchor");

            if (test !== false && $anchor.val()) {
                var $e = this.$('.active input.url-source');
                if (!$e.length) {
                    $e = this.$('input.url-source:first');
                }
                var val = $e.val();
                var isNewWindow = this.$('input.window-new').prop('checked');
                var label = this.$('#o_link_dialog_label_input').val() || val;
                var style = this.$("input[name='link-style-type']:checked").val() || '';
                var size = this.$("select.link-style").val() || '';
                var classes = (this.data.className || "") + (style && style.length ? " btn " : "") + style + " " + size;

                return $.Deferred().resolve($e.val() + '#' + $anchor.val(), isNewWindow, label, classes);
            } else {
                return this._super.apply(this, arguments);
            }
        },

        /**
         * Put data in its corresponding place in the link dialog.
         *
         * When user edits an existing link that contains an anchor, put it
         * in its dedicated field.
         */
        bind_data: function () {
            var url = this.data.url || "",
                url_parts = url.split("#", 2);
            if (url_parts.length > 1) {
                this.data.url = url_parts[0];
                this.$("#anchor").val(url_parts[1]);
            }
            return this._super.apply(this, arguments);
        },
    });
});
