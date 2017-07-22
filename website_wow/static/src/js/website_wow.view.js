/* Copyright 2017 LasLabs Inc.
   License GPL-3.0 or later (http://www.gnu.org/licenses/gpl).
*/

odoo.define('website_wow.view', function (require) {
    'use strict';

    var base = require('web_editor.base');
    var core = require('web.core');

    var WebsiteWow = {

        start: function () {
            this.$els = $('.o_animate');
            this.$els.addClass('wow');
            this.bindListeners();
            this.wow = new WOW(this.wowSettings());
            this.wow.init();
        },

        /* Use this method in child modules to add event listeners on start */
        bindListeners: function () {},

        /* Use this method in child modules to control the WowJS settings.
            The WowJS defaults are currently being returned, primarily to
            serve as documentation.
         */
        wowSettings: function () {
            return {
                boxClass: 'wow',
                animateClass: 'animated',
                offset: 0,
                mobile: true,
                live: true
            };
        }

    }

    base.ready().then(function () {
        WebsiteWow.start();
    });

    return {
        'WebsiteWow': WebsiteWow
    }

})
