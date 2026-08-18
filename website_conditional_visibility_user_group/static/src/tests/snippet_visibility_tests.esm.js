/* Copyright 2024 Tecnativa - David Vidal
   Copyrigt 2026 Tecnativa - Adasat Torres
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */
import {
    changeOptionInPopover,
    clickOnEditAndWaitEditMode,
    clickOnSave,
    clickOnSnippet,
    insertSnippet,
    registerWebsitePreviewTour,
} from "@website/js/tours/tour_utils";

const snippets = [
    {
        id: "s_text_image",
        name: "Text - Image",
        groupName: "Content",
    },
];
registerWebsitePreviewTour(
    "conditional_visibility_only_internal_user",
    {
        url: "/",
        edition: true,
    },
    () => [
        ...insertSnippet(snippets[0]),
        ...clickOnSnippet(snippets[0]),
        ...changeOptionInPopover("Text - Image", "Visibility", "Conditionally"),
        ...changeOptionInPopover("Text - Image", "Users", "Visible for Logged In"),
        ...changeOptionInPopover("Text - Image", "Groups", "Only portal users"),
        ...clickOnSave(),
        {
            trigger: ".o_website_preview",
        },
        {
            content: "Check if the rule was applied",
            trigger: ":iframe #wrap:not(:visible)",
            run: function () {
                const style = window.getComputedStyle(
                    this.anchor.getElementsByClassName("s_text_image")[0]
                );
                if (style.display !== "none") {
                    console.error("error");
                }
            },
        },
        ...clickOnEditAndWaitEditMode(),
        {
            content:
                "Check if the element is visible as it should always be visible in edit view",
            trigger: ":iframe #wrap .s_text_image",
            run: function () {
                const style = window.getComputedStyle(this.anchor);
                if (style.display === "none") {
                    console.error("error");
                }
            },
        },
        ...clickOnSave(),
    ]
);
