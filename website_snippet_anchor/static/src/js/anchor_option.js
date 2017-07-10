/* Copyright 2015, 2017 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html). */

"use strict";
odoo.define("website_snippet_anchor.anchor_option", function (require) {
    var core = require("web.core"),
        options = require("web_editor.snippets.options"),
        website = require("website.website"),
        sprintf = _.str.sprintf,
        _t = core._t;

    // Option to have anchors in snippets
    options.registry.anchor = options.Class.extend({
        // Let user choose anchor name
        anchor_ask: function (type, window_title) {
            // Only react on clicks, not on resets or other events
            if (type != "click") {
                return $.Deferred().reject();
            }
            // Ask the anchor to the user
            return website.prompt({
                "window_title": window_title || _t("Choose anchor"),
                "input": _t("Anchor"),
                "default": this.$target.attr("id"),
            }).done($.proxy(this.anchor_update, this));
        },

        /**
         * Return an array of anchors except the one found in `except`.
         */
        current_anchors: function (except) {
            var anchors = Array();
            $("[id]").not(except).each(function () {
                anchors.push($(this).attr("id"));
            });
            return anchors;
        },

        /**
         * Indicates if this is a valid anchor
         */
        anchor_valid: function (anchor) {
            return /^[\w-]+$/.test(anchor) &&
                !$(sprintf("#%s", anchor)).not(this.$target).length;
        },

        /**
         * Update an anchor and all its dependencies.
         */
        anchor_update: function (new_anchor, $input, $dialog) {
            // Remove current anchor if any falsey value came in
            if (!new_anchor) {
                this.$target.removeAttr("id");
                return;
            }
            // Re-ask if invalid anchor
            if (!this.anchor_valid(new_anchor)) {
                $dialog.modal("hide");
                return this.anchor_ask(
                    "click",
                    sprintf(
                        _t("Anchor '%s' already exists or is not valid"),
                        new_anchor
                    )
                );
            }
            // Update all elements that point to current anchor
            var old_anchor = this.$target.attr("id");
            if (old_anchor) {
                $(sprintf('[href="#%s"]', old_anchor))
                .attr("href", sprintf("#%s", new_anchor));
            }
            // Set new anchor on curret target
            this.$target.attr("id", new_anchor);
        },
    });
});
