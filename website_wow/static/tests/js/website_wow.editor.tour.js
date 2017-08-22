/* Copyright 2017 LasLabs Inc.
   License GPL-3.0 or later (http://www.gnu.org/licenses/gpl).
*/

odoo.define('website_wow.tour_editor', function (require) {
    'use strict';

    var tour = require("web_tour.tour");
    var base = require("web_editor.base");
    var snippet_editor = require('web_editor.snippet.editor');

    require('website_wow.editor');
    require('website_wow.view');

    tour.register("website_wow_editor", {
        url: '/page/contactus?debug=assets&enable_editor=1',
        test: true,
        wait_for: base.ready(),
    }, [{
        content: 'Create an animable element.',
        trigger: 'div[name=Cover]',
        run: function () {
            var $snippet = $('section.s_text_block_image_fw');
            var $div = $('<div class="oe_structure o_editable o_dirty note-air-editor note-editable" data-oe-id="239" data-oe-model="ir.ui.view" data-oe-field="arch" data-oe-xpath="/t[1]/t[1]/div[1]/div[3]" data-note-id="1" contenteditable="true"></div>');
            $div.append($snippet);
            $('main').append($div);
            $snippet.addClass('o_dirty');
            // Save the element that we created
            $('button[data-action=save]').click();
            // But our element causes some weird error, so discard (it's still saved somehow...)
            $('button[data-action=cancel]').click();
            // Click OK
            $('span:contains("Ok")').parent().click();
        }
    }, {
        content: 'Go back to edit',
        trigger: 'a[data-action=edit]',
        run: function () {
            $('a[data-action=edit]').click();
        }
    }, {
        content: 'Click an animable element.',
        trigger: 'main h2:contains("Headline")',
        run: function () {
            debugger;
            $('main h2:contains("Headline")').click();
        }
    }, {
        content: 'Click the customize menu.',
        trigger: 'a.btn[title="Customize"]',
    }, {
        content: 'Check that animation preview works',
        trigger: 'li.snippet-option-o_wow',
        run: function () {
            var $bounce = $('li[data-select_class="o_wow_animate bounce"]');
            var $div = $('main h2:contains("Headline")');
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
        trigger: 'button[data-action=save]',
    }, {
        content: 'Check that `wow` class was added after save.',
        trigger: 'a.wow',
    }, {
        content: 'Click Edit',
        trigger: 'button[data-action="edit"]',
    }, {
        content: 'Click an animable element.',
        trigger: 'main h2:contains("Headline")',
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
            var $div = $('main h2:contains("Headline")');
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
