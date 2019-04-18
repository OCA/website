/* Copyright 2015-2019 Tecnativa - Jairo Llopis <jairo.llopis@tecnativa.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html). */

odoo.define("website_snippet_anchor.anchor_option", function (require) {
    "use strict";
    var core = require("web.core");
    var options = require("web_editor.snippets.options");
    var utils = require("website.utils");
    var sprintf = _.str.sprintf;
    var _t = core._t;

    /**
     * Option to have anchors in snippets
     */
    options.registry.anchor = options.Class.extend({

        /**
         * Let user choose anchor name
         *
         * @param {String} window_title
         *
         * @returns {jQuery.Deferred}
         * Resolves when the dialog is open and ready to accept input.
         */
        anchor_ask: function (window_title) {
            // Ask the anchor to the user
            return utils.prompt({
                "window_title": window_title || _t("Choose anchor"),
                "input": _t("Anchor"),
                "default": this.$target.attr("id"),
            }).done(this.anchor_update.bind(this));
        },

        /**
         * Indicates if this is a valid anchor
         *
         * @param {String} anchor
         * Anchor string to be validated
         *
         * @returns {Boolean}
         */
        anchor_valid: function (anchor) {
            return (/^[\w-]+$/).test(anchor) &&
                !$(sprintf("#%s", anchor)).not(this.$target).length;
        },

        /**
         * Update an anchor and all its dependencies.
         *
         * @param {String} new_anchor
         * The new anchor string, or an empty string if you're removing it.
         *
         * @param {jQuery} $input
         * The element where the anchor was chosen.
         *
         * @param {jQuery} $dialog
         * The dialog where you asked for a new anchor.
         *
         * @returns {undefined/jQuery.Deferred}
         * The deferred is returned with a new dialog, in case the update fails
         * and a new achor has to be asked to the user.
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

    return {
        Option: options.registry.anchor,
    };
});
