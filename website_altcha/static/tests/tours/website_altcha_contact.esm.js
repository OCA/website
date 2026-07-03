/* Copyright 2026 Hunki Enterprises BV */
import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("website_altcha_contact", {
    steps: () => [
        {
            content: "Fill in a name",
            trigger: "input[name='name']",
            run: "fill Testname",
        },
        {
            content: "Fill in an email",
            trigger: "input[name='email_from']",
            run: "fill test_website_altcha@test.com",
        },
        {
            content: "Fill in a subject",
            trigger: "input[name='subject']",
            run: "fill the subject",
        },
        {
            content: "Fill in a question",
            trigger: "textarea[name='description']",
            run: "fill the question",
        },
        {
            content: "Verify altcha",
            trigger: "altcha-widget input[type='checkbox']",
            run: "click",
        },
        {
            content: "Verify altcha value exists",
            trigger: "input[name='altcha']:not(:visible):not(:empty)",
        },
        {
            content: "Click Submit",
            trigger: "div.s_website_form_submit a",
            run: "click",
        },
    ],
});
