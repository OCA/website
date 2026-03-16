/* global window URLSearchParams console */
import {registry} from "@web/core/registry";

registry
    .category("web_tour.tours")
    .add("website_snippet_country_phone_code_dropdown_tour_demo_page", {
        test: true,
        url: "/",
        steps: () => [
            {
                trigger: 'a:contains("Country Phone Code Dropdown Demo"):not(:visible)',
                run: "click",
            },
            {
                content: "Click Button",
                trigger: ".js_enabled .js_btn_country_phone_code",
                run: "click",
            },
            {
                content: "Select Country",
                trigger: '.js_enabled [data-country_phone_code="34"]',
                run: "click",
            },
            {
                content: "Make sure that the selection has been made",
                trigger:
                    '.js_enabled .js_btn_country_phone_code[data-country_phone_code="34"]',
            },
            {
                content: "Insert text",
                trigger: ".js_enabled .js_no_country_field",
                run: "edit 111 22 33 44",
            },
            {
                trigger: ".btn[type=submit]",
                run: "click",
            },
            {
                trigger:
                    '.js_enabled .js_btn_country_phone_code[data-country_phone_code="1"]',
                run: function () {
                    const checks = {
                        country_phone_code_field: "+34",
                        complete_field: "+34 111 22 33 44",
                        no_country_field: "111 22 33 44",
                        disabled_complete_field: "+33 6 00 11 22 33",
                        disabled_country_phone_code_field: "+33",
                        disabled_no_country_field: "6 00 11 22 33",
                    };
                    const query = new URLSearchParams(window.location.search);
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
        ],
    });
