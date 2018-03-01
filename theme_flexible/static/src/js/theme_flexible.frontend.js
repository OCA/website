/* Copyright 2018 Onestein
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define('theme_flexible.frontend', function(require) {
"use strict";

    var base = require('web_editor.base');

    base.ready().then(function () {
        var header = $('header');
        var navbar = $('header > .navbar');

        if (navbar.attr('data-do-stick') === '1') {
            var navbar_clone = navbar.clone();
            navbar_clone.addClass('navbar-fixed-top');
            header.append(navbar_clone);

            $(window).scroll(function() {
                if ($(window).scrollTop() > 15) {
                    navbar_clone.addClass('stick');
                } else if($(window).scrollTop() < 15) {
                    navbar_clone.removeClass('stick');
                }
            });

        }
    });
});
