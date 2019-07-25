// Copyright 2019 Therp BV <https://therp.nl>
// License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


odoo.define('website_base_form_handler.datepicker', function (require) {
    "use strict";
    var Time = require('web.time');
    var Translation = require('web.translation');

    require('website.website').ready().then(function () {
        // Apply date picker to all inputs marked as dates
        var $inputs = jQuery('input[type="date"]');
        // And make them normal inputs again
        $inputs.attr('type', 'text');
        $inputs.datetimepicker({
            format: Time.strftime_to_moment_format(
                Translation._t.database.parameters.date_format),
            language: moment.locale(),
            pickTime: false,
        });
    });
});
