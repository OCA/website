/* © 2015 Grupo ESOC Ingeniería de Servicios, S.L.U. - Jairo Llopis
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */

(function ($) {
    'use strict';

    var snippet = openerp.website.snippet;

    snippet.animationRegistry.big_button = snippet.Animation.extend({
        selector: ".js_big_button",
        start: function(editable_mode) {
            if (!editable_mode) {
                this.$target.click(this.on_click);
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
})(jQuery);
