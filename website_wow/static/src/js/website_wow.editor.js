/* Copyright 2017 LasLabs Inc.
   License GPL-3.0 or later (http://www.gnu.org/licenses/gpl).
*/

odoo.define('website_wow.website_wow_editor', function (require) {
    'use strict';

    var s_options = require('web_editor.snippets.options');

    s_options.registry.o_wow = s_options.Class.extend({


        select_class: function (type, value, $li) {
            this._super.apply(this, arguments);

            if (type !== "click") {
                return;
            }

            var animationEnd = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';

            this.$target.addClass('wow').addClass('animated').one(
                animationEnd,
                function () {
                    $(this).removeClass('wow animated').css('animation-name', '');
                }
            );

        },

        clean_for_save: function () {
            if (this.$target.hasClass('o_wow_animate')) {
                this.$target.addClass('wow');
            } else {
                this.$target.removeClass('wow');
            }
        }

    })

})
