/* Copyright 2015-2016 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html). */

odoo.define('website_snippet_anchor.widgets', function (require) {
    "use strict";
    var ajax = require("web.ajax");
    var core = require("web.core");
    var options = require("web_editor.snippets.options");
    var website = require("website.website");
    var widget = require("web_editor.widget");
    var _t = core._t;

    // Templates
    ajax.loadXML(
        "/website_snippet_anchor/static/src/xml/website_snippet_anchor.xml",
        core.qweb
    );

    // Option to have anchors in snippets
    options.registry.anchor = options.Class.extend({
        // Ask anchor name.
        ask: function (type, value, $li) {
            if (type !== "click") return;
            return website.prompt({
                "window_title": value,
                "default": this.$target.attr("id") || "",
                "input": _t("Name"),
            })
            .done($.proxy(this.answer, this));
        },

        // Process user's answer
        answer: function (answer) {
            if (answer) {
                if (this.valid_anchor(answer)) {
                    return this.update_anchor(answer);
                } else {
                    return this.ask(
                        "click",
                        _.str.sprintf(
                            _t("Anchor %s already exists, choose another"),
                            answer
                        )
                    );
                }
            } else {
                this.$target.removeAttr("id");
            }
        },

        // Check if a given anchor is valid
        valid_anchor: function (anchor) {
            return !$("#" + anchor).not(this.$target[0]).length;
        },

        // Update an anchor and all its dependencies.
        update_anchor: function (new_anchor) {
            var old_anchor = this.$target.attr("id"),
                new_hashed = "#" + new_anchor,
                old_hashed = "#" + old_anchor;

            // Set new anchor
            this.$target.attr("id", new_anchor);

            // Fix other elements' attributes.
            $(".oe_editable [href='" + old_hashed + "']")
                .attr("href", new_hashed);
            $(".oe_editable [data-target='" + old_hashed + "']")
                .attr("data-target", new_hashed);
            $(".oe_editable [for='" + old_anchor + "']")
                .attr("for", new_anchor);
        },
    });

    // Add anchor to link dialog
    widget.LinkDialog.include({
        /**
         * Allow the user to use only an anchor.
         */
        get_data: function (test) {
            var $anchor = this.$el.find("#anchor");

            // Replace parent method if we have an anchor
            if (test !== false && $anchor.val()) {
                var $url_source = this.$el
                                  .find(".active input.url-source:input"),
                    style = this.$el
                            .find("input[name='link-style-type']:checked")
                            .val(),
                    size = this.$el
                           .find("input[name='link-style-size']:checked")
                           .val(),
                    classes = (style && style.length ? "btn " : "") +
                              style + " " + size;

                return new $.Deferred().resolve(
                    $url_source.val() + "#" + $anchor.val(),
                    this.$el.find("input.window-new").prop("checked"),
                    this.$el.find("#link-text").val() || $url_source.val(),
                    classes);

            // Fall back to parent method if no anchor is present
            } else {
                return this._super(test);
            }
        },

        /**
         * Put data in its corresponding place in the link dialog.
         *
         * When user edits an existing link that contains an anchor, put it
         * in its field.
         */
        bind_data: function () {
            var url = this.element && this.element.getAttribute("href"),
                url_parts = url && url.split("#", 2) || "";

            // Trick this._super()
            if (url_parts.length > 1) {
                this.element.setAttribute("href", url_parts[0]);
                this.$el.find("#anchor").val(url_parts[1]);
            }

            var result = this._super();

            // Back to expected status of this.element
            if (url_parts.length > 1) {
                this.element.setAttribute("href", url)
            }

            return result;
        },
    });

    return {
        Option: options.registry.anchor,
        LinkDialog: widget.LinkDialog,
    }
});
