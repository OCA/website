/** @odoo-module */

/* Copyright 2015-2017 Tecnativa - Jairo Llopis <jairo.llopis@tecnativa.com>
 * Copyright 2019 Tecnativa - Cristina Martin R.
 * Copyright 2020 Tecnativa - Alexandre D. Díaz
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html). */

import {
    clickOnSave,
    insertSnippet,
    registerWebsitePreviewTour,
} from "@website/js/tours/tour_utils";

registerWebsitePreviewTour(
    "marginless_gallery",
    {
        url: "/",
        edition: true,
    },
    () => [
        ...insertSnippet({
            id: "s_marginless_gallery",
            name: "Marginless Gallery",
            groupName: "Images",
        }),
        ...clickOnSave(),
    ]
);
