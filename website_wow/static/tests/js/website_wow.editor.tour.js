/* Copyright 2017 LasLabs Inc.
   License GPL-3.0 or later (http://www.gnu.org/licenses/gpl).
*/

odoo.define('website_wow.tour_editor', function (require) {
    'use strict';

    var tour = require("web_tour.tour");
    var base = require("web_editor.base");
    var snippet_editor = require('web_editor.snippet.editor');

    tour.register("website_wow_editor", {
        url: '/?debug=assets&enable_editor=1',
        test: true,
        wait_for: base.ready(),
    }, [{
        content: 'Click an animable element.',
        trigger: 'footer div.col-md-4:first',
        run: function() {
            $('footer div.col-md-4:first').click();
        }
    }, {
        content: 'Click the customize menu.',
        trigger: 'a.btn[title="Customize"]',
    }, {
        content: 'Check that animation preview works',
        trigger: 'li.snippet-option-o_wow',
        run: function () {
            var $bounce = $('li[data-select_class="o_wow_animate bounce"]');
            var $div = $('footer div.col-md-4:first');
            debugger;
            $bounce.click();
            if ( ! $div.hasClass('o_wow_animate') ) {
                tour._consume_tour(
                    tour.running_tour,
                    'Element does not contain class `o_wow_animate`'
                );
            }
            if ( ! $div.hasClass('bounce') ) {
                tour._consume_tour(
                    tour.running_tour,
                    'Element does not contain class `bounce`'
                );
            }
        }
    }, {
        content: 'Click Save',
        trigger: 'btn[@data-action="save"]',
    }, {
        content: 'Check that `wow` class was added after save.',
        trigger: 'div.wow',
    }, {
        content: 'Click Edit',
        trigger: 'btn[@data-action="edit"]',
    }, {
        content: 'Click '
    }, {
        content: 'Click an animable element.',
        trigger: 'footer div.col-md-4:first',

    }, {
        content: 'Click the customize menu.',
        trigger: 'a.btn[title="Customize"]',
    }, {
        content: 'Check that `Wow!` is present in customize menu',
        trigger: 'li.snippet-option-o_wow_duration',
        run: function () {
            $('li.snippet-option-o_wow_duration').addClass('open');
        }
    }, {
        content: 'Check that option sets data attribute.',
        trigger: 'li.o_wow_duration-1s',
        run: function () {
            var $duration = $('li.o_wow_duration-1s > a');
            var $div = $('footer div.col-md-4:first');
            $duration.click();
            if ( $div.data('wow-duration') != '1s' ) {
                tour._consume_tour(
                    tour.running_tour,
                    'Element does not contain proper duration data',
                );
            }
        }
    }])

})
