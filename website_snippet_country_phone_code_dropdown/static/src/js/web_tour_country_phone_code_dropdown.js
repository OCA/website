odoo.define(
    "website_snippet_country_phone_code_dropdown.tour_demo_page",
    function (require) {
        "use strict";

        const tour = require("web_tour.tour");
        const country_phone_code_test = "34";
        const number_test = "111 22 33 44";

        tour.register(
            "website_snippet_country_phone_code_dropdown_tour_demo_page",
            {
                url: "/website_snippet_country_phone_code_dropdown.demo_page",
            },
            [
                {
                    content: "Click Button",
                    trigger: ".js_enabled .js_btn_country_phone_code",
                    run: "click",
                },
                {
                    content: "Select Country",
                    trigger: _.str.sprintf(
                        ".js_enabled [data-country_phone_code=%s]",
                        country_phone_code_test
                    ),
                    run: "click",
                },
                {
                    content: "Insert text",
                    trigger: ".js_enabled .js_no_country_field",
                    extra_trigger:
                        ".js_enabled .js_btn_country_phone_code[data-country_phone_code=34]",
                    run: "text " + number_test,
                },
                {
                    trigger: ".btn[type=submit]",
                    run: "click",
                },
                {
                    trigger:
                        ".js_enabled .js_btn_country_phone_code[data-country_phone_code=1]",
                    run: function () {
                        const checks = {
                            country_phone_code_field: "+34",
                            complete_field: "+34 111 22 33 44",
                            no_country_field: "111 22 33 44",
                            disabled_complete_field: "+33 6 00 11 22 33",
                            disabled_country_phone_code_field: "+33",
                            disabled_no_country_field: "6 00 11 22 33",
                        };
                        const query = new URLSearchParams(location.search);
                        for (const field_name in checks) {
                            const real = query.get(field_name),
                                expected = checks[field_name];
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
                },
            ]
        );
    }
);
