/* Copyright 2026 Hunki Enterprises BV */
import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("website_altcha_signup", {
    steps: () => [
        {
            content: "Fill in a login",
            trigger: "input[name='login']",
            run: "fill admin",
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
            trigger: "button[type='submit']",
            run: "click",
        },
    ],
});
