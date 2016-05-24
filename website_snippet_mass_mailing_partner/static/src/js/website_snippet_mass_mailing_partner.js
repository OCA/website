/* © 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl). */

"use strict";
(function ($) {
    openerp.website.snippet.animationRegistry.subscribe.include({
        on_click: function() {
            var self = this;
            var $email = this.$target.find(".js_subscribe_email:visible");
            var $name = this.$target.find(".js_subscribe_name:visible");

            if (
                ($email.length && !$email.val().match(/.+@.+/)) ||
                ($name.length && !$name.val())
            ) {
                this.$target.addClass('has-error');
                return false;
            }
            this.$target.removeClass('has-error');

            openerp.jsonRpc('/website_mass_mailing/subscribe', 'call', {
                'list_id': this.$target.data('list-id'),
                'email': $email.length ? $email.val() : false,
                'name': $name.length && $name.val(),
            }).then(function (subscribe) {
                self.$target.children("input, span").addClass("hidden");
                self.$target.find(".alert").removeClass("hidden");
                self.$target.find('input.js_subscribe_email')
                    .attr("disabled", subscribe);
                self.$target.attr("data-subscribe", subscribe ? 'on' : 'off');
            });
        },
    });
})(jQuery);
