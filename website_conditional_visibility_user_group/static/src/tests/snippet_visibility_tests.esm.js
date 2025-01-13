/** @odoo-module */
/* Copyright 2024 Tecnativa - David Vidal
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */
import wTourUtils from "@website/js/tours/tour_utils";

wTourUtils.registerWebsitePreviewTour(
    "conditional_visibility_only_internal_user",
    {
        test: true,
        url: "/",
        edition: true,
    },
    () => [
        wTourUtils.dragNDrop({id: "s_text_image", name: "Text - Image"}),
        wTourUtils.clickOnSnippet({
            id: "s_text_image",
            name: "Text - Image",
        }),
        wTourUtils.changeOption("ConditionalVisibility", "we-toggler"),
        wTourUtils.changeOption(
            "ConditionalVisibility",
            '[data-name="visibility_conditional"]'
        ),
        {
            content: "Click in User visibility",
            trigger: '[data-save-attribute="visibilityValueLogged"]',
            run: "click",
        },
        {
            content: "Set visibility to logged in users",
            trigger: '[data-name="visibility_logged_in"]',
            run: "click",
        },
        {
            content: "Click in group visibility",
            trigger: '[data-save-attribute="visibilityUserGroup"]',
            run: "click",
        },
        {
            content: "Set visibility to logged internal users only",
            trigger: '[data-name="user_group_internal"]',
            run: "click",
        },
        ...wTourUtils.clickOnSave(),
        {
            content: "Check if the rule was applied",
            trigger: "iframe #wrap .s_text_image",
            run: function () {
                const style = window.getComputedStyle(this.$anchor[0]);
                if (style.display === "none") {
                    console.error(
                        "Error: this item should be visible for internal users"
                    );
                }
            },
        },
    ]
);
