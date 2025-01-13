/** @odoo-module */
/* Copyright 2024 Tecnativa - David Vidal
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

import wTourUtils from "@website/js/tours/tour_utils";

wTourUtils.registerWebsitePreviewTour(
    "conditional_visibility_portal",
    {
        test: true,
        url: "/",
    },
    () => [
        {
            content: "Go to '/'",
            trigger: 'header#top a[href="/"]',
        },
        {
            content: "The content should be hidden for portal users",
            trigger: "#wrap",
            run: function () {
                const elements = this.$anchor[0].getElementsByClassName("s_text_image");
                if (elements.length === 0) {
                    console.log("Success: Element is not visible for portal users");
                } else {
                    const style = window.getComputedStyle(elements[0]);
                    if (style.display !== "none") {
                        console.error(
                            "Error: This item should be invisible for portal users"
                        );
                    }
                }
            },
        },
    ]
);
