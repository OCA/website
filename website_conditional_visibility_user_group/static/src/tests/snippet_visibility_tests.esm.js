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
            content: "enter edit mode",
            trigger: "a[data-action=edit]",
        },
        wTourUtils.dragNDrop(snippet),
        wTourUtils.clickOnSnippet(snippet),
        wTourUtils.changeOption("ConditionalVisibility", "we-toggler"),
        {
            content: "Set on conditional visibility",
            trigger: '[data-name="visibility_conditional"]',
            run: "click",
        },
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
            trigger: "body:not(.editor_enable) #wrap",
            run: function () {
                const style = window.getComputedStyle(
                    this.$anchor[0].getElementsByClassName("s_text_image")[0]
                );
                if (style.display === "none") {
                    console.error(
                        "Error: this item should be visible for internal users"
                    );
                }
            },
        },
    ]
);
