/* Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */
odoo.define("website_portal_crm_claim.tour", function (require) {
    "use strict";
    var Tour = require("web.Tour");

    return Tour.register({
        id: "website_portal_crm_claim",
        name: "Try to demostrate how to create a tour",
        path: "/my/home",
        mode: "test",
        steps: [
            {
                title: "Go to your claims",
                element: "a[href='/my/claims']:has(.badge:contains('1'))",
                waitFor: "a[href='/my/claims']:has(.badge:contains('1'))",
            },
            {
                title: "Enter your only claim",
                element: "a[href^='/my/claims/problem-with-the-delivery']",
                waitFor: ".o_my_status_table tbody tr:nth-child(1)",
                waitNot: ".o_my_status_table tbody tr:nth-child(2)",
            },
            {
                title: "Enter a message",
                element: "textarea[name='message']",
                waitFor: ".panel, .o_website_chatter_form",
                sampleText: "Hello",
            },
            {
                title: "Send the message",
                element: ".o_website_message_post_helper",
            },
            {
                title: "Wait for the message to appear",
                waitFor: ".o_website_comments .media" +
                         ":contains('Demo Portal User'):contains('Hello')",
            }
        ]
    });
});
