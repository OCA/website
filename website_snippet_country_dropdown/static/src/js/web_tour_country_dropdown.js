odoo.define("website_snippet_country_dropdown.tour_demo_page", function (require) {
    "use strict";

    var tour = require("web_tour.tour");
    var base = require("web_editor.base");

    var country_code_test = 'ES';
    var vat_number_test = 'B01010101';

    tour.register("website_snippet_country_dropdown_tour_demo_page", {
        url: "/website_snippet_country_dropdown.demo_page",
        wait_for: base.ready(),
    }, [{
        content: "Click Button",
        trigger: '.js_enabled .js_btn_country_code',
        run: "click",
    }, {
        content: "Select Country",
        trigger: _.str.sprintf('.js_enabled [data-country_code=%s]', country_code_test),
        run: "click",
    }, {
        content: "Insert text",
        trigger: '.js_enabled .js_no_country_field',
        extra_trigger: ".js_enabled .js_btn_country_code[data-country_code=ES]",
        run: "text " + vat_number_test,
    },
    {
        trigger: '.btn[type=submit]',
        run: "click",
    }, {
        trigger: ".js_enabled .js_btn_country_code[data-country_code=US]",
        run: function () {
            let checks = {
                country_code_field: "ES",
                complete_field: "ESB01010101",
                no_country_field: "B01010101",
                disabled_complete_field: "FRA123456789",
                disabled_country_code_field: "FR",
                disabled_no_country_field: "A123456789",
            };
            let query = new URLSearchParams(location.search);
            for (let field_name in checks) {
                let real = query.get(field_name), expected = checks[field_name];
                if (real !== expected) {
                    console.error(
                        "Tour error: param",
                        field_name,
                        "is",
                        real,
                        "but should be",
                        expected
                    );
                }
            }
        },
    }]);
});
