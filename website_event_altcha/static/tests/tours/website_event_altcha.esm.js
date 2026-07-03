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
            content: "Select a ticket",
            trigger: "#o_wevent_tickets_collapse select",
            run: "selectByIndex 1",
        },
        {
            content: "Verify altcha",
            trigger: "altcha-widget input[type='checkbox']",
            run: "click",
        },
        {
            content: "Click Submit",
            trigger: "#registration_form button[type='submit']:enabled",
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
        },
    ],
});
