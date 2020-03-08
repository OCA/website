/* Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */

odoo.define('website_portal_address.tour_test', function (require) {
    'use strict';

    var tour = require('web_tour.tour');
    // var core = require('web.core');
    var base = require('web_editor.base');

    // Get an element in the selection filters form
    // function sel(name) {
    //     return _.str.sprintf("%s select[name='%s']", id, name);
    // }
    //
    // // Get an option value by its text
    // function opt_val(option_text) {
    //     return function (action_helper) {
    //         var option_id = this.$anchor.children(_.str.sprintf(
    //             "option:contains('%s')", option_text
    //         )).val();
    //         action_helper.text(option_id);
    //     };
    // }

    var steps = [
        {
            content: 'Click to add Guybrush',
            trigger: 'div.col-md-4.col-md-offset-4.mt8 > a',
            waitFor: 'div.col-md-4.col-md-offset-4.mt8 > a',
            position: 'top',
            run: 'click',
        },
        {
            content: 'Select "Shipping address"',
            trigger: '#radio212_delivery',
            run: 'click',
        },
        {
            content: 'Fill name "Guybrush Threpwood"',
            trigger: '#name',
            run: 'text Guybrush Threpwood',
        },
        {
            content: 'Fill phone',
            trigger: '#phone',
            run: 'text 987654321',
        },
        {
            content: 'Fill mobile',
            trigger: '#mobile',
            run: 'text 123456789',
        },
        {
            content: 'Fill email "guybrush@example.com"',
            trigger: '#email',
            run: 'text guybrush@example.com',
        },
        {
            content: 'Fill address "123 address"',
            trigger: '#street',
            run: 'text 123 address',
        },
        {
            content: 'Fill address2 "456 address"',
            trigger: '#street2',
            run: 'text 456 address',
        },
        {
            content: 'Fill city "Big city"',
            trigger: '#city',
            run: 'text Big city',
        },
        {
            content: 'Fill zip "h0h0h0"',
            trigger: '#zip',
            run: 'text h0h0h0',
        },
        // TODO fix this tests
        // {
        //     content: 'Select country',
        //     trigger: sel("country_id"),
        //     run: opt_val("Canada"),
        // },
        // {
        //     content: 'Select state',
        //     trigger: sel("state_id"),
        //     run: opt_val("Quebec"),
        // },
        {
            content: 'Save new contact Guybrush',
            trigger: '#portal_contact > section > div > button',
            run: 'click',
            wait: 11500,
        },
        {
            content: 'Return to list',
            trigger: 'a[href="/my/contacts"]',
            run: 'click',
        },
        {
            content: 'Search for Guybrush',
            trigger: '#wrap > div.container.mb64 > div.row.mt16.mb16 > div.col-md-4.mt8 > form > div > input',
            waitFor: '#wrap > div.container.mb64 > div.row.mt16.mb16 > div.col-md-4.mt8 > form > div > input',
            position: 'top',
            run: 'text guybrush',
        },
        {
            content: 'Click search for Guybrush',
            position: 'top',
            trigger: '#wrap > div.container.mb64 > div.row.mt16.mb16 > div.col-md-4.mt8 > form > div > span > button',
            run: 'click',
        },
        {
            content: 'Delete Guybrush',
            trigger: 'tr:contains("Guybrush") td.text-center > a',
            waitFor: 'tr:contains("Guybrush")',
            run: 'click',
        },
        {
            content: 'Return to home',
            trigger: 'a[href="/my/home"]',
            run: 'click',
        }
    ];

    tour.register('test_website_portal_address', {
            test: true,
            url: '/my/contacts',
            wait_for: base.ready(),
            'skip_enabled': true
        },
        steps
    );
});
