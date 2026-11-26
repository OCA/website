/* Copyright 2026 Dixmit */
import {registry} from "@web/core/registry";

registry.category("web_tour.tours").add("website_altcha_login", {
    steps: () => [
        {
            content: "Fill in the login",
            trigger: ".oe_login_form input[name='login']",
            run: "fill admin",
        },
        {
            content: "Fill in the password",
            trigger: ".oe_login_form input[name='password']",
            run: "fill admin",
        },
        {
            content: "Verify altcha",
            trigger: ".oe_login_form altcha-widget input[type='checkbox']",
            run: "click",
        },
        {
            content: "Verify altcha value exists",
            trigger: "input[name='altcha']:not(:visible):not(:empty)",
        },
        {
            content: "Click Log in",
            trigger: ".oe_login_form button[type='submit']",
            run: "click",
            expectUnloadPage: true,
        },
        {
            content: "Logged in",
            trigger: ".o_portal_my_home",
        },
    ],
});
