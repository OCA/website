/* Copyright 2019 Tecnativa - Sergio Teruel
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

odoo.define("website_event_filter_organizer.tour", function (require) {
    "use strict";

    var base = require('web_editor.base');
    var tour = require("web_tour.tour");

    var steps = [
        {
            trigger: "a[href='/event?organizer=all']",
            extra_trigger: "a:contains('Deco Addict')",
        },
        {
            trigger: "a[href='/']",
            extra_trigger: "ul:has(span:contains('Event One')):has(span:contains('Event Two'))",
        },
        {
            trigger: "a:contains('Deco Addict')",
        },
        {
            trigger: "a[href='/event']",
            extra_trigger: "#middle_column > ul:not(:has(span:contains('Event One')))",
        },
    ];

    tour.register(
        "website_event_filter_organizer",
        {
            url: "/event",
            test: true,
            wait_for: base.ready(),
        },
        steps
    );

    return {
        steps: steps,
    };
});
