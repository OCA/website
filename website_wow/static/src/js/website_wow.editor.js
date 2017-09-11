/* Copyright 2017 LasLabs Inc.
   License GPL-3.0 or later (http://www.gnu.org/licenses/gpl).
*/

odoo.define('website_wow.editor', function (require) {
    'use strict';

    var s_options = require('web_editor.snippets.options');

    var Mixin = s_options.Class.extend({

        select_class: function (type, value, $li) {
            this._super.apply(this, arguments);
            this.setWowData(this.$target, value);
            this.previewAnimation(this.$target);
        },

        clean_for_save: function () {
            this.cleanForSave(this.$target);
        },

        clearAnimationStyles: function ($target) {
            var styles = [
                'visibility',
                'animation-name',
                'animation-duration',
                'animation-delay',
                'animation-offset',
                'animation-iteration',
            ];
            $target.removeClass('wow animated');
            _.each(styles, function(style) {
                $target.css(style, '');
            });
        },

        previewAnimation: function ($target) {
            var self = this;
            var animationEnd = 'webkitAnimationEnd mozAnimationEnd MSAnimationEnd oanimationend animationend';
            this.clearAnimationStyles($target);
            $target.addClass('wow').addClass('animated').one(
                animationEnd,
                function () {
                    self.clearAnimationStyles($(this));
                }
            );
        },

        cleanForSave: function ($target) {
            if ( $target.hasClass('o_wow_animate') ) {
                $target.addClass('wow');
            } else {
                $target.removeClass('wow');
            }
        },

        setWowData: function ($target, dataClass) {

            var wowData = dataClass.split('-');
            var dataType = wowData[0].replace('o_wow_', '');
            var dataVal = wowData[1];

            if (!dataVal) {
                return;
            }

            // Note that `.data` cannot be used because it doesn't actually
            // append to the HTML, so the attribute isn't saved.
            if ($target.hasClass(dataClass)) {
                $target.attr('data-wow-' + dataType, dataVal);
            } else {
                $target.attr('data-wow-' + dataType, '');
            }

        }

    })

    // Animations
    s_options.registry.o_wow = Mixin.extend({});

    // Duration
    s_options.registry.o_wow_duration = Mixin.extend({});

    // Delay
    s_options.registry.o_wow_delay = Mixin.extend({});

    // Offset
    s_options.registry.o_wow_offset = Mixin.extend({});

    // Iteration
    s_options.registry.o_wow_iteration = Mixin.extend({});

})
