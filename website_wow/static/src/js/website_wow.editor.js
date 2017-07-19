/* Copyright 2017 LasLabs Inc.
   License GPL-3.0 or later (http://www.gnu.org/licenses/gpl).
*/

odoo.define('website_wow.website_wow_editor', function (require) {
    'use strict';

    var s_options = require('web_editor.snippets.options');

    function previewAnimation ($target) {
        var animationEnd = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
        $target.removeClass('wow animated').css('animation-name', '');
        $target.addClass('wow').addClass('animated').one(
            animationEnd,
            function () {
                $(this).removeClass('wow animated').css('animation-name', '');
            }
        );
    }

    function setWowData (dataClass, $target) {

        var wowData = dataClass.split('-');
        var dataType = wowData[0].replace('o_wow_', '');
        var dataVal = wowData[1];

        // Note that `.data` cannot be used because it doesn't actually
        // append to the HTML, so the attribute isn't saved.
        if ($target.hasClass(dataClass)) {
            $target.attr('data-wow-' + dataType, dataVal);
        } else {
            $target.attr('data-wow-' + dataType, '');
        }

    };

    // Animations
    s_options.registry.o_wow = s_options.Class.extend({

        select_class: function (type, value, $li) {
            this._super.apply(this, arguments);
            if (type !== "click") {
                return;
            }
            previewAnimation(this.$target);
        },

        clean_for_save: function () {
            if (this.$target.hasClass('o_wow_animate')) {
                this.$target.addClass('wow');
            } else {
                this.$target.removeClass('wow');
            }
        }

    });

    // Duration
    s_options.registry.o_wow_duration = s_options.Class.extend({

        select_class: function (type, value, $li) {
            this._super.apply(this, arguments);
            if (type !== "click") {
                return;
            }
            setWowData($li.data('select_class'), this.$target);
            previewAnimation(this.$target);
        },

    })

})
