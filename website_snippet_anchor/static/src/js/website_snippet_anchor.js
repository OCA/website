/* © 2015 Antiun Ingeniería S.L. - Jairo Llopis
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

"use strict";
(function ($) {
    var website = openerp.website,
        _t = openerp._t;

    // Option to have anchors in snippets
    website.snippet.options.anchor = website.snippet.Option.extend({
        start: function () {
            var self = this;
            self.$el.find(".js_anchor").click(function (event) {
                return self.select(event, _t("Choose anchor"));
            });
        },

        /**
         * Allow to set anchor name.
         */
        select: function (event, window_title, default_) {
            var self = this;
            default_ = default_ || self.$target.attr("id");
            website.prompt({
                "window_title": window_title,
                "default": default_,
                "input": _t("Name"),
            }).then(function (answer) {
                if (answer) {
                    if (-1 != $.inArray(answer,
                                  self.current_anchors(self.$target[0]))) {
                        return self.select(
                            event,
                            _t("Anchor already exists: ") + answer,
                            answer
                        );
                    } else {
                        self.update_anchor(self.$target, answer);
                    }
                } else {
                    self.$target.removeAttr("id");
                }
            });
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
         * Update an anchor and all its dependencies.
         */
        update_anchor: function ($element, new_anchor, old_anchor) {
            old_anchor = old_anchor || $element.attr("id");
            var new_hashed = "#" + new_anchor,
                old_hashed = "#" + old_anchor;

            // Set new anchor
            $element.attr("id", new_anchor);
            $element.attr("data-cke-saved-id", new_anchor);

            // Fix other elements' attributes. The "data-cke-saved-*" attribute
            // forces Odoo to update when no visible changes are made.
            $("[href='" + old_hashed + "'], \
               [data-cke-saved-href='" + old_hashed + "']")
                .attr("href", new_hashed)
                .attr("data-cke-saved-href", new_hashed);
            $("[data-target='" + old_hashed + "']")
                .attr("data-target", new_hashed);
            $("[for='" + old_anchor + "'], \
               [data-cke-saved-for='" + old_anchor + "']")
                .attr("for", new_anchor)
                .attr("data-cke-saved-for", new_anchor);
        },
    });

    // Load QWeb js snippets
    website.add_template_file(
        "/website_snippet_anchor/static/src/xml/website_snippet_anchor.xml");

    // Add anchor to link dialog
    website.editor.RTELinkDialog = website.editor.RTELinkDialog.extend({
        /**
         * Allow the user to use only an anchor.
         */
        get_data: function (test) {
            var $anchor = this.$el.find("#anchor");

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
            var url = this.element && (this.element.data("cke-saved-href")
                                   ||  this.element.getAttribute("href")),
                url_parts = url.split("#", 2),
                result = null;

            // Trick this._super()
            if (url_parts.length > 1) {
                this.element.setAttribute("href", url_parts[0]);
                this.element.data("cke-saved-href", url_parts[0])
                this.$el.find("#anchor").val(url_parts[1]);
            }

            result = this._super();

            // Back to expected status of this.element
            if (url_parts.length > 1) {
                this.element.setAttribute("href", url)
                this.element.data("cke-saved-href", url)
            }

            return result;
        },
    })
})(jQuery);
