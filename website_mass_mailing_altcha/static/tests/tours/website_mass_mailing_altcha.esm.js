/* Copyright 2026 Nitrokey GmbH */
import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("website_mass_mailing_altcha", {
    steps: () => [
        {
            content: "Verify the widget was inserted",
            trigger: ".js_subscribe altcha-widget",
        },
        {
            content: "Fill in the email address",
            trigger: ".js_subscribe input.js_subscribe_value",
            run: "edit test_website_mass_mailing_altcha@test.com",
        },
        {
            content: "Subscribe without verifying first",
            trigger: ".js_subscribe .js_subscribe_btn",
            run: "click",
        },
        {
            content: "Verify altcha solved the challenge on the fly",
            trigger:
                ".js_subscribe altcha-widget input[name='altcha']:not(:visible):not(:empty)",
        },
        {
            content: "Verify the subscription was accepted",
            trigger: ".js_subscribe .js_subscribed_wrap:not(.d-none)",
        },
    ],
});
