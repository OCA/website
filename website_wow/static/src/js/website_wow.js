/* Copyright 2017 LasLabs Inc.
   License GPL-3.0 or later (http://www.gnu.org/licenses/gpl).
*/

odoo.define('website_wow.website_wow', function (require) {
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

        bindListeners: function () {

        },

        wowSettings: function () {
            return {};
        }

    }

    base.ready().then(function () {
        WebsiteWow.start();
    });

    return {
        'WebsiteWow': WebsiteWow
    }

})
