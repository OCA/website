/** @odoo-module */
/* Copyright 2024 Tecnativa - David Vidal
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */
import tour from "web_tour.tour";
import wTourUtils from "website.tour_utils";

const snippet = {
    id: "s_text_image",
    name: "Text - Image",
};

tour.register(
    "conditional_visibility_only_internal_user",
    {
        test: true,
        url: "/",
    },
    [
        {
            content: "Enter edit mode",
            trigger: "a[data-action=edit]",
            extraTrigger: "#wrap",
        },
        wTourUtils.dragNDrop(snippet),
        wTourUtils.clickOnSnippet(snippet),
        wTourUtils.changeOption("ConditionalVisibility", "we-toggler"),
        {
            content: "Set conditional visibility",
            trigger: '[data-name="visibility_conditional"]',
            extraTrigger: ".s_text_image",
            run: "click",
        },
        {
            content: "Set visibility to logged in users",
            trigger: '[data-save-attribute="visibilityValueLogged"]',
            extraTrigger: ".s_text_image",
            run: "click",
        },
        {
            content: "Set visibility to internal users only",
            trigger: '[data-save-attribute="visibilityUserGroup"]',
            extraTrigger: ".s_text_image",
            run: "click",
        },
        {
            content: "Select internal user group",
            trigger: '[data-name="user_group_internal"]',
            extraTrigger: ".s_text_image",
            run: "click",
        },
        ...wTourUtils.clickOnSave(),
        {
            content: "Check if the rule was applied",
            trigger: "#wrap .s_text_image",
            extraTrigger: ".s_text_image",
            run: function () {
                setTimeout(() => {
                    const element = this.$anchor[0].querySelector(".s_text_image");
                    if (!element) {
                        console.error("Error: Element not found");
                        return;
                    }
                    const style = window.getComputedStyle(element);
                    if (style.display === "none") {
                        console.error(
                            "Error: This item should be visible for internal users"
                        );
                    }
                }, 100);
            },
        },
    ]
);
