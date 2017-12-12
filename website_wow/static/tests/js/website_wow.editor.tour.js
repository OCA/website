/* Copyright 2017 LasLabs Inc.
   License GPL-3.0 or later (http://www.gnu.org/licenses/gpl).
*/

odoo.define('website_wow.tour_editor', function (require) {
    'use strict';

    var tour = require("web_tour.tour");
    var base = require("web_editor.base");

    tour.register("website_wow_editor", {
        test: true,
        wait_for: base.ready(),
    }, [{
        content: 'Create an animable element.',
        trigger: '#snippet_structure .oe_snippet:eq(1) .oe_snippet_thumbnail',
        run: 'drag_and_drop'
    }, {
        content: 'Click an animable element.',
        trigger: 'main h2:contains("Headline"):first',
        run: 'click'
    }, {
        content: 'Click the customize menu.',
        trigger: 'a.btn[title=Customize]'
    }, {
        content: 'Check that animation preview works',
        trigger: 'li.snippet-option-o_wow',
        run: function () {
            var $bounce = $('li[data-select_class="o_wow_animate bounce"]');
            var $div = $('main h2:contains("Headline"):first').parent();
            $bounce.find('a:first').click();
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
        trigger: 'button[data-action=save]'
    }, {
        content: 'Check that `wow` class was added after save.',
        trigger: 'div.o_wow_animate.bounce.wow'
    }, {
        content: 'Click Edit',
        trigger: 'a[data-action=edit]'
    }, {
        content: "Create another animable element because Odoo sucks and won't " +
                 "click the existing one from within a test.",
        trigger: '#snippet_structure .oe_snippet:eq(1) .oe_snippet_thumbnail',
        run: 'drag_and_drop'
    }, {
        content: 'Click an animable element.',
        trigger: 'main h2:contains("Headline"):first',
        run: 'click'
    }, {
        content: 'Click the customize menu.',
        trigger: 'a.btn[title="Customize"]'
    }, {
        content: 'Check that option sets data attribute.',
        trigger: 'li.snippet-option-o_wow',
        run: function () {
            var $duration = $('li[data-select_class="o_wow_duration-1s"]');
            var $div = $('main h2:contains("Headline"):first').parent();
            $duration.find('a:first').click();
            if ( $div.data('wow-duration') != '1s' ) {
                tour._consume_tour(
                    tour.running_tour,
                    'Element does not contain proper duration data',
                );
            }
        }
    }])

})
