/* global window URLSearchParams console */
import {registry} from "@web/core/registry";

registry
    .category("web_tour.tours")
    .add("website_snippet_country_dropdown_tour_demo_page", {
        test: true,
        url: "/",
        steps: () => [
            {
                trigger: 'a[href="/website_snippet_country_dropdown.demo_page"]',
                run: "click",
            },
            {
                content: "Click Button",
                trigger: ".js_enabled .js_btn_country_code",
                run: "click",
            },
            {
                content: "Select Country",
                trigger: ".js_enabled [data-country_code=ES]",
                run: "click",
            },
            {
                content: "Make sure that the selection has been made",
                trigger: ".js_enabled .js_btn_country_code[data-country_code=ES]",
            },
            {
                content: "Insert text",
                trigger: ".js_enabled .js_no_country_field",
                run: "edit B01010101",
            },
            {
                trigger: ".btn[type=submit]",
                run: "click",
            },
            {
                trigger: ".js_enabled .js_btn_country_code[data-country_code=US]",
                run: function () {
                    const checks = {
                        country_code_field: "ES",
                        complete_field: "ESB01010101",
                        no_country_field: "B01010101",
                        disabled_complete_field: "FRA123456789",
                        disabled_country_code_field: "FR",
                        disabled_no_country_field: "A123456789",
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
