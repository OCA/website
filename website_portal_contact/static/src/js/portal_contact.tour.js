/* Copyright 2016 Jairo Llopis <jairo.llopis@tecnativa.com>
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */

odoo.define("website_portal_contact.tour", function (require) {
    "use strict";

    var Tour = require("web.Tour");

    function in_url (needle) {
        return (location.pathname + location.search).indexOf(needle) !== -1;
    }

    function workaround_12961(needle, next_step) {
        return function () {
            if (in_url(needle)) {
                console.log(
                    "Applying workaround for " +
                    "https://github.com/odoo/odoo/issues/12961"
                );
                return next_step;
            }
        };
    }


    Tour.register({
        id: "website_portal_contact",
        name: "Website portal contact manager test",
        path: "/my/contacts",
        mode: "test",
        steps: [
            {
                title: "Click to add Guybrush",
                element: ".fa-plus",
                waitFor: ".fa-plus",
            },
            {
                title: "Fill name",
                element: "#name",
                waitFor: "#name",
                sampleText: "Guybrush Threpwood",
            },
            {
                title: "Fill phone",
                element: "#phone",
                sampleText: "987654321",
            },
            {
                title: "Fill mobile",
                element: "#mobile",
                sampleText: "123456789",
            },
            {
                title: "Fill email",
                element: "#email",
                sampleText: "guybrush@example.com",
            },
            {
                title: "Save new contact",
                element: "form#portal_contact .fa-cloud-upload",
                onload: workaround_12961("guybrush", "Change to Elaine"),
            },
            {
                title: "Change to Elaine",
                element: "#name",
                waitFor: "#name[value='Guybrush Threpwood']",
                sampleText: "Elaine Marley",
            },
            {
                title: "Change email",
                element: "#email",
                sampleText: "elaine@example.com",
            },
            {
                title: "Save changes",
                element: "form#portal_contact .fa-cloud-upload",
                onload: workaround_12961("elaine", "Delete Elaine"),
            },
            {
                title: "Delete Elaine",
                element: ".fa-trash",
                waitFor: "#name[value='Elaine Marley']",
            },
            {
                title: "Click to add LeChuck",
                element: ".fa-plus",
                waitFor: ".fa-plus",
                waitNot: "a:contains('Elaine')",
            },
            {
                title: "Fill LeChuck's name",
                element: "#name",
                waitFor: "#name",
                sampleText: "LeChuck",
            },
            {
                title: "Save LeChuck",
                element: "form#portal_contact .fa-cloud-upload",
                onload: workaround_12961("lechuck", "Return to list"),
            },
            {
                title: "Return to list",
                element: "a[href='/my/contacts']",
                waitFor: "#name[value='LeChuck']",
            },
            {
                title: "Search for Guybrush",
                element: "input[name=search]",
                waitFor: "input[name=search]",
                sampleText: "guybrush",
            },
            {
                title: "Click search for Guybrush",
                element: ".fa-search",
                onload: workaround_12961(
                    "search=guybrush",
                    "Guybrush not found, search for LeChuck"
                ),
            },
            {
                title: "Guybrush not found, search for LeChuck",
                element: "input[name=search]",
                waitFor: "input[name=search][value='guybrush']",
                waitNot: "table",
                sampleText: "lechuck",
            },
            {
                title: "Click search for LeChuck",
                element: ".fa-search",
                onload: workaround_12961("search=lechuck", "Delete LeChuck"),
            },
            {
                title: "Delete LeChuck",
                element: "tr:contains('LeChuck') .fa-trash",
                waitFor: "tr:contains('LeChuck') .fa-trash",
            },
            {
                title: "No remaining contacts!",
                waitNot: "tr:contains('LeChuck')",
            },
        ]
    });
});
