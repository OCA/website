/* Copyright 2015-2017 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html). */

odoo.define('website_marginless_gallery.gallery', function(require) {
    "use strict";
    var _t = require("web.core")._t;
    var Dialog = require("web.Dialog");
    var options = require('web_editor.snippets.options');
    var website = require("website.website");

    return options.registry.marginless_gallery = options.Class.extend({
        auto_remove: function () {
            return this.$target.data("overlay")
                .find(".oe_snippet_remove").click();
        },

        drop_and_build_snippet: function () {
            this.change_images_height("click")
                .fail($.proxy(this, "auto_remove"));
            return this._super.apply(this, arguments);
        },

        change_images_height: function (type) {
            if (type !== "click") return;
            return website.prompt({
                window_title: _t("Height for all images in gallery"),
                input: _t("Image height in pixels"),

            }).then(
                $.proxy(this, "images_height_changed"),
                $.proxy(this, "images_height_failed")
            );
        },

        images_height_changed: function (pixels) {
            // Must be a number
            pixels = Number(pixels);
            if (isNaN(pixels)) {
                return $.Deferred().reject(pixels);
            }
            this.$target
                .find(".row > .img")
                .css("height", pixels ? pixels + "px" : "");
        },

        images_height_failed: function (pixels) {
            return pixels && Dialog.alert(
                this,
                _.str.sprintf(_t("%s is not a valid value"), pixels)
            );
        }
    });
});
