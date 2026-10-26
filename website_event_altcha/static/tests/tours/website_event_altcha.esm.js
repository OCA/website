/* Copyright 2026 Hunki Enterprises BV */
import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("website_event_altcha", {
    steps: () => [
        {
            content: "Click register button",
            trigger: "button[data-bs-target='#modal_ticket_registration']",
            run: "click",
        },
        {
            content: "Click Register",
            trigger: ".o_wevent_js_ticket_details .a-submit:not([disabled])",
            run: "click",
        },
        {
            content: "Verify altcha",
            trigger: "altcha-widget input[type='checkbox']",
            run: "click",
        },
        {
            content: "Fill in name",
            trigger: "#attendee_registration input[name*='-name-']:enabled",
            async run() {
                this.anchor.value = "Testname";
            },
        },
        {
            content: "Fill in email",
            trigger: "#attendee_registration input[name*='-email-']:enabled",
            async run() {
                this.anchor.value = "test_website_altcha@test.com";
            },
        },
        {
            content: "Verify altcha value exists",
            trigger:
                "#attendee_registration input[name='altcha']:not(:visible):not(:empty)",
        },
        {
            content: "Click submit",
            trigger: "#attendee_registration button[type='submit']",
            run: "click",
            expectUnloadPage: true,
        },
        {
            content: "Registration successful",
            trigger: "div.o_wereg_confirmed",
        },
    ],
});
