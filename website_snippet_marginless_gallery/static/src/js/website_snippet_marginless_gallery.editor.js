/* © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

"use strict";
(function ($) {
    var prompt = openerp.website.prompt,
        snippet = openerp.website.snippet,
        _t = openerp._t;

    snippet.options.marginless_gallery = snippet.Option.extend({
        start: function () {
            var self = this;
            self._super();
            self.$el.find(".js_change_height").click(function () {
                return self.change_images_height();
            });
        },

        drop_and_build_snippet: function () {
            var self = this;
            self._super();
            self.change_images_height().fail(function () {
                self.$target.data("overlay")
                    .find(".oe_snippet_remove").click()
            });
        },

        change_images_height: function () {
            var self = this;
            return prompt({
                window_title: _t("Height for all images in gallery"),
                input: _t("Image height in pixels"),

            }).then(function (answer) {
                // Must be a number
                answer = Number(answer);
                if (isNaN(answer)) {
                    return failure();
                }

                self.$target
                    .find(".row > .img")
                    .css("height", answer ? answer + "px" : "");
            });
        },
    });
})(jQuery);
