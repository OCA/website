/* Copyright 2024 Tecnativa - David Vidal
   Copyright 2026 Tecnativa - Adasat Torres
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

import {registerWebsitePreviewTour} from "@website/js/tours/tour_utils";

registerWebsitePreviewTour(
    "conditional_visibility_portal",
    {
        url: "/",
    },
    () => [
        {
            content: "Go to '/'",
            trigger: 'header#top a[href="/"]',
            expectUnloadPage: true,
            run: "click",
        },
        {
            content: "The content previously hidden should now be visible",
            trigger: "body #wrapwrap",
            run: function () {
                const style = window.getComputedStyle(
                    this.anchor.getElementsByClassName("s_text_image")[0]
                );
                if (style.display === "none") {
                    console.error("error");
                }
            },
        },
    ]
);
