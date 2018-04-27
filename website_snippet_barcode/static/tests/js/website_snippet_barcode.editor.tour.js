/* Copyright 2017 LasLabs Inc.
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html). */

odoo.define("website_snippet_barcode.tour_editor", function (require) {
    "use strict";

    var tour = require("web_tour.tour");
    var base = require("web_editor.base");

    function checkBarcodeType(barcodeType) {
        var $barcode = $('footer .o_barcode');
        var $barcodeImg = $('footer .o_barcode .o_barcode_img');
        if ( $barcode.attr('data-type') !== barcodeType ) {
            tour._consume_tour(
                tour.running_tour,
                'Barcode does not have data-type ' + barcodeType
            );
        }
        if ( $barcodeImg.attr('src').indexOf('?type=' + barcodeType) < 0 ) {
            tour._consume_tour(
                tour.running_tour,
                'Barcode image source was not updated to ' + barcodeType + ' barcode'
            );
        }
    }

    tour.register("website_snippet_barcode", {
        url: '/?enable_editor=1',
        test: true,
        wait_for: base.ready()
    }, [{
        content: 'Create a barcode.',
        trigger: '#snippet_content .oe_snippet[name="Barcode"] .oe_snippet_thumbnail',
        run: 'drag_and_drop footer .row div:eq(2) '
    }, {
        content: 'Click the barcode.',
        trigger: 'footer .o_barcode',
        run: 'click'
    }, {
        content: 'Click the customize menu.',
        trigger: 'a.btn[title=Customize]'
    }, {
        content: 'Check that barcode preview works',
        trigger: 'li.snippet-option-barcode',
        run: function () {
            var $code128 = $('li[data-select_type="Code128"]');
            $code128.find('a:first').click();
            checkBarcodeType('Code128');
        }
    }, {
        content: 'Click Save',
        trigger: 'button[data-action=save]'
    }, {
        content: 'Check that barcode is `Code128` type after save.',
        trigger: 'footer .o_barcode',
        run: function () {
            checkBarcodeType('Code128');
        }
    }, {
        content: 'Click Edit',
        trigger: 'a[data-action=edit]'
    }, {
        content: "Create another barcode because Odoo sucks and won't " +
                 "click the existing one from within a test.",
        trigger: '#snippet_content .oe_snippet[name="Barcode"] .oe_snippet_thumbnail',
        run: 'drag_and_drop footer .row div:eq(2) '
    }, {
        content: 'Click the barcode.',
        trigger: 'footer .o_barcode:last',
        run: 'click'
    }, {
        content: 'Click the customize menu.',
        trigger: 'a.btn[title="Customize"]'
    }, {
        content: 'Check that human readable text option displays value in footer.',
        trigger: 'li.snippet-option-barcode',
        run: function () {
            var $textOption = $('li[data-select_humanreadable="text"]');
            $textOption.find('a:first').click();
            var $barcode = $('footer .o_barcode:last');
            var barcodeValue = decodeURIComponent($barcode.attr('data-value'));
            var $barcodeFooterText = $barcode.find('.o_barcode_footer p');
            if ( $barcodeFooterText.hasClass('hidden') ) {
                tour._consume_tour(
                    tour.running_tour,
                    'Hidden class was not removed from footer text'
                );
            }
            if ( $barcodeFooterText.text() !== barcodeValue ) {
                tour._consume_tour(
                    tour.running_tour,
                    'Barcode value was not added to footer text'
                );
            }
        }
    }, {
        content: 'Click the barcode.',
        trigger: 'footer .o_barcode:last',
        run: 'click'
    }, {
        content: 'Click the customize menu.',
        trigger: 'a.btn[title="Customize"]'
    }, {
        content: 'Check that human readable image option hides value in footer.',
        trigger: 'li.snippet-option-barcode',
        run: function () {
            var $imageOption = $('li[data-select_humanreadable="image"]');
            $imageOption.find('a:first').click();
            var $barcode = $('footer .o_barcode:last');
            var $barcodeFooterText = $barcode.find('.o_barcode_footer p');
            if ( ! $barcodeFooterText.hasClass('hidden') ) {
                tour._consume_tour(
                    tour.running_tour,
                    'Hidden class was not added to footer text'
                );
            }
            if ( $barcodeFooterText.text() !== '' ) {
                tour._consume_tour(
                    tour.running_tour,
                    'Footer text was not removed'
                );
            }
        }
    }, {
        content: 'Click the barcode.',
        trigger: 'footer .o_barcode:last',
        run: 'click'
    }, {
        content: 'Click the customize menu.',
        trigger: 'a.btn[title="Customize"]'
    }, {
        content: 'Check that selecting "Set Custom Value" opens dialog modal.',
        trigger: 'li.snippet-option-barcode',
        run: function () {
            var $customValueOption = $('li[data-select_value="custom"]');
            $customValueOption.find('a:first').click();
            var $barcode = $('footer .o_barcode:last');
            var barcodeValue = decodeURIComponent($barcode.attr('data-value'));
            var $dialog = $('.modal-dialog').last();
            if ( $dialog.find('.modal-title').text() !== 'Custom Barcode Value' ) {
                tour._consume_tour(
                    tour.running_tour,
                    'A dialog modal was not opened'
                );
            }
            if ( $dialog.find('.modal-body input').val() !== barcodeValue ) {
                tour._consume_tour(
                    tour.running_tour,
                    'Modal dialog was not pre-populated with the current barcode value'
                );
            }
        }
    }, {
        content: 'Change custom barcode value.',
        trigger: '.modal-dialog:contains("Custom Barcode Value")',
        run: function () {
            var $input = $('.modal-dialog:contains("Custom Barcode Value") .modal-body input');
            $input.val('Test');
        }
    }, {
        content: 'Click the continue button.',
        trigger: '.modal-dialog button:contains("Continue")',
        run: 'click'
    }, {
        content: 'Check that clicking "Continue" on dialog modal sets new barcode value.',
        trigger: 'footer .o_barcode:last',
        run: function () {
            var $barcode = $('footer .o_barcode:last');
            var barcodeValue = decodeURIComponent($barcode.attr('data-value'));
            if ( barcodeValue !== 'Test' ) {
                tour._consume_tour(
                    tour.running_tour,
                    'Barcode value was not changed to custom value'
                );
            }
        }
    }, {
        content: 'Click the barcode.',
        trigger: 'footer .o_barcode:last',
        run: 'click'
    }, {
        content: 'Click the customize menu.',
        trigger: 'a.btn[title="Customize"]'
    }, {
        content: 'Check that selecting "Current Page URI" sets barcode value to current URI.',
        trigger: 'li.snippet-option-barcode',
        run: function () {
            var $currentValueOption = $('li[data-select_value="current"]');
            $currentValueOption.find('a:first').click();
            var $barcode = $('footer .o_barcode:last');
            var barcodeValue = decodeURIComponent($barcode.attr('data-value'));
            var currentURI = window.location.href.split('#')[0];
            if ( barcodeValue !== currentURI ) {
                tour._consume_tour(
                    tour.running_tour,
                    'Barcode value not set to current page URI'
                );
            }
        }
    }]);

});
