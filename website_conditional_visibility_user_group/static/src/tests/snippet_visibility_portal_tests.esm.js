/** @odoo-module */
/* Copyright 2024 Tecnativa - David Vidal
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */
import tour from "web_tour.tour";

tour.register(
    "conditional_visibility_portal",
    {
        test: true,
        url: "/",
    },
    [
        {
            content: "The content should be hidden for portal users",
            trigger: "#wrap",
            run: function () {
                const style = window.getComputedStyle(
                    this.$anchor[0].getElementsByClassName("s_text_image")[0]
                );
                if (style.display !== "none") {
                    console.error(
                        "Error: This item should be invisible for portal users"
                    );
                }
            },
        },
    ]
);
