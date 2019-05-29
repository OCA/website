/**
*    Copyright 2016 Antiun Ingeniería S.L. - Jairo Llopis
*    Copyright 2016 LasLabs Inc.
*    License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
**/

odoo.define('website_anchor_smooth_scroll', function (require) {
    'use strict';

    var base = require('web_editor.base');

    var smooth_scroll = function (event) {
        event.preventDefault();
        var anchor_fragment = event.target.hash;

        // Do this before scrolling so that browser history
        // accurately reflects scroll position at time of click
        history.pushState(null, document.title, anchor_fragment);

        return $('html, body').stop().animate({
            'scrollTop': $(anchor_fragment).offset().top - 100,
        }).promise();
    };

    base.ready().done(function () {
        $('a[href^="#"][href!="#"][href!="#advanced-view-editor"]')
            .click(smooth_scroll);
    });

    return {'scroll_handler': smooth_scroll};
});
